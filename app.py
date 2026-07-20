import os
import io
import time
import json
import math
import re
import random
import logging
import secrets
import threading
import uuid
import hmac
import requests
import base64
import concurrent.futures
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, make_response, send_file, g
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException
from pypdf import PdfReader, PdfWriter
from fpdf import FPDF
from html import escape
from google import genai
from google.genai import types
from supabase import create_client, Client
from flashcard_data import PRELOADED_DECKS
import filetype

from sqlalchemy import inspect, text
from models import db, User, QuizSession, QuizQuestion, SuperNote, FlashcardDeck

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("quizpup")

app = Flask(__name__)

IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RENDER') is not None

if IS_PRODUCTION:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

_secret_key_env = os.environ.get('SECRET_KEY')
if not _secret_key_env:
    if IS_PRODUCTION:
        raise RuntimeError(
            "SECRET_KEY environment variable is not set. Refusing to start in "
            "production with an insecure fallback key. Set SECRET_KEY to a long "
            "random value (e.g. `python -c \"import secrets; print(secrets.token_hex(32))\"`)."
        )
    print("--- WARNING: SECRET_KEY is not set. Using an insecure development-only "
          "fallback. This is only acceptable for local dev. ---")
app.config['SECRET_KEY'] = _secret_key_env or 'dev-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///quiz_saas.db')
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].replace("postgres://", "postgresql://", 1)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 60 * 1024 * 1024
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=30)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = IS_PRODUCTION
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'
app.config['REMEMBER_COOKIE_SECURE'] = IS_PRODUCTION

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_NOTE_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.webp'}
ALLOWED_NOTE_KINDS = {'pdf', 'jpg', 'jpeg', 'png', 'webp'}

def is_allowed_upload_content(filepath, expect_pdf):
    kind = filetype.guess(filepath)
    if kind is None:
        return False
    if kind.extension not in ALLOWED_NOTE_KINDS:
        return False
    if expect_pdf and kind.extension != 'pdf':
        return False
    if not expect_pdf and kind.extension == 'pdf':
        return False
    return True

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)

RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
if RATELIMIT_STORAGE_URI == 'memory://' and IS_PRODUCTION:
    print("--- WARNING: Rate limiting is using in-process memory storage in "
          "production. If Gunicorn runs more than one worker, set "
          "RATELIMIT_STORAGE_URI to a shared Redis instance or these limits "
          "are effectively multiplied by the worker count. ---")

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    storage_uri=RATELIMIT_STORAGE_URI,
    default_limits=["200 per hour"],
    headers_enabled=True,
)

@app.before_request
def _set_csp_nonce():
    g.csp_nonce = secrets.token_urlsafe(16)

@app.context_processor
def _inject_csp_nonce():
    return {"csp_nonce": lambda: g.csp_nonce}

@app.after_request
def set_security_headers(response):
    nonce = getattr(g, 'csp_nonce', '')
    csp = (
        "default-src 'self'; "
        f"script-src 'self' 'nonce-{nonce}' https://cdn.jsdelivr.net; "
        "script-src-attr 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "font-src 'self' data: https://cdn.jsdelivr.net; "
        "img-src 'self' data: blob:; "
        "connect-src 'self'; "
        "frame-ancestors 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "object-src 'none'"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), payment=()'
    response.headers['Content-Security-Policy'] = csp
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin'
    if IS_PRODUCTION:
        response.headers['Strict-Transport-Security'] = 'max-age=63072000; includeSubDomains; preload'
    return response

@login_manager.unauthorized_handler
def handle_unauthorized():
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "error": "Session expired or not logged in. Please refresh and log in again."}), 401
    return redirect(url_for('login'))

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_ACTUAL_GEMINI_API_KEY_HERE")
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# ==========================================
#          AI MODEL TIER SELECTION
# ==========================================
MODEL_LITE = 'gemini-3.1-flash-lite'
MODEL_HEAVY = 'gemini-2.5-flash'

HEAVY_TEXT_CHAR_THRESHOLD = 15000

def pick_model(is_hardest=False, char_count=0):
    if is_hardest:
        return MODEL_HEAVY
    if char_count and char_count > HEAVY_TEXT_CHAR_THRESHOLD:
        return MODEL_HEAVY
    return MODEL_LITE

GEMINI_RPM_TARGET = 10

_gemini_window_lock = threading.Lock()
_gemini_window_start = [time.monotonic()]
_gemini_window_count = [0]

