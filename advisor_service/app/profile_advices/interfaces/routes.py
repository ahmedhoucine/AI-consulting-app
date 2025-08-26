from flask import Blueprint, copy_current_request_context, request, jsonify
from app.profile_advices.services.streaming_callback import StreamTokensHandler
from app.profile_advices.services.advisor_service import AdvisorService
from flask import Response

advisor_bp = Blueprint('advisor', __name__)
service = AdvisorService()

@advisor_bp.route('/history', methods=['GET'])
def advisor_history():
    try:
        records = service.get_history()
        result = [
            {
                "id": r.id,
                "profile_description": r.profile_description,
                "target_job_title": r.target_job_title,
                "advice": r.advice,
                "created_at": r.created_at.isoformat()
            }
            for r in records
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@advisor_bp.route('/stream', methods=['POST'])
def advisor_stream():
    data = request.get_json()
    profile_description = data.get('profile_description')
    target_job_title = data.get('target_job_title')

    if not profile_description or not target_job_title:
        return jsonify({"error": "Missing required fields"}), 400

    tokens = []

    @copy_current_request_context
    def save_advice_later(full_text):
        service.repo.save_advice(profile_description, target_job_title, full_text)
        print("saved:", full_text)

    def generate():
        stream = service.repo.get_recommendations(profile_description, target_job_title, stream=True)
        for chunk in stream:
            tokens.append(chunk)
            yield chunk
        # After streaming finished, save in DB (inside app context)
        full_text = "".join(tokens)
        save_advice_later(full_text)

    return Response(generate(), content_type='text/plain')