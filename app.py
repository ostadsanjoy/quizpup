import os
import json
import math
import random
import uuid
import requests
import base64
import concurrent.futures
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from google import genai
from google.genai import types
from supabase import create_client, Client
from flashcard_data import PRELOADED_DECKS

from models import db, User, QuizSession, QuizQuestion 

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quiz_saas.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_GEMINI_API_KEY_HERE")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL")
MAIL_FROM_NAME = "QuizPup"

OTP_VALID_MINUTES = 10
OTP_MAX_ATTEMPTS = 5

PRELOADED_DECKS = {
    "JEE": [
        {"question": "What is the hybridisation of Cl in ClO4-?", "answer": "sp3 hybridisation"},
        {"question": "State the conditions required for Rolle's Theorem on interval [a,b].", "answer": "f(x) must be continuous on [a,b], differentiable on open (a,b), and f(a) = f(b)."},
        {"question": "Evaluate value of Integral dx/(1+x^2) bounded from 0 to 1.", "answer": "pi / 4"}
    ],
    "NEET": [
        {"question": "Where exactly does the Krebs cycle take place in eukaryotic cellular geometry?", "answer": "Within the internal mitochondrial matrix space."},
        {"question": "What is the primary physiological function of interstitial Leydig cells?", "answer": "Synthesis and secretion of testicular androgen hormones (testosterone)."},
        {"question": "Which specific adenohypophyseal hormone triggers immediate ovulation cycles?", "answer": "Luteinizing Hormone (LH surge)."}
    ],
    "CAT": [
        {"question": "What is the combinations equation to distribute n items containing p identical entities?", "answer": "Total paths = n! / p!"},
        {"question": "Solve for base element x constraints if: log_2(x) + log_4(x) = 6.", "answer": "Calculated value x = 16"},
        {"question": "Define a structural network bottleneck inside Data Interpretation resource pathways.", "answer": "A localized point or node constraint that defines the absolute peak capacity flow of the complete graph map."}
    ]
}

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def send_email(target_email, subject, html_body):
    if not BREVO_API_KEY or not BREVO_SENDER_EMAIL:
        print("--- ERROR: BREVO_API_KEY or BREVO_SENDER_EMAIL environment variable is missing! ---")
        return False

    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={
                "api-key": BREVO_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json"
            },
            json={
                "sender": {"name": MAIL_FROM_NAME, "email": BREVO_SENDER_EMAIL},
                "to": [{"email": target_email}],
                "subject": subject,
                "htmlContent": html_body
            },
            timeout=10
        )
        if response.status_code in (200, 201):
            return True
        return False
    except Exception:
        return False

def send_otp_email(target_email, otp_code):
    return send_email(
        target_email,
        "Quiz App Verification Code",
        f"<p>Your Quiz App verification security code is: <strong>{otp_code}</strong></p>"
    )

def send_verification_email(target_email, otp_code):
    return send_email(
        target_email,
        "Verify your QuizPup account",
        f"<p>Welcome to QuizPup! Your account verification code is: <strong>{otp_code}</strong></p>"
        f"<p>This code expires in {OTP_VALID_MINUTES} minutes.</p>"
    )

