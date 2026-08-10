import logging
from flask import request, jsonify, flash, redirect, url_for
from werkzeug.exceptions import HTTPException

logger = logging.getLogger("quizpup")


def _is_api_or_ajax_request():
    return (
        request.path.startswith('/api/') or
        request.path == '/generate-quiz' or
        request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
        'application/json' in request.headers.get('Accept', '') or
        request.is_json
    )


def register_error_handlers(app):
    @app.errorhandler(413)
    def handle_file_too_large(e):
        max_mb = app.config['MAX_CONTENT_LENGTH'] // (1024 * 1024)
        message = f"That file is too large. The maximum upload size is {max_mb}MB — try a lower-resolution scan or split the document into smaller parts."
        if _is_api_or_ajax_request():
            return jsonify({"success": False, "error": message}), 413
        return message, 413

    @app.errorhandler(429)
    def handle_rate_limit(e):
        message = "You're doing that a bit too fast — please wait a moment and try again."
        if _is_api_or_ajax_request():
            return jsonify({"success": False, "error": message}), 429
        flash(message, 'error')
        return redirect(request.referrer or url_for('dashboard.home'))

    @app.errorhandler(Exception)
    def handle_uncaught_exception(e):
        if isinstance(e, HTTPException):
            if _is_api_or_ajax_request():
                return jsonify({"success": False, "error": e.description}), e.code
            return e
        logger.exception("Unhandled exception on %s", request.path)
        if _is_api_or_ajax_request():
            return jsonify({"success": False, "error": "An unexpected server error occurred. Please try again."}), 500
        raise e