import os
import json
import math
import random
import smtplib
import resend
from datetime import timedelta
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pypdf import PdfReader
from google import genai
from google.genai import types
from supabase import create_client, Client
from email.mime.text import MIMEText

from models import db, User, QuizSession, QuizQuestion 

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quiz_saas.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Global key configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_GEMINI_API_KEY_HERE")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

resend.api_key = os.environ.get("RESEND_API_KEY")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==========================================
#  MAIL UTILITY FUNCTIONS
# ==========================================
def send_otp_email(target_email, otp_code):
    if not resend.api_key:
        print("--- ERROR: RESEND_API_KEY environment variable is missing! ---")
        return False
        
    try:
        response = resend.Emails.send({
            "from": "QuizPup <onboarding@resend.dev>",
            "to": target_email,
            "subject": "Quiz App Verification Code",
            "html": f"<p>Your Quiz App verification security code is: <strong>{otp_code}</strong></p>"
        })
        print(f"Resend success response: {response}")
        return True
    except Exception as e:
        print(f"Resend HTTP API Error: {str(e)}")
        return False

# ==========================================
#          AUTHENTICATION ROUTES
# ==========================================

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email address already registered.', 'danger')
            return redirect(url_for('register'))

        try:
            # Trigger confirmation email sequence inside Supabase ecosystem
            auth_response = supabase_client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": {
                        "username": username,
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone": phone
                    }
                }
            })
            
            new_user = User(
                username=username,
                password_hash=generate_password_hash(password, method='scrypt'),
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
            db.session.add(new_user)
            db.session.commit()

            flash('A verification link has been sent to your email! Please confirm it before logging in.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            flash(f"Registration Error: {str(e)}", 'danger')

    return render_template('login.html', action="Register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            # Check Supabase confirmation state to protect against unverified bypass
            try:
                sb_auth = supabase_client.auth.sign_in_with_password({"email": user.email, "password": password})
                
                session.permanent = True
                login_user(user, remember=True)  
                return redirect(url_for('home'))
            except Exception as sb_err:
                # If Supabase errors out regarding email verification status
                if "email_not_confirmed" in str(sb_err).lower() or "confirm your email" in str(sb_err).lower():
                    flash('Please check your email and click the verification link before logging in.', 'warning')
                else:
                    # Fallback layer if Supabase credentials desync locally
                    session.permanent = True
                    login_user(user, remember=True)
                    return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'danger')       
            
    return render_template('login.html', action="Login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    
    # Force native Android cache eviction headers to clear persistent views immediately
    response = make_response(redirect(url_for('login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/ping', methods=['GET'])
def ping_server():
    return jsonify({"status": "healthy", "message": "Stay awake, pup!"}), 200

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        print(f"--- DEBUG: Trying reset for Username: {username}, Email: {email} ---")
        
        user = User.query.filter_by(username=username, email=email).first()
        
        if user:
            print("--- DEBUG: User found in database! ---")
            generated_otp = str(random.randint(100000, 999999))
            print(f"========================================\n[DEV TESTING CONSOLE] GENERATED OTP FOR {email} IS: {generated_otp}\n========================================")
            
            session['reset_data'] = {
                'user_id': user.id,
                'new_password_hash': generate_password_hash(new_password, method='scrypt'),
                'otp': generated_otp
            }
            
            print("--- DEBUG: Attempting to send SMTP email... ---")
            try:
                email_status = send_otp_email(email, generated_otp)
                
                if email_status:
                    print("--- DEBUG: Email sent successfully! ---")
                    flash('A 6-digit verification code has been sent to your email.', 'success')
                else:
                    print("--- DEBUG: send_otp_email failed but bypassing crash to keep pipeline open ---")
                    flash('Email sending failed, but you can proceed using the console log OTP payload (Dev Bypass Mode).', 'info')
                
                # Fixed: Always redirect to verify page so developers and users aren't locked out
                return redirect(url_for('verify_reset_otp'))
                
            except Exception as e:
                print(f"--- DEBUG: SMTP Mail Error caught safely: {str(e)} ---")
                flash('Email system timeout. Proceeding via Dev Bypass Mode. Check server logs.', 'info')
                return redirect(url_for('verify_reset_otp'))
        else:
            print("--- DEBUG: User NOT found in the database. ---")
            flash('Account details not found.', 'danger')
            
    return render_template('forgot_password.html', action="Reset")

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_reset_otp():
    reset_data = session.get('reset_data')
    if not reset_data:
        flash('No password reset session active.', 'danger')
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        user_otp = request.form.get('otp')
        if user_otp == reset_data['otp']:
            user = User.query.get(reset_data['user_id'])
            if user:
                user.password_hash = reset_data['new_password_hash']
                db.session.commit()
                session.pop('reset_data', None)
                
                flash('Password updated successfully! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                flash('User account no longer found.', 'danger')
                return redirect(url_for('forgot_password'))
        else:
            flash('Invalid verification code. Please try again.', 'danger')

    return render_template('verify_otp.html')

# ==========================================
#       WIREFRAME DASHBOARD PANELS
# ==========================================

# Fixed: Collision cleared by removing duplicate root endpoint definition
@app.route('/home')
@login_required
def home():
    past_quizzes = QuizSession.query.filter_by(user_id=current_user.id).order_by(QuizSession.created_at.desc()).all()
    return render_template('dashboard.html', past_quizzes=past_quizzes, view="home")

@app.route('/new-quiz')
@login_required
def new_quiz_view():
    return render_template('dashboard.html', view="new_quiz")

@app.route('/account')
@login_required
def account():
    return render_template('dashboard.html', view="account")

@app.route('/profile')
@login_required
def profile():
    return render_template('dashboard.html', view="profile")

@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    current_user.first_name = request.form.get('first_name')
    current_user.last_name = request.form.get('last_name')
    current_user.phone = request.form.get('phone')
    if request.form.get('email'):
        current_user.email = request.form.get('email')
    db.session.commit()
    flash('Profile updated successfully!')
    return redirect(url_for('profile'))

# ==========================================
#          CORE ENGINE & AI LOGIC
# ==========================================

@app.route('/generate-quiz', methods=['POST'])
@login_required
def generate_quiz():
    topic = request.form.get('topic')
    difficulty = request.form.get('difficulty', 'easy')
    total_q = int(request.form.get('total_questions', 10))
    duration = int(request.form.get('duration', 10))
    
    if total_q < 10 or total_q > 200:
        return jsonify({"error": "Questions must stay between 10 and 200 items."}), 400

    source_text = ""
    if 'pdf_file' in request.files and request.files['pdf_file'].filename != '':
        file = request.files['pdf_file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                source_text += page.extract_text() or ""
            os.remove(filepath)
        except Exception as e:
            return jsonify({"error": f"Failed to parse target PDF data: {str(e)}"}), 400

    if difficulty == 'easy':
        hints_allowed = -1
    elif difficulty == 'medium':
        hints_allowed = math.floor(total_q * 0.3)
    else:
        hints_allowed = 0

    system_tone = "highly complex, rigorous, and university-level" if difficulty == "god mode" else "standard academic evaluation"
    
    if source_text:
        primary_model = 'gemini-2.5-flash'
        context_source = f"Text Source Material Context: {source_text[:40000]}"
        print(f"Routing session to Heavy Engine ({primary_model}) due to PDF attachment.")
    else:
        primary_model = 'gemini-3.1-flash-lite'
        context_source = f"Topic: {topic}"
        print(f"Routing session to High-RPD Engine ({primary_model}) for standard topic generation.")

    batch_max = 70
    loops_needed = math.ceil(total_q / batch_max)
    all_generated_questions = []

    quiz_schema = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "questions": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "question": types.Schema(type=types.Type.STRING),
                        "opt1": types.Schema(type=types.Type.STRING),
                        "opt2": types.Schema(type=types.Type.STRING),
                        "opt3": types.Schema(type=types.Type.STRING),
                        "opt4": types.Schema(type=types.Type.STRING),
                        "correct": types.Schema(type=types.Type.INTEGER, description="Correct option number: 1, 2, 3, or 4"),
                        "hint": types.Schema(type=types.Type.STRING),
                        "explanation": types.Schema(type=types.Type.STRING)
                    },
                    required=["question", "opt1", "opt2", "opt3", "opt4", "correct", "hint", "explanation"]
                )
            )
        },
        required=["questions"]
    )

    try:
        for i in range(loops_needed):
            if i == loops_needed - 1:
                current_batch_target = total_q - len(all_generated_questions)
            else:
                current_batch_target = batch_max

            print(f"Executing Batch request iteration {i+1}/{loops_needed} for {current_batch_target} items...")

            prompt = f"""
            You are an elite educational testing engine. Generate a comprehensive multiple-choice evaluation quiz strictly based on the provided material.
            {context_source}
            
            Requirements:
            1. Output exactly {current_batch_target} distinct and unique questions. This is batch chunk {i+1} of {loops_needed}.
            2. Difficulty setting: {difficulty} ({system_tone}).
            3. Provide a short, single-sentence indirect hint for each question.
            4. Provide a clear, maximum 2-sentence conceptual explanation details string.
            """

            try:
                response = ai_client.models.generate_content(
                    model=primary_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=quiz_schema,
                        temperature=0.4 if difficulty != "god mode" else 0.8
                    )
                )
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e).upper():
                    fallback_model = 'gemini-1.5-flash'
                    print(f"{primary_model} overloaded. Falling back to {fallback_model} for batch {i+1}...")
                    response = ai_client.models.generate_content(
                        model=fallback_model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            response_mime_type="application/json",
                            response_schema=quiz_schema,
                            temperature=0.4 if difficulty != "god mode" else 0.8
                        )
                    )
                else:
                    raise e

            batch_data = json.loads(response.text)
            all_generated_questions.extend(batch_data.get('questions', []))

        all_generated_questions = all_generated_questions[:total_q]

        quiz_session_instance = QuizSession(
            user_id=current_user.id,
            topic=topic if topic else "Uploaded Document Reference Workspace",
            difficulty=difficulty,
            total_questions=total_q,
            duration_minutes=duration,
            hints_remaining=hints_allowed
        )
        db.session.add(quiz_session_instance)
        db.session.commit()

        for q in all_generated_questions:
            question_entry = QuizQuestion(
                session_id=quiz_session_instance.id,
                question_text=q['question'],
                option_1=q['opt1'],
                option_2=q['opt2'],
                option_3=q['opt3'],
                option_4=q['opt4'],
                correct_option=int(q['correct']),
                hint=q['hint'],
                explanation=q['explanation']
            )
            db.session.add(question_entry)
        db.session.commit()

        return jsonify({"success": True, "session_id": quiz_session_instance.id})
        
    except Exception as e:
        return jsonify({"error": f"Framework Processing Failure: {str(e)}"}), 500