def generate_otp():
    return str(random.randint(100000, 999999))

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

        if not email:
            flash('Email address is required.', 'danger')
            return redirect(url_for('register'))

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('Email address already registered.', 'danger')
            return redirect(url_for('register'))

        otp_code = generate_otp()
        new_user = User(
            username=username,
            password_hash=generate_password_hash(password, method='scrypt'),
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            is_verified=False,
            verification_otp=otp_code,
            verification_otp_expires=datetime.utcnow() + timedelta(minutes=OTP_VALID_MINUTES),
            verification_attempts=0
        )
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('That username or email was just taken by someone else. Please try again.', 'danger')
            return redirect(url_for('register'))

        try:
            supabase_client.auth.sign_up({
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
        except Exception as e:
            print(f"Supabase sign_up notice: {str(e)}")

        session['pending_verification_user_id'] = new_user.id

        if send_verification_email(email, otp_code):
            flash('Account created! Check your email for a 6-digit verification code.', 'success')
        else:
            flash('Account created, but we could not send the verification email right now. Tap "Resend code" on the next screen to try again.', 'warning')

        return redirect(url_for('verify_email'))

    return render_template('login.html', action="Register")

@app.route('/verify-email', methods=['GET', 'POST'])
def verify_email():
    user_id = session.get('pending_verification_user_id')
    if not user_id:
        flash('No pending verification found. Please register or log in.', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, user_id)
    if not user:
        session.pop('pending_verification_user_id', None)
        flash('Account not found.', 'danger')
        return redirect(url_for('register'))

    if user.is_verified:
        session.pop('pending_verification_user_id', None)
        flash('Your account is already verified. Please log in.', 'success')
        return redirect(url_for('login'))

    if request.method == 'POST':
        expired = (not user.verification_otp_expires) or datetime.utcnow() > user.verification_otp_expires
        if expired:
            flash('Your verification code expired. Please request a new one.', 'danger')
        elif user.verification_attempts >= OTP_MAX_ATTEMPTS:
            flash('Too many incorrect attempts. Please request a new code.', 'danger')
        else:
            submitted_otp = request.form.get('otp')
            if submitted_otp == user.verification_otp:
                user.is_verified = True
                user.verification_otp = None
                user.verification_otp_expires = None
                user.verification_attempts = 0
                db.session.commit()
                session.pop('pending_verification_user_id', None)
                flash('Email verified! Please log in.', 'success')
                return redirect(url_for('login'))
            else:
                user.verification_attempts += 1
                db.session.commit()
                remaining = OTP_MAX_ATTEMPTS - user.verification_attempts
                flash(f'Invalid verification code. {remaining} attempt(s) remaining.', 'danger')

    return render_template('verify_email.html', email=user.email)

@app.route('/verify-email/resend', methods=['POST'])
def resend_verification_email():
    user_id = session.get('pending_verification_user_id')
    if not user_id:
        flash('No pending verification found.', 'danger')
        return redirect(url_for('login'))

    user = db.session.get(User, user_id)
    if not user or user.is_verified:
        return redirect(url_for('login'))

    otp_code = generate_otp()
    user.verification_otp = otp_code
    user.verification_otp_expires = datetime.utcnow() + timedelta(minutes=OTP_VALID_MINUTES)
    user.verification_attempts = 0
    db.session.commit()

    if send_verification_email(user.email, otp_code):
        flash('A new verification code has been sent.', 'success')
    else:
        flash('Could not send the email right now. Please try again shortly.', 'danger')

    return redirect(url_for('verify_email'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            if not user.is_verified:
                session['pending_verification_user_id'] = user.id
                flash('Please verify your email before logging in. Check your inbox for the code.', 'warning')
                return redirect(url_for('verify_email'))

            try:
                supabase_client.auth.sign_in_with_password({"email": user.email, "password": password})
            except Exception as sb_err:
                print(f"Supabase sign_in notice: {str(sb_err)}")

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
    
    response = make_response(redirect(url_for('login')))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.delete_cookie('session', path='/')
    response.delete_cookie('remember_token', path='/')
    
    return response

# ==========================================
#          PASSWORD RECOVERY ROUTES
# ==========================================

@app.route('/forgot-username', methods=['GET', 'POST'])
def forgot_username():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            send_email(
                email,
                "Your QuizPup Username Reminder",
                f"<p>Hello,</p><p>You requested a username reminder. Your account username identifier is: <strong>{user.username}</strong></p><p>Have a great study session!</p>"
            )
            flash('Username reminder message successfully dispatched to your email address.', 'success')
        else:
            flash(f'No accounts related to {email}', 'danger')
            
    return render_template('forgot_username.html')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            otp_code = generate_otp()
            user.verification_otp = otp_code
            user.verification_otp_expires = datetime.utcnow() + timedelta(minutes=OTP_VALID_MINUTES)
            db.session.commit()
            
            send_otp_email(email, otp_code)
            session['reset_password_email'] = email
            flash('A verification recovery code has been sent to your email address.', 'success')
            return redirect(url_for('verify_otp'))
        else:
            flash('No active account found containing this email address.', 'danger')
            
    return render_template('forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    email = session.get('reset_password_email')
    if not email:
        return redirect(url_for('forgot_password'))
        
    user = User.query.filter_by(email=email).first()
    if not user:
        return redirect(url_for('forgot_password'))
        
    if request.method == 'POST':
        submitted_otp = request.form.get('otp')
        new_password = request.form.get('new_password')
        
        if not submitted_otp or not new_password:
            flash('Both the verification code and chosen password fields are required.', 'danger')
            return render_template('verify_otp.html', email=email)
        
        if submitted_otp == user.verification_otp:
            user.password_hash = generate_password_hash(new_password, method='scrypt')
            user.verification_otp = None
            db.session.commit()
            
            session.pop('reset_password_email', None)
            flash('Your account security password has been updated successfully. Please login.', 'success')
            return redirect(url_for('login'))
        else:
            flash('Invalid or active recovery code token mismatch.', 'danger')
            
    return render_template('verify_otp.html', email=email)

# ==========================================
#       WIREFRAME DASHBOARD PANELS
# ==========================================

@app.route('/home')
@login_required
def home():
    past_quizzes = QuizSession.query.filter_by(user_id=current_user.id).order_by(QuizSession.created_at.desc()).all()
    return render_template('dashboard.html', past_quizzes=past_quizzes, view="home")

@app.route('/flashcards')
@login_required
def flashcards_view():
    return render_template('dashboard.html', view="flashcards")

@app.route('/study')
@login_required
def study_view():
    return render_template('dashboard.html', view="study")

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
    db.session.commit()
    return redirect(url_for('profile'))

# ==========================================
#        NEW FLASHCARD & STUDY ASYNC APIs
# ==========================================

@app.route('/api/flashcards/preload', methods=['GET'])
@login_required
def preload_flashcards():
    exam_target = request.args.get('exam', 'JEE').upper()
    exam_deck = PRELOADED_DECKS.get(exam_target, [])
    
    return jsonify({"success": True, "deck": exam_deck})

@app.route('/api/flashcards/generate', methods=['POST'])
@login_required
def generate_ai_flashcards():
    data = request.get_json() or {}
    topic = data.get('topic', '')
    if not topic:
        return jsonify({"success": False, "error": "Topic argument is completely missing."}), 400

    fc_schema = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "cards": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "question": types.Schema(type=types.Type.STRING),
                        "answer": types.Schema(type=types.Type.STRING)
                    },
                    required=["question", "answer"]
                )
            )
        },
        required=["cards"]
    )

    prompt = f"Create exactly 5 revision flashcards matching the core parameter topic context: '{topic}'. Keep answers concise."
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=fc_schema,
                temperature=0.5
            )
        )
        res_data = json.loads(response.text)
        return jsonify({"success": True, "deck": res_data.get('cards', [])})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/study/process-notes', methods=['POST'])
