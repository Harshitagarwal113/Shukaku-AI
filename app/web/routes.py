from flask import Blueprint, render_template, request, jsonify
from app.core.pipeline import AIPipeline
from app import limiter

web_bp = Blueprint('web', __name__, template_folder='templates', static_folder='static', static_url_path='/web-static')

# Initialize single global pipeline instance
pipeline = AIPipeline()

@web_bp.route('/')
def index():
    """Render the main chat interface."""
    return render_template('index.html')

@web_bp.route('/chat', methods=['POST'])
@limiter.limit("80 per minute")
def chat():
    """Handle incoming chat messages."""
    data = request.json
    user_message = data.get('message')
    history = data.get('history', [])
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
            
    # Process message through AI pipeline
    response_data = pipeline.process_message(user_message, history)
    
    return jsonify(response_data)