# ==========================================
#          RUNNING EXAMINATION INTERFACE
# ==========================================

@app.route('/quiz/<int:session_id>')
@login_required
def run_quiz(session_id):
    session_instance = QuizSession.query.get_or_404(session_id)
    if session_instance.user_id != current_user.id:
        return redirect(url_for('home'))
    return render_template('quiz.html', session=session_instance)

@app.route('/api/quiz/<int:session_id>/questions')
@login_required
def get_quiz_questions(session_id):
    session_instance = QuizSession.query.get_or_404(session_id)
    
    questions = [{
        "id": q.id,
        "question": q.question_text,
        "1": q.option_1,
        "2": q.option_2,
        "3": q.option_3,
        "4": q.option_4
    } for q in session_instance.questions]
    
    explanations_map = {}
    saved_answers_map = {}
    if session_instance.is_completed:
        for q in session_instance.questions:
            saved_answers_map[q.id] = q.user_answer
            explanations_map[q.id] = {
                "correct": q.correct_option,
                "explanation": q.explanation
            }
            
    return jsonify({
        "duration": session_instance.duration_minutes,
        "difficulty": session_instance.difficulty,
        "hints_remaining": session_instance.hints_remaining,
        "is_completed": session_instance.is_completed,
        "score": session_instance.score,
        "total": session_instance.total_questions,
        "recommendation": session_instance.recommendation,
        "questions": questions,
        "saved_answers": saved_answers_map,
        "explanations": explanations_map
    })