@login_required
def process_study_notes():
    if 'note_file' not in request.files:
        return jsonify({"success": False, "error": "Payload key mismatch."}), 400
    
    file = request.files['note_file']
    if file.filename == '':
        return jsonify({"success": False, "error": "Empty filename."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{filename}")
    file.save(filepath)

    extracted_text = ""
    is_pdf = filename.lower().endswith('.pdf')

    try:
        if is_pdf:
            reader = PdfReader(filepath)
            for page in reader.pages:
                extracted_text += page.extract_text() or ""
            
            if not extracted_text.strip():
                with open(filepath, 'rb') as f:
                    pdf_bytes = f.read()
                
                # Encode using standard google-genai dictionary syntax structure
                b64_data = base64.b64encode(pdf_bytes).decode('utf-8')
                ocr_prompt = "Perform accurate OCR transcription on these scanned handwritten note pages."
                response = ai_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[
                        {"type": "document", "data": b64_data, "mime_type": "application/pdf"},
                        {"type": "text", "text": ocr_prompt}
                    ]
                )
                extracted_text = response.text
        else:
            with open(filepath, 'rb') as f:
                img_bytes = f.read()
            
            b64_data = base64.b64encode(img_bytes).decode('utf-8')
            ocr_prompt = "Perform full digital text transcription from this photographic note document."
            response = ai_client.models.generate_content(
                model='gemini-2.5-flash',
                contents=[
                    {"type": "image", "data": b64_data, "mime_type": file.content_type},
                    {"type": "text", "text": ocr_prompt}
                ]
            )
            extracted_text = response.text

        if os.path.exists(filepath):
            os.remove(filepath)

        summary_prompt = f"""
        Analyze the following transcribed document text block carefully:
        {extracted_text}
        
        Generate a concise One-Pager SuperNote summary. Render clean structural output lines.
        Wrap important concepts or terms inside <strong> elements and format list hierarchies inside <ul><li> structures.
        Do not use markdown symbols like #, ##, or **.
        """
        summary_res = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=summary_prompt
        )

        db.session.expunge_all()

        return jsonify({
            "success": True, 
            "digitized_text": extracted_text.strip() or "No raw text segments discovered.", 
            "summary": summary_res.text
        })
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        db.session.expunge_all()
        return jsonify({"success": False, "error": str(e)}), 500

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
        safe_name = secure_filename(file.filename) or "upload.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{safe_name}")
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
    primary_model = 'gemini-2.5-flash'
    context_source = f"Text Source Material Context: {source_text[:40000]}" if source_text else f"Topic: {topic}"

    batch_max = 70
    loops_needed = math.ceil(total_q / batch_max)

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

    def generate_batch(batch_index, current_batch_target):
        prompt = f"""
        You are an elite educational testing engine. Generate a comprehensive multiple-choice evaluation quiz strictly based on the provided material.
        {context_source}
        
        Requirements:
        1. Output exactly {current_batch_target} distinct and unique questions. This is batch chunk {batch_index+1} of {loops_needed}.
        2. Difficulty setting: {difficulty} ({system_tone}).
        3. Provide a short, single-sentence indirect hint for each question.
        4. Provide a clear, maximum 2-sentence conceptual explanation details string.
        """
        response = ai_client.models.generate_content(
            model=primary_model,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=quiz_schema,
                temperature=0.4 if difficulty != "god mode" else 0.8
            )
        )
        batch_data = json.loads(response.text)
        return batch_data.get('questions', [])

    try:
        batch_targets = []
        remaining = total_q
        for i in range(loops_needed):
            current_batch_target = batch_max if i < loops_needed - 1 else remaining
            batch_targets.append(current_batch_target)
            remaining -= current_batch_target

        results_by_index = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(loops_needed, 5)) as executor:
            future_to_index = {
                executor.submit(generate_batch, i, batch_targets[i]): i
                for i in range(loops_needed)
            }
            for future in concurrent.futures.as_completed(future_to_index):
                idx = future_to_index[future]
                results_by_index[idx] = future.result()

        all_generated_questions = []
        for i in range(loops_needed):
            all_generated_questions.extend(results_by_index[i])

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
        return jsonify({"error": f"Framework Failure: {str(e)}"}), 500

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
    if session_instance.user_id != current_user.id:
        return jsonify({"error": "Not authorized"}), 403
    
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
            explanations_map[q.id] = {"correct": q.correct_option, "explanation": q.explanation}
            
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

@app.route('/api/quiz/<int:session_id>/submit', methods=['POST'])
@login_required
def submit_quiz(session_id):
    session_instance = QuizSession.query.get_or_404(session_id)
    if session_instance.user_id != current_user.id:
        return jsonify({"error": "Not authorized"}), 403
        
    data = request.json.get('answers', {})
    score = 0
    for q in session_instance.questions:
        user_ans = data.get(str(q.id))
        user_ans_int = int(user_ans) if user_ans is not None else None
        q.user_answer = user_ans_int
        if user_ans_int == q.correct_option:
            score += 1
            
    session_instance.score = score
    session_instance.is_completed = True
    session_instance.recommendation = "Review completed targets to fortify foundational metrics."
    db.session.commit()
    
    return jsonify({"score": score, "total": session_instance.total_questions, "recommendation": session_instance.recommendation})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true")