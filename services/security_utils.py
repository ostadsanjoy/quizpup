import re
import hmac
import secrets

ALLOWED_NOTE_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.webp'}

PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$')
PASSWORD_REQUIREMENTS_MESSAGE = (
    "Password must be at least 8 characters and include at least one letter, "
    "one number, and one special character."
)


def is_allowed_upload_content(filepath, expect_pdf):
    try:
        h = open(filepath, 'rb').read(12)
        return h.startswith(b'%PDF-') if expect_pdf else (
            h.startswith(b'\xff\xd8\xff') or h.startswith(b'\x89PNG\r\n\x1a\n') or (h.startswith(b'RIFF') and h[8:12] == b'WEBP')
        )
    except Exception:
        return False


def generate_otp():
    return str(secrets.randbelow(900000) + 100000)


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