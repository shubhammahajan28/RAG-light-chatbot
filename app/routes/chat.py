from flask import Blueprint, request, jsonify
from ..chatbot import get_bot_response

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/', methods=['POST'])
def chat():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"error": "No question provided"}), 400

    answer = get_bot_response(question)
    return jsonify({"answer": answer})
