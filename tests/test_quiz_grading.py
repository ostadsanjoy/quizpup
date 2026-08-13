import json
from unittest.mock import patch, MagicMock

from extensions import db
from models import QuizSession
from tests.conftest import make_user, login, make_quiz_session


SAMPLE_QUESTIONS = [
    {"question_text": "2 + 2?", "option_1": "3", "option_2": "4", "option_3": "5", "option_4": "6", "correct_option": 2},
    {"question_text": "Capital of France?", "option_1": "Rome", "option_2": "Berlin", "option_3": "Paris", "option_4": "Madrid", "correct_option": 3},
    {"question_text": "H2O is?", "option_1": "Water", "option_2": "Salt", "option_3": "Sugar", "option_4": "Oil", "correct_option": 1},
]


def _logged_in_user_and_client(client, email="quizzer@example.com"):
    user = make_user(email=email, password="Correct-Horse9!", is_verified=True)
    login(client, email, "Correct-Horse9!")
    return user


# ---------------------------------------------------------------------------
# submit_quiz — scoring correctness
# ---------------------------------------------------------------------------

def test_submit_quiz_scores_all_correct_answers(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    answers = {str(q.id): q.correct_option for q in quiz.questions}

    resp = client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": answers})

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["score"] == 3
    assert data["total"] == 3


def test_submit_quiz_scores_partial_correct_answers(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    qs = quiz.questions
    # Get exactly the first question right, the rest wrong.
    answers = {
        str(qs[0].id): qs[0].correct_option,
        str(qs[1].id): (qs[1].correct_option % 4) + 1,  # guaranteed wrong option
        str(qs[2].id): (qs[2].correct_option % 4) + 1,
    }

    resp = client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": answers})

    assert resp.get_json()["score"] == 1


def test_submit_quiz_treats_unanswered_questions_as_wrong(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    qs = quiz.questions
    # Only answer the first question; leave the rest out entirely.
    answers = {str(qs[0].id): qs[0].correct_option}

    resp = client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": answers})

    assert resp.get_json()["score"] == 1


def test_submit_quiz_does_not_crash_on_malformed_answer_values(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    qs = quiz.questions
    # Garbage/non-numeric values must be handled gracefully, not 500.
    answers = {
        str(qs[0].id): "not-a-number",
        str(qs[1].id): None,
        str(qs[2].id): qs[2].correct_option,
    }

    resp = client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": answers})

    assert resp.status_code == 200
    assert resp.get_json()["score"] == 1  # only the valid, correct one counts


def test_submit_quiz_marks_session_completed(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": {}})

    refreshed = db.session.get(QuizSession, quiz.id)
    assert refreshed.is_completed is True


def test_submit_quiz_is_idempotent_once_completed(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    qs = quiz.questions
    correct_answers = {str(q.id): q.correct_option for q in qs}

    first = client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": correct_answers})
    assert first.get_json()["score"] == 3

    # Resubmitting with all-wrong answers must NOT re-score a completed quiz.
    wrong_answers = {str(q.id): (q.correct_option % 4) + 1 for q in qs}
    second = client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": wrong_answers})

    assert second.get_json()["score"] == 3  # unchanged from the first submission


# ---------------------------------------------------------------------------
# Ownership checks — a user must never touch another user's quiz
# ---------------------------------------------------------------------------

def test_submit_quiz_rejects_other_users_session(client):
    owner = make_user(email="owner@example.com", password="Correct-Horse9!", is_verified=True)
    quiz = make_quiz_session(owner, SAMPLE_QUESTIONS)

    _logged_in_user_and_client(client, email="attacker@example.com")
    resp = client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": {}})

    assert resp.status_code == 403
    assert db.session.get(QuizSession, quiz.id).is_completed is False


def test_get_quiz_questions_rejects_other_users_session(client):
    owner = make_user(email="owner2@example.com", password="Correct-Horse9!", is_verified=True)
    quiz = make_quiz_session(owner, SAMPLE_QUESTIONS)

    _logged_in_user_and_client(client, email="attacker2@example.com")
    resp = client.get(f"/api/quiz/{quiz.id}/questions")

    assert resp.status_code == 403


def test_delete_quiz_session_rejects_other_users_session(client):
    owner = make_user(email="owner3@example.com", password="Correct-Horse9!", is_verified=True)
    quiz = make_quiz_session(owner, SAMPLE_QUESTIONS)

    _logged_in_user_and_client(client, email="attacker3@example.com")
    resp = client.delete(f"/api/quiz/{quiz.id}")

    assert resp.status_code == 403
    assert db.session.get(QuizSession, quiz.id) is not None  # not deleted


def test_quiz_endpoints_require_login(client):
    user = make_user(email="noauth@example.com", password="Correct-Horse9!", is_verified=True)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    # Deliberately not logging in.
    resp = client.get(f"/api/quiz/{quiz.id}/questions", follow_redirects=False)
    assert resp.status_code in (302, 401)  # login_manager redirects HTML, 401 for /api/*


# ---------------------------------------------------------------------------
# Explanations should stay hidden until the quiz is actually completed
# ---------------------------------------------------------------------------

def test_explanations_hidden_before_completion(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)

    resp = client.get(f"/api/quiz/{quiz.id}/questions")
    data = resp.get_json()

    assert data["is_completed"] is False
    assert data["explanations"] == {}


def test_explanations_revealed_after_completion(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS)
    client.post(f"/api/quiz/{quiz.id}/submit", json={"answers": {}})

    resp = client.get(f"/api/quiz/{quiz.id}/questions")
    data = resp.get_json()

    assert data["is_completed"] is True
    assert len(data["explanations"]) == 3
    first_q_id = str(quiz.questions[0].id)
    assert "correct" in data["explanations"][first_q_id]


# ---------------------------------------------------------------------------
# Hint logic
# ---------------------------------------------------------------------------

def test_hints_disabled_for_hard_difficulty(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS, difficulty="hard")
    q = quiz.questions[0]

    resp = client.post(f"/api/quiz/{quiz.id}/hint/{q.id}")

    assert resp.status_code == 400


def test_hints_disabled_for_god_mode(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS, difficulty="god mode")
    q = quiz.questions[0]

    resp = client.post(f"/api/quiz/{quiz.id}/hint/{q.id}")

    assert resp.status_code == 400


def test_hint_decrements_remaining_count_for_medium(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS, difficulty="medium", hints_remaining=2)
    q = quiz.questions[0]

    resp = client.post(f"/api/quiz/{quiz.id}/hint/{q.id}")
    data = resp.get_json()

    assert resp.status_code == 200
    assert data["hints_remaining"] == 1


def test_hint_blocked_when_none_remaining(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS, difficulty="medium", hints_remaining=0)
    q = quiz.questions[0]

    resp = client.post(f"/api/quiz/{quiz.id}/hint/{q.id}")

    assert resp.status_code == 400


def test_hint_requesting_twice_does_not_double_charge(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS, difficulty="medium", hints_remaining=2)
    q = quiz.questions[0]

    client.post(f"/api/quiz/{quiz.id}/hint/{q.id}")
    second = client.post(f"/api/quiz/{quiz.id}/hint/{q.id}")

    assert second.get_json()["hints_remaining"] == 1  # not decremented again


def test_hints_unlimited_for_easy_difficulty(client):
    user = _logged_in_user_and_client(client)
    quiz = make_quiz_session(user, SAMPLE_QUESTIONS, difficulty="easy", hints_remaining=-1)
    q = quiz.questions[0]

    resp = client.post(f"/api/quiz/{quiz.id}/hint/{q.id}")

    assert resp.status_code == 200
    assert resp.get_json()["hints_remaining"] == -1  # untouched/unlimited


# ---------------------------------------------------------------------------
# generate_quiz — input validation (Gemini call is mocked, never hits network)
# ---------------------------------------------------------------------------

def test_generate_quiz_rejects_too_few_questions(client):
    _logged_in_user_and_client(client)
    resp = client.post("/generate-quiz", data={"topic": "Algebra", "total_questions": "5", "duration": "10"})
    assert resp.status_code == 400


def test_generate_quiz_rejects_too_many_questions(client):
    _logged_in_user_and_client(client)
    resp = client.post("/generate-quiz", data={"topic": "Algebra", "total_questions": "500", "duration": "10"})
    assert resp.status_code == 400


def test_generate_quiz_rejects_bad_duration(client):
    _logged_in_user_and_client(client)
    resp = client.post("/generate-quiz", data={"topic": "Algebra", "total_questions": "10", "duration": "0"})
    assert resp.status_code == 400


def test_generate_quiz_requires_topic_or_pdf(client):
    _logged_in_user_and_client(client)
    resp = client.post("/generate-quiz", data={"topic": "", "total_questions": "10", "duration": "10"})
    assert resp.status_code == 400


def test_generate_quiz_requires_login(client):
    resp = client.post("/generate-quiz", data={"topic": "Algebra", "total_questions": "10", "duration": "10"},
                        follow_redirects=False)
    assert resp.status_code in (302, 401)


@patch("blueprints.quiz.routes.call_gemini")
def test_generate_quiz_success_creates_session_and_questions(mock_call_gemini, client):
    user = _logged_in_user_and_client(client)

    fake_response = MagicMock()
    fake_response.text = json.dumps({
        "questions": [
            {"question": "1+1?", "opt1": "1", "opt2": "2", "opt3": "3", "opt4": "4",
             "correct": 2, "hint": "count", "explanation": "basic addition"},
        ]
    })
    mock_call_gemini.return_value = fake_response

    resp = client.post("/generate-quiz", data={
        "topic": "Basic Math", "total_questions": "10", "duration": "10", "difficulty": "easy",
    })

    assert resp.status_code == 200
    data = resp.get_json()
    assert data["success"] is True
    quiz = db.session.get(QuizSession, data["session_id"])
    assert quiz.user_id == user.id
    assert quiz.topic == "Basic Math"


@patch("blueprints.quiz.routes.call_gemini", side_effect=RuntimeError("Gemini is down"))
def test_generate_quiz_handles_gemini_failure_gracefully(mock_call_gemini, client):
    _logged_in_user_and_client(client)

    resp = client.post("/generate-quiz", data={
        "topic": "Basic Math", "total_questions": "10", "duration": "10", "difficulty": "easy",
    })

    assert resp.status_code == 500
    assert "error" in resp.get_json()