def _wait_for_rate_slot():
    while True:
        with _gemini_window_lock:
            now = time.monotonic()
            elapsed = now - _gemini_window_start[0]
            if elapsed >= 60:
                _gemini_window_start[0] = now
                _gemini_window_count[0] = 0
                elapsed = 0
            if _gemini_window_count[0] < GEMINI_RPM_TARGET:
                _gemini_window_count[0] += 1
                return
            sleep_time = 60 - elapsed
        time.sleep(sleep_time)

def call_gemini(**kwargs):
    last_error = None
    for attempt in range(3):
        _wait_for_rate_slot()
        try:
            return ai_client.models.generate_content(**kwargs)
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                last_error = e
                time.sleep(15 * (attempt + 1))
                continue
            raise
    raise last_error

SUPERNOTE_CHUNK_CHAR_LIMIT = 8000
CHAPTER_HEADING_PATTERN = re.compile(r'(?im)^\s*(chapter|part|unit)\s+([0-9]+|[ivxlcdm]+)\b.*$')

def split_into_segments(text, max_chars=SUPERNOTE_CHUNK_CHAR_LIMIT):
    matches = list(CHAPTER_HEADING_PATTERN.finditer(text))
    segments = []

    if len(matches) >= 2:
        for i, m in enumerate(matches):
            start = m.start()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            segments.append((m.group().strip(), text[start:end]))
    else:
        segments = [(None, text)]

    final_segments = []
    for label, content in segments:
        if len(content) <= max_chars:
            final_segments.append((label, content))
            continue
        n_parts = math.ceil(len(content) / max_chars)
        part_size = math.ceil(len(content) / n_parts)
        for i in range(n_parts):
            part = content[i * part_size: (i + 1) * part_size]
            part_label = f"{label} (Part {i + 1})" if label else f"Part {i + 1}"
            final_segments.append((part_label, part))

    return final_segments

SUMMARY_SCHEMA = types.Schema(
    type=types.Type.OBJECT,
    properties={
        "topics": types.Schema(
            type=types.Type.ARRAY,
            items=types.Schema(
                type=types.Type.OBJECT,
                properties={
                    "heading": types.Schema(type=types.Type.STRING),
                    "bullets": types.Schema(
                        type=types.Type.ARRAY,
                        items=types.Schema(type=types.Type.STRING)
                    )
                },
                required=["heading", "bullets"]
            )
        )
    },
    required=["topics"]
)

def summarize_segment(label, content, retry_tokens=None):
    source_words = len(content.split())
    target_words = max(35, round(source_words * 0.175))
    prompt = f"""
    Create concise study notes from the text segment below. Identify only the
    MOST IMPORTANT topics covered — this is a compressed study aid, not a full
    rewrite, so skip minor or repetitive details entirely if needed.

    Text segment:
    {content}

    Strict rules:
    1. The combined bullets across all topics must total approximately
       {target_words} words — roughly 15-20% of the source length. Do not pad
       or significantly exceed this.
    2. Give each distinct topic you keep a short heading, with a tight list of
       bullets, each bullet under 15 words.
    3. Include only the highest-yield concepts, definitions, formulas, and facts.
       Do not restate the source verbatim, include examples/filler, or repeat points.
    """
    # Content with many short, distinct topics (e.g. a cheatsheet-style list)
    # needs a token budget driven by topic count/JSON overhead, not just word
    # count — so this floor is generous rather than tightly coupled to target_words.
    token_budget = retry_tokens or max(2000, target_words * 6)

    response = call_gemini(
        model=pick_model(),
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=SUMMARY_SCHEMA,
            max_output_tokens=token_budget
        )
    )

    finish_reason = None
    if response.candidates:
        finish_reason = str(response.candidates[0].finish_reason)

    if "MAX_TOKENS" in (finish_reason or "") and retry_tokens is None:
        # Response got cut off mid-generation — retry once with double the budget
        # instead of silently accepting truncated/incomplete JSON.
        return summarize_segment(label, content, retry_tokens=token_budget * 2)

    parsed = json.loads(response.text)
    return {"chapter": label, "topics": parsed.get("topics", [])}