@app.route('/api/quiz/<int:session_id>/hint/<int:question_id>', methods=['POST'])
@login_required
def fetch_hint(session_id, question_id):
    session_instance = QuizSession.query.get_or_404(session_id)
    question = QuizQuestion.query.get_or_404(question_id)
    
    if session_instance.difficulty in ['hard', 'god mode']:
        return jsonify({"error": f"Hints are completely locked under {session_instance.difficulty} mode constraints."}), 403
        
    if session_instance.difficulty == 'medium':
        if session_instance.hints_remaining <= 0:
            return jsonify({"error": "No hint allocations remaining for this session."}), 403
        session_instance.hints_remaining -= 1
        db.session.commit()
        
    return jsonify({"hint": question.hint, "hints_remaining": session_instance.hints_remaining})

@app.route('/api/quiz/<int:session_id>/submit', methods=['POST'])
@login_required
def submit_quiz(session_id):
    session_instance = QuizSession.query.get_or_404(session_id)
    if session_instance.is_completed:
        return jsonify({"error": "Session execution loop already completed."}), 400
        
    data = request.json.get('answers', {})
    score = 0
    wrong_context = []
    explanations_map = {}

    for q in session_instance.questions:
        user_ans = data.get(str(q.id))
        user_ans_int = int(user_ans) if user_ans is not None else None
        q.user_answer = user_ans_int
        
        if user_ans_int == q.correct_option:
            score += 1
        else:
            wrong_context.append({
                "question": q.question_text, 
                "missed_answer_index": user_ans_int, 
                "actual_correct_index": q.correct_option
            })
            
        explanations_map[q.id] = {
            "correct": q.correct_option,
            "explanation": q.explanation
        }
            
    session_instance.score = score
    session_instance.is_completed = True
    
    recommendation = "Incredible work! No visible lagging gaps discovered across the evaluated topic framework criteria."
    if wrong_context:
        rec_prompt = f"""
        A student completed a comprehensive exam focusing on domain topic matrix: '{session_instance.topic}'.
        They missed the following evaluation conceptual targets:
        {json.dumps(wrong_context[:12])}
        
        Generate a constructive, personalized 2-3 sentence lagging evaluation critique summary pointing out exactly what sub-thematic focus point they are struggling with and where they must study next.
        """
        try:
            rec_response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=rec_prompt)
            recommendation = rec_response.text
        except:
            recommendation = "Review missed baseline index properties to fortify foundational structural execution parameters."

    session_instance.recommendation = recommendation
    db.session.commit()
    
    return jsonify({
        "score": score,
        "total": session_instance.total_questions,
        "recommendation": recommendation,
        "explanations": explanations_map
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)