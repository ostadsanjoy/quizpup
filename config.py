import os
from datetime import timedelta

IS_PRODUCTION = os.environ.get('FLASK_ENV') == 'production' or os.environ.get('RENDER') is not None


def resolve_secret_key():
    secret_key = os.environ.get('SECRET_KEY')
    if not secret_key:
        if IS_PRODUCTION:
            raise RuntimeError(
                "SECRET_KEY environment variable is not set. Refusing to start in "
                "production with an insecure fallback key. Set SECRET_KEY to a long "
                "random value (e.g. `python -c \"import secrets; print(secrets.token_hex(32))\"`)."
            )
        print("--- WARNING: SECRET_KEY is not set. Using an insecure development-only "
              "fallback. This is only acceptable for local dev. ---")
    return secret_key or 'dev-secret-key-change-this-in-production'


class Config:
    SECRET_KEY = resolve_secret_key()
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///quiz_saas.db')
    if SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 60 * 1024 * 1024
    REMEMBER_COOKIE_DURATION = timedelta(days=30)
    PERMANENT_SESSION_LIFETIME = timedelta(days=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = IS_PRODUCTION
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_SECURE = IS_PRODUCTION
    RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')