def batch_ocr_pdf(filepath, page_count, batch_size=15):
    reader = PdfReader(filepath)
    batch_ranges = [(start, min(start + batch_size, page_count)) for start in range(0, page_count, batch_size)]

    # Pre-extract each batch's bytes sequentially first — pypdf isn't guaranteed
    # thread-safe, so no concurrent access to the shared reader/writer objects.
    batch_byte_chunks = []
    for start, end in batch_ranges:
        writer = PdfWriter()
        for i in range(start, end):
            writer.add_page(reader.pages[i])
        buffer = io.BytesIO()
        writer.write(buffer)
        batch_byte_chunks.append(buffer.getvalue())

    def ocr_one_batch(idx, start, end):
        ocr_prompt = f"Perform accurate OCR transcription on these scanned handwritten note pages (pages {start+1}-{end})."
        response = call_gemini(
            model=pick_model(),
            contents=[
                types.Part.from_bytes(data=batch_byte_chunks[idx], mime_type="application/pdf"),
                ocr_prompt
            ]
        )
        return response.text

    results_by_index = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(batch_ranges), GEMINI_RPM_TARGET)) as executor:
        future_to_index = {
            executor.submit(ocr_one_batch, idx, start, end): idx
            for idx, (start, end) in enumerate(batch_ranges)
        }
        for future in concurrent.futures.as_completed(future_to_index):
            idx = future_to_index[future]
            results_by_index[idx] = future.result()

    return "\n\n".join(results_by_index[i] for i in range(len(batch_ranges)))

def render_summary_html(structured_summary):
    parts = []
    for chapter in structured_summary:
        if chapter.get("chapter"):
            parts.append(f"<h4>{escape(chapter['chapter'])}</h4>")
        for topic in chapter.get("topics", []):
            if topic.get("heading"):
                parts.append(f"<strong>{escape(topic['heading'])}</strong>")
            bullets_html = "".join(f"<li>{escape(b)}</li>" for b in topic.get("bullets", []))
            parts.append(f"<ul>{bullets_html}</ul>")
    return "\n".join(parts)

FONT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "fonts")

def generate_pdf_bytes(title, structured_summary):
    pdf = FPDF(format="A4")
    pdf.add_font("DejaVu", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
    pdf.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(True, margin=15)
    pdf.add_page()

    pdf.set_font("DejaVu", "B", 15)
    pdf.multi_cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_draw_color(180, 146, 134)
    pdf.line(15, pdf.get_y(), pdf.w - 15, pdf.get_y())
    pdf.ln(3)

    with pdf.text_columns(ncols=2, gutter=8, text_align="LEFT", line_height=1.2) as cols:
        for chapter in structured_summary:
            if chapter.get("chapter"):
                pdf.set_font("DejaVu", "B", 9.5)
                cols.write(text=f"{chapter['chapter']}\n")
            for topic in chapter.get("topics", []):
                if topic.get("heading"):
                    pdf.set_font("DejaVu", "B", 8)
                    cols.write(text=f"{topic['heading']}\n")
                pdf.set_font("DejaVu", "", 7.5)
                for bullet in topic.get("bullets", []):
                    with cols.paragraph(bullet_string="\u2022", indent=4, bottom_margin=1) as par:
                        par.write(bullet)

    return bytes(pdf.output())

download_token_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def generate_download_token(note_id, user_id):
    return download_token_serializer.dumps({"note_id": note_id, "user_id": user_id})

def verify_download_token(token, note_id):
    try:
        data = download_token_serializer.loads(token, max_age=300)
    except (BadSignature, SignatureExpired):
        return None
    if data.get("note_id") != note_id:
        return None
    return data.get("user_id")

SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase_client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.environ.get("BREVO_SENDER_EMAIL")
MAIL_FROM_NAME = "QuizPup"

OTP_VALID_MINUTES = 10
OTP_MAX_ATTEMPTS = 5

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

def send_email(target_email, subject, html_body):
    if not BREVO_API_KEY or not BREVO_SENDER_EMAIL:
        logger.error("BREVO_API_KEY or BREVO_SENDER_EMAIL environment variable is missing!")
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

PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$')
PASSWORD_REQUIREMENTS_MESSAGE = (
    "Password must be at least 8 characters and include at least one letter, "
    "one number, and one special character."
)

def is_password_strong(password):
    return bool(password) and bool(PASSWORD_PATTERN.match(password))

def otp_matches(submitted, expected):
    if not submitted or not expected:
        return False
    return hmac.compare_digest(str(submitted), str(expected))

def clear_email_change_state(user):
    user.pending_email = None
    user.email_change_otp = None
    user.email_change_otp_expires = None
    user.email_change_stage = None
    user.email_change_attempts = 0

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
@limiter.limit("10 per hour")
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

        if not is_password_strong(password):
            flash(PASSWORD_REQUIREMENTS_MESSAGE, 'danger')
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
            logger.warning("Supabase sign_up notice: %s", str(e))

        session['pending_verification_user_id'] = new_user.id

        if send_verification_email(email, otp_code):
            flash('Account created! Check your email for a 6-digit verification code.', 'success')
        else:
            flash('Account created, but we could not send the verification email right now. Tap "Resend code" on the next screen to try again.', 'warning')

        return redirect(url_for('verify_email'))

    return render_template('login.html', action="Register")

@app.route('/verify-email', methods=['GET', 'POST'])
@limiter.limit("15 per hour")
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
            if otp_matches(submitted_otp, user.verification_otp):
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
@limiter.limit("5 per hour")
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
@limiter.limit("10 per minute; 50 per hour")
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
                logger.warning("Supabase sign_in notice: %s", str(sb_err))

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

@app.route('/ping', methods=['GET'])
@limiter.exempt
def ping_server():
    return jsonify({"status": "healthy", "message": "Stay awake, pup!"}), 200

# ==========================================
#          PASSWORD RECOVERY ROUTES
# ==========================================

@app.route('/forgot-username', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
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
@limiter.limit("5 per hour")
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if user:
            otp_code = generate_otp()
            user.verification_otp = otp_code
            user.verification_otp_expires = datetime.utcnow() + timedelta(minutes=OTP_VALID_MINUTES)
            user.password_reset_attempts = 0
            db.session.commit()
            send_otp_email(email, otp_code)

        # Always show the same message and proceed to the same next step,
        # regardless of whether the account exists — otherwise this endpoint
        # can be used to enumerate which emails have registered accounts.
        session['reset_password_email'] = email
        flash('If an account exists for that email address, a verification code has been sent.', 'success')
        return redirect(url_for('verify_otp'))

    return render_template('forgot_password.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
@limiter.limit("15 per hour")
def verify_otp():
    email = session.get('reset_password_email')
    if not email:
        return redirect(url_for('forgot_password'))

    user = User.query.filter_by(email=email).first()

    if request.method == 'POST':
        submitted_otp = request.form.get('otp')
        new_password = request.form.get('new_password')

        if not submitted_otp or not new_password:
            flash('Both the verification code and chosen password fields are required.', 'danger')
            return render_template('verify_otp.html', email=email)

        if not is_password_strong(new_password):
            flash(PASSWORD_REQUIREMENTS_MESSAGE, 'danger')
            return render_template('verify_otp.html', email=email)

        # No matching account — show the same generic error as a wrong code,
        # never reveal that the account doesn't exist.
        if not user:
            flash('Invalid or expired recovery code.', 'danger')
            return render_template('verify_otp.html', email=email)

        expired = (not user.verification_otp_expires) or datetime.utcnow() > user.verification_otp_expires
        if expired:
            flash('Your verification code expired. Please request a new one.', 'danger')
        elif user.password_reset_attempts >= OTP_MAX_ATTEMPTS:
            flash('Too many incorrect attempts. Please request a new code.', 'danger')
        elif otp_matches(submitted_otp, user.verification_otp):
            user.password_hash = generate_password_hash(new_password, method='scrypt')
            user.verification_otp = None
            user.verification_otp_expires = None
            user.password_reset_attempts = 0
            db.session.commit()

            session.pop('reset_password_email', None)
            flash('Your account security password has been updated successfully. Please login.', 'success')
            return redirect(url_for('login'))
        else:
            user.password_reset_attempts += 1
            db.session.commit()
            flash('Invalid or expired recovery code.', 'danger')

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

@app.route('/profile/edit', methods=['GET'])
@login_required
def edit_profile_page():
    return render_template('dashboard.html', view="edit_profile")

@app.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    first_name = (request.form.get('first_name') or '').strip()[:100]
    last_name = (request.form.get('last_name') or '').strip()[:100]
    phone = (request.form.get('phone') or '').strip()[:20]

    if not first_name or not last_name:
        flash('First and last name are required.', 'danger')
        return redirect(url_for('edit_profile_page'))

    current_user.first_name = first_name
    current_user.last_name = last_name
    current_user.phone = phone
    db.session.commit()
    flash('Your details have been updated.', 'success')
    return redirect(url_for('profile'))

@app.route('/profile/email/request-change', methods=['POST'])
@login_required
@limiter.limit("5 per hour")
def request_email_change():
    new_email = (request.form.get('new_email') or '').strip().lower()

    if not new_email or '@' not in new_email:
        flash('Please enter a valid email address.', 'danger')
        return redirect(url_for('edit_profile_page'))

    if new_email == (current_user.email or '').lower():
        flash('That is already your current email address.', 'danger')
        return redirect(url_for('edit_profile_page'))

    if User.query.filter(User.email.ilike(new_email)).first():
        flash('That email address is already in use by another account.', 'danger')
        return redirect(url_for('edit_profile_page'))

    otp_code = generate_otp()
    current_user.pending_email = new_email
    current_user.email_change_otp = otp_code
    current_user.email_change_otp_expires = datetime.utcnow() + timedelta(minutes=OTP_VALID_MINUTES)
    current_user.email_change_stage = 'verify_current'
    current_user.email_change_attempts = 0
    db.session.commit()

    send_email(
        current_user.email,
        "Confirm your QuizPup email change",
        f"<p>We received a request to change the email on your QuizPup account to "
        f"<strong>{escape(new_email)}</strong>.</p>"
        f"<p>Your confirmation code is: <strong>{otp_code}</strong></p>"
        f"<p>If you didn't request this, you can safely ignore this email — your "
        f"address won't change without this code.</p>"
    )
    flash(f'A confirmation code has been sent to your current email ({current_user.email}).', 'success')
    return redirect(url_for('edit_profile_page'))

@app.route('/profile/email/verify', methods=['POST'])
@login_required
@limiter.limit("15 per hour")
def verify_email_change():
    submitted_otp = request.form.get('otp')

    if not current_user.pending_email or not current_user.email_change_stage:
        flash('No pending email change found.', 'danger')
        return redirect(url_for('edit_profile_page'))

    expired = (not current_user.email_change_otp_expires) or datetime.utcnow() > current_user.email_change_otp_expires
    if expired:
        flash('That code has expired. Please start the email change again.', 'danger')
        clear_email_change_state(current_user)
        db.session.commit()
        return redirect(url_for('edit_profile_page'))

    if current_user.email_change_attempts >= OTP_MAX_ATTEMPTS:
        flash('Too many incorrect attempts. Please start the email change again.', 'danger')
        clear_email_change_state(current_user)
        db.session.commit()
        return redirect(url_for('edit_profile_page'))

    if not otp_matches(submitted_otp, current_user.email_change_otp):
        current_user.email_change_attempts += 1
        db.session.commit()
        flash('Incorrect code. Please try again.', 'danger')
        return redirect(url_for('edit_profile_page'))

    if current_user.email_change_stage == 'verify_current':
        # Current email confirmed — now verify ownership of the new address
        otp_code = generate_otp()
        current_user.email_change_otp = otp_code
        current_user.email_change_otp_expires = datetime.utcnow() + timedelta(minutes=OTP_VALID_MINUTES)
        current_user.email_change_stage = 'verify_new'
        current_user.email_change_attempts = 0
        db.session.commit()

        send_email(
            current_user.pending_email,
            "Verify your new QuizPup email address",
            f"<p>Your verification code to confirm this as your new QuizPup email "
            f"address is: <strong>{otp_code}</strong></p>"
        )
        flash(f'Confirmed. A verification code has been sent to your new email ({current_user.pending_email}).', 'success')
        return redirect(url_for('edit_profile_page'))

    elif current_user.email_change_stage == 'verify_new':
        # Guard against the address being claimed by someone else mid-flow
        if User.query.filter(User.email.ilike(current_user.pending_email), User.id != current_user.id).first():
            flash('That email address was just claimed by another account. Please try a different address.', 'danger')
            clear_email_change_state(current_user)
            db.session.commit()
            return redirect(url_for('edit_profile_page'))

        current_user.email = current_user.pending_email
        clear_email_change_state(current_user)
        db.session.commit()
        flash('Your email address has been updated successfully.', 'success')
        return redirect(url_for('profile'))

    return redirect(url_for('edit_profile_page'))

@app.route('/profile/email/cancel', methods=['POST'])
@login_required
def cancel_email_change():
    clear_email_change_state(current_user)
    db.session.commit()
    flash('Email change cancelled.', 'success')
    return redirect(url_for('edit_profile_page'))

# ==========================================
#        NEW FLASHCARD & STUDY ASYNC APIs
# ==========================================

@app.route('/api/flashcards/structure', methods=['GET'])
@login_required
def flashcards_structure():
    exam_target = request.args.get('exam', 'JEE').upper()
    exam_data = PRELOADED_DECKS.get(exam_target, {})

    structure = {}
    for subject, chapters in exam_data.items():
        structure[subject] = [
            {"chapter": chapter_name, "count": len(cards)}
            for chapter_name, cards in chapters.items()
        ]

    return jsonify({"success": True, "exam": exam_target, "subjects": structure})

@app.route('/api/flashcards/preload', methods=['GET'])
@login_required
def preload_flashcards():
    exam_target = request.args.get('exam', 'JEE').upper()
    subject_target = request.args.get('subject', '')
    chapter_target = request.args.get('chapter', '')

    exam_data = PRELOADED_DECKS.get(exam_target, {})
    subject_data = exam_data.get(subject_target, {})
    chapter_deck = subject_data.get(chapter_target, [])

    return jsonify({"success": True, "deck": chapter_deck})

@app.route('/api/flashcards/generate', methods=['POST'])
@login_required
@limiter.limit("20 per hour")
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

    prompt = f"Create 15 - 25 revision flashcards matching the core and most important concepts in the parameter topic context: '{topic}'. Keep answers within 3 lines."
    try:
        response = call_gemini(
            model=pick_model(),
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=fc_schema,
                temperature=0.5
            )
        )
        res_data = json.loads(response.text)
        cards = res_data.get('cards', [])

        saved_deck = FlashcardDeck(
            user_id=current_user.id,
            topic=topic,
            cards_json=json.dumps(cards)
        )
        db.session.add(saved_deck)
        db.session.commit()

        return jsonify({"success": True, "deck": cards, "deck_id": saved_deck.id})
    except Exception as e:
        logger.exception("AI flashcard generation failed for user %s", current_user.id)
        return jsonify({"success": False, "error": "Could not generate flashcards right now. Please try again shortly."}), 500

@app.route('/api/flashcards/my-decks', methods=['GET'])
@login_required
def my_flashcard_decks():
    decks = FlashcardDeck.query.filter_by(user_id=current_user.id).order_by(FlashcardDeck.created_at.desc()).all()
    return jsonify({
        "success": True,
        "decks": [
            {
                "id": d.id,
                "topic": d.topic,
                "count": len(json.loads(d.cards_json)),
                "created_at": d.created_at.strftime('%b %d, %Y') if d.created_at else ""
            }
            for d in decks
        ]
    })

@app.route('/api/flashcards/my-decks/<int:deck_id>', methods=['GET'])
@login_required
def get_flashcard_deck(deck_id):
    deck = FlashcardDeck.query.filter_by(id=deck_id, user_id=current_user.id).first()
    if not deck:
        return jsonify({"success": False, "error": "Deck not found."}), 404
    return jsonify({"success": True, "topic": deck.topic, "deck": json.loads(deck.cards_json)})

def run_supernotes_job(app_instance, note_id, filepath, filename, is_pdf, file_mime_type):
    with app_instance.app_context():
        note = SuperNote.query.get(note_id)
        try:
            extracted_text = ""

            if is_pdf:
                reader = PdfReader(filepath)
                for page in reader.pages:
                    extracted_text += page.extract_text() or ""

                page_count = len(reader.pages)
                avg_chars_per_page = len(extracted_text.strip()) / max(page_count, 1)
                # Low density per page means it's likely scanned/handwritten
                looks_scanned = avg_chars_per_page < 40

                if looks_scanned:
                    extracted_text = batch_ocr_pdf(filepath, page_count)
            else:
                with open(filepath, 'rb') as f:
                    img_bytes = f.read()

                ocr_prompt = "Perform full digital text transcription from this photographic note document."
                response = call_gemini(
                    model=pick_model(),
                    contents=[
                        types.Part.from_bytes(data=img_bytes, mime_type=file_mime_type or "image/jpeg"),
                        ocr_prompt
                    ]
                )
                extracted_text = response.text

            if os.path.exists(filepath):
                os.remove(filepath)

            segments = split_into_segments(extracted_text)
            summary_results = {}
            with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(segments), GEMINI_RPM_TARGET)) as executor:
                future_to_index = {
                    executor.submit(summarize_segment, label, content): idx
                    for idx, (label, content) in enumerate(segments)
                }
                for future in concurrent.futures.as_completed(future_to_index):
                    idx = future_to_index[future]
                    summary_results[idx] = future.result()
            structured_summary = [summary_results[i] for i in range(len(segments))]

            full_summary = render_summary_html(structured_summary)
            pdf_bytes = generate_pdf_bytes(note.title, structured_summary)

            note.digitized_text = extracted_text.strip()
            note.summary_html = full_summary
            note.pdf_data = pdf_bytes
            note.status = "complete"
            db.session.commit()
        except Exception as e:
            logger.exception("SuperNotes job failed for note %s", note_id)
            if os.path.exists(filepath):
                os.remove(filepath)
            note.status = "failed"
            note.error_message = "We couldn't process this file. Please try a clearer scan or a different file."
            db.session.commit()

@app.route('/api/study/process-notes', methods=['POST'])
@login_required
@limiter.limit("15 per hour")
def process_study_notes():
    if 'note_file' not in request.files:
        return jsonify({"success": False, "error": "Payload key mismatch."}), 400
    
    file = request.files['note_file']
    if file.filename == '':
        return jsonify({"success": False, "error": "Empty filename."}), 400

    filename = secure_filename(file.filename)
    if not filename.lower().endswith(tuple(ALLOWED_NOTE_EXTENSIONS)):
        return jsonify({"success": False, "error": "Unsupported file type. Please upload a PDF, JPG, PNG, or WEBP file."}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{filename}")
    is_pdf = filename.lower().endswith('.pdf')
    file_mime_type = file.content_type

    try:
        file.save(filepath)
    except Exception as e:
        logger.exception("Failed to save uploaded note file")
        return jsonify({"success": False, "error": "Could not save the uploaded file. Please try again."}), 500

    if not is_allowed_upload_content(filepath, is_pdf):
        os.remove(filepath)
        return jsonify({"success": False, "error": "That file's contents don't match a supported PDF or image format."}), 400

    note_title = os.path.splitext(filename)[0].replace('_', ' ').replace('-', ' ').strip() or "Untitled Note"
    note = SuperNote(user_id=current_user.id, title=note_title, status="processing")
    db.session.add(note)
    db.session.commit()
    note_id = note.id

    threading.Thread(
        target=run_supernotes_job,
        args=(app, note_id, filepath, filename, is_pdf, file_mime_type),
        daemon=True
    ).start()

    return jsonify({
        "success": True,
        "note_id": note_id,
        "title": note_title,
        "status": "processing"
    })

@app.route('/api/study/notes/history', methods=['GET'])
@login_required
def supernotes_history():
    notes = SuperNote.query.filter_by(user_id=current_user.id).order_by(SuperNote.created_at.desc()).all()
    return jsonify({
        "success": True,
        "notes": [
            {"id": n.id, "title": n.title, "status": n.status, "created_at": n.created_at.isoformat()}
            for n in notes
        ]
    })

@app.route('/api/study/notes/<int:note_id>/status', methods=['GET'])
@login_required
def supernotes_status(note_id):
    note = SuperNote.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({"success": False, "error": "Note not found."}), 404
    return jsonify({"success": True, "status": note.status, "error": note.error_message})

@app.route('/api/study/notes/<int:note_id>', methods=['GET'])
@login_required
def supernotes_view(note_id):
    note = SuperNote.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note:
        return jsonify({"success": False, "error": "Note not found."}), 404
    return jsonify({
        "success": True,
        "title": note.title,
        "status": note.status,
        "error": note.error_message,
        "digitized_text": note.digitized_text,
        "summary": note.summary_html,
        "created_at": note.created_at.isoformat()
    })

@app.route('/api/study/notes/<int:note_id>/download-token', methods=['GET'])
@login_required
def supernotes_download_token(note_id):
    note = SuperNote.query.filter_by(id=note_id, user_id=current_user.id).first()
    if not note or note.status != "complete":
        return jsonify({"success": False, "error": "Note not found or not ready yet."}), 404
    token = generate_download_token(note_id, current_user.id)
    return jsonify({"success": True, "url": f"/api/study/notes/{note_id}/pdf?token={token}"})

@app.route('/api/study/notes/<int:note_id>/pdf', methods=['GET'])
def supernotes_download(note_id):
    token = request.args.get('token')
    if token:
        owner_id = verify_download_token(token, note_id)
        if owner_id is None:
            return jsonify({"success": False, "error": "This download link has expired. Please try downloading again."}), 401
    elif current_user.is_authenticated:
        owner_id = current_user.id
    else:
        return jsonify({"success": False, "error": "Session expired or not logged in. Please refresh and log in again."}), 401

    note = SuperNote.query.filter_by(id=note_id, user_id=owner_id).first()
    if not note or note.status != "complete":
        return jsonify({"success": False, "error": "Note not found or not ready yet."}), 404
    safe_name = secure_filename(note.title) or "supernote"
    return send_file(
        io.BytesIO(note.pdf_data),
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f"{safe_name}.pdf"
    )

# ==========================================
#          CORE ENGINE & AI LOGIC
# ==========================================

@app.route('/generate-quiz', methods=['POST'])
@login_required
@limiter.limit("20 per hour")
def generate_quiz():
    topic = request.form.get('topic')
    difficulty = request.form.get('difficulty', 'easy')
    try:
        total_q = int(request.form.get('total_questions', 10))
        duration = int(request.form.get('duration', 10))
    except (TypeError, ValueError):
        return jsonify({"error": "Questions and duration must be numbers."}), 400

    if total_q < 10 or total_q > 200:
        return jsonify({"error": "Questions must stay between 10 and 200 items."}), 400
    if duration < 1 or duration > 300:
        return jsonify({"error": "Duration must be between 1 and 300 minutes."}), 400

    source_text = ""
    if 'pdf_file' in request.files and request.files['pdf_file'].filename != '':
        file = request.files['pdf_file']
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({"error": "Please upload a PDF file."}), 400
        safe_name = secure_filename(file.filename) or "upload.pdf"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4().hex}_{safe_name}")
        file.save(filepath)
        if not is_allowed_upload_content(filepath, expect_pdf=True):
            os.remove(filepath)
            return jsonify({"error": "That file's contents don't match a valid PDF."}), 400
        try:
            reader = PdfReader(filepath)
            for page in reader.pages:
                source_text += page.extract_text() or ""
            os.remove(filepath)
        except Exception as e:
            logger.exception("Failed to parse uploaded quiz-source PDF")
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({"error": "Could not read that PDF. Please try a different file."}), 400

    if difficulty == 'easy':
        hints_allowed = -1
    elif difficulty == 'medium':
        hints_allowed = math.floor(total_q * 0.3)
    else:
        hints_allowed = 0

    system_tone = "highly complex, rigorous, and university-level" if difficulty == "god mode" else "standard academic evaluation"
    primary_model = pick_model(is_hardest=(difficulty == "god mode"), char_count=len(source_text))
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
        response = call_gemini(
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
        logger.exception("Quiz generation failed for user %s", current_user.id)
        return jsonify({"error": "Could not generate the quiz right now. Please try again shortly."}), 500

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

def sync_missing_columns():
    inspector = inspect(db.engine)
    existing_tables = set(inspector.get_table_names())
    for mapper in db.Model.registry.mappers:
        table = mapper.local_table
        if table is None or table.name not in existing_tables:
            continue
        existing_cols = {col['name'] for col in inspector.get_columns(table.name)}
        for column in table.columns:
            if column.name in existing_cols:
                continue
            col_type = column.type.compile(dialect=db.engine.dialect)
            with db.engine.connect() as conn:
                conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{column.name}" {col_type}'))
                conn.commit()

with app.app_context():
    db.create_all()
    sync_missing_columns()

@app.errorhandler(413)
def handle_file_too_large(e):
    max_mb = app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)
    message = f"That file is too large. The maximum upload size is {max_mb}MB — try a lower-resolution scan or split the document into smaller parts."
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "error": message}), 413
    return message, 413

@app.errorhandler(429)
def handle_rate_limit(e):
    message = "You're doing that a bit too fast — please wait a moment and try again."
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "error": message}), 429
    flash(message, 'error')
    return redirect(request.referrer or url_for('home'))

@app.errorhandler(Exception)
def handle_uncaught_exception(e):
    if isinstance(e, HTTPException):
        if request.path.startswith('/api/'):
            return jsonify({"success": False, "error": e.description}), e.code
        return e
    logger.exception("Unhandled exception on %s", request.path)
    if request.path.startswith('/api/'):
        return jsonify({"success": False, "error": "An unexpected server error occurred. Please try again."}), 500
    raise e

if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    if debug_mode and IS_PRODUCTION:
        raise RuntimeError("FLASK_DEBUG=true is not allowed when running in production.")
    app.run(debug=debug_mode)