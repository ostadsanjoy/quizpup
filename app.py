import os
import json
import math
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from pypdf import PdfReader
from google import genai
from google.genai import types

from models import db, User, QuizSession, QuizQuestion

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quiz_saas.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['UPLOAD_FOLDER'] = 'uploads'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Global key configuration
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_GEMINI_API_KEY_HERE")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==========================================
#          AUTHENTICATION ROUTES
# ==========================================

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
            flash('Username already exists.')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password, method='scrypt')
        new_user = User(
            username=username, 
            password_hash=hashed_pw, 
            first_name=first_name,
            last_name=last_name,
            email=email if email else None, 
            phone=phone
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('login.html', action="Register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid credentials.')
    return render_template('login.html', action="Login")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# ==========================================
#       WIREFRAME DASHBOARD PANELS
# ==========================================

@app.route('/')
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
    
    # Intelligent Model Routing & Context Extraction
    if source_text:
        primary_model = 'gemini-2.5-flash'
        context_source = f"Text Source Material Context: {source_text[:40000]}"
        print(f"Routing session to Heavy Engine ({primary_model}) due to PDF attachment.")
    else:
        primary_model = 'gemini-3.1-flash-lite'
        context_source = f"Topic: {topic}"
        print(f"Routing session to High-RPD Engine ({primary_model}) for standard topic generation.")

    # ====================================================================
    # OPTIMIZED BATCHING LOGIC (70 QUESTIONS MAX PER CALL)
    # ====================================================================
    batch_max = 70
    loops_needed = math.ceil(total_q / batch_max)
    all_generated_questions = []

    # Common schema rule constraint container
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
            # Calculate exact items to pull in this dynamic run slice
            if i == loops_needed - 1:
                current_batch_target = total_q - len(all_generated_questions)
            else:
                current_batch_target = batch_max

            print(f"Executing Batch request iteration {i+1}/{loops_needed} for {current_batch_target} items...")

            # CRITICAL: We instruct the model to keep hints/explanations concise 
            # to stay safely under the 8,192 token limit for 70 items.
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

        # Enforce hard validation safety net cuts
        all_generated_questions = all_generated_questions[:total_q]

        # Save session container
        session = QuizSession(
            user_id=current_user.id,
            topic=topic if topic else "Uploaded Document Reference Workspace",
            difficulty=difficulty,
            total_questions=total_q,
            duration_minutes=duration,
            hints_remaining=hints_allowed
        )
        db.session.add(session)
        db.session.commit()

        # Commit compiled batch array to user tables
        for q in all_generated_questions:
            question_entry = QuizQuestion(
                session_id=session.id,
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

        return jsonify({"success": True, "session_id": session.id})
        
    except Exception as e:
        return jsonify({"error": f"Framework Processing Failure: {str(e)}"}), 500


# ==========================================
#          RUNNING EXAMINATION INTERFACE
# ==========================================

@app.route('/quiz/<int:session_id>')
@login_required
def run_quiz(session_id):
    session = QuizSession.query.get_or_404(session_id)
    if session.user_id != current_user.id:
        return redirect(url_for('home'))
    return render_template('quiz.html', session=session)

@app.route('/api/quiz/<int:session_id>/questions')
@login_required
def get_quiz_questions(session_id):
    session = QuizSession.query.get_or_404(session_id)
    
    questions = [{
        "id": q.id,
        "question": q.question_text,
        "1": q.option_1,
        "2": q.option_2,
        "3": q.option_3,
        "4": q.option_4
    } for q in session.questions]
    
    explanations_map = {}
    saved_answers_map = {}
    if session.is_completed:
        for q in session.questions:
            saved_answers_map[q.id] = q.user_answer
            explanations_map[q.id] = {
                "correct": q.correct_option,
                "explanation": q.explanation
            }
            
    return jsonify({
        "duration": session.duration_minutes,
        "difficulty": session.difficulty,
        "hints_remaining": session.hints_remaining,
        "is_completed": session.is_completed,
        "score": session.score,
        "total": session.total_questions,
        "recommendation": session.recommendation,
        "questions": questions,
        "saved_answers": saved_answers_map,
        "explanations": explanations_map
    })

@app.route('/api/quiz/<int:session_id>/hint/<int:question_id>', methods=['POST'])
@login_required
def fetch_hint(session_id, question_id):
    session = QuizSession.query.get_or_404(session_id)
    question = QuizQuestion.query.get_or_404(question_id)
    
    if session.difficulty in ['hard', 'god mode']:
        return jsonify({"error": f"Hints are completely locked under {session.difficulty} mode constraints."}), 403
        
    if session.difficulty == 'medium':
        if session.hints_remaining <= 0:
            return jsonify({"error": "No hint allocations remaining for this session."}), 403
        session.hints_remaining -= 1
        db.session.commit()
        
    return jsonify({"hint": question.hint, "hints_remaining": session.hints_remaining})

@app.route('/api/quiz/<int:session_id>/submit', methods=['POST'])
@login_required
def submit_quiz(session_id):
    session = QuizSession.query.get_or_404(session_id)
    if session.is_completed:
        return jsonify({"error": "Session execution loop already completed."}), 400
        
    data = request.json.get('answers', {})
    score = 0
    wrong_context = []
    explanations_map = {}

    for q in session.questions:
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
            
    session.score = score
    session.is_completed = True
    
    recommendation = "Incredible work! No visible lagging gaps discovered across the evaluated topic framework criteria."
    if wrong_context:
        rec_prompt = f"""
        A student completed a comprehensive exam focusing on domain topic matrix: '{session.topic}'.
        They missed the following evaluation conceptual targets:
        {json.dumps(wrong_context[:12])}
        
        Generate a constructive, personalized 2-3 sentence lagging evaluation critique summary pointing out exactly what sub-thematic focus point they are struggling with and where they must study next.
        """
        try:
            rec_response = ai_client.models.generate_content(model='gemini-2.5-flash', contents=rec_prompt)
            recommendation = rec_response.text
        except:
            recommendation = "Review missed baseline index properties to fortify foundational structural execution parameters."

    session.recommendation = recommendation
    db.session.commit()
    
    return jsonify({
        "score": score,
        "total": session.total_questions,
        "recommendation": recommendation,
        "explanations": explanations_map
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)