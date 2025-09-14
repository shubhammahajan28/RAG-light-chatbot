from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..chatbot import get_bot_response
from ..models import User

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
@jwt_required()
def chat():
    user_id = int(get_jwt_identity())  # Convert back to int
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"message": "Question is required"}), 400

    answer = get_bot_response(question)

    return jsonify({
        "answer": answer
    }), 200