from flask import Blueprint

flashcards_bp = Blueprint('flashcards', __name__)

from . import routes
