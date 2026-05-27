from flask import Blueprint, render_template, request, jsonify, session
from app.core.pipeline import AIPipeline
from app import limiter
import uuid

web_bp = Blueprint('web', __name__, template_folder='templates', static_folder='static', static_url_path='/web-static')

# Initialize single global pipeline instance
pipeline = AIPipeline()

def init_session():
    """Ensure the user has an active session ID."""
    if 'active_session_id' not in session:
        # Create the first session
        new_id = pipeline.memory.create_session()
        session['active_session_id'] = new_id
        session.modified = True

@web_bp.route('/')
def index():
    """Render the main chat interface."""
    init_session()
    return render_template('index.html')

@web_bp.route('/chat', methods=['POST'])
@limiter.limit("10 per minute")
def chat():
    """Handle incoming chat messages."""
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
        
    init_session()
    session_id = session['active_session_id']
    
    # Update title if it's "New Chat"
    recent = pipeline.memory.get_recent_sessions()
    for s in recent:
        if s['id'] == session_id and s['title'] == "New Chat":
            title = " ".join(user_message.split()[:4])
            if len(user_message.split()) > 4:
                title += "..."
            pipeline.memory.update_session_title(session_id, title)
            break
            
    # Process message through AI pipeline
    response_data = pipeline.process_message(session_id, user_message)
    
    return jsonify(response_data)
    
@web_bp.route('/reset', methods=['POST'])
@limiter.limit("10 per minute")
def reset_chat():
    """Create a new chat session."""
    init_session()
    
    recent = pipeline.memory.get_recent_sessions()
    
    # Don't stack multiple empty "New Chat" sessions
    if recent and recent[0]['title'] == "New Chat":
        session['active_session_id'] = recent[0]['id']
        session.modified = True
        return jsonify({"status": "success", "message": "Already in a new session."})
    
    # Create new session ID
    new_id = pipeline.memory.create_session()
    
    session['active_session_id'] = new_id
    session.modified = True
    
    return jsonify({"status": "success", "message": "New session created."})

@web_bp.route('/sessions', methods=['GET'])
def get_sessions():
    """Returns the list of recent sessions from the database."""
    init_session()
    
    recent = pipeline.memory.get_recent_sessions()
    active_id = session.get('active_session_id')
    
    # Only show 'New Chat' if it is the currently active session.
    display_sessions = [
        s for s in recent 
        if s['title'] != "New Chat" or s['id'] == active_id
    ]
    
    return jsonify({
        "sessions": display_sessions,
        "active_session_id": active_id
    })

@web_bp.route('/session/<session_id>', methods=['GET'])
def load_session(session_id):
    """Switch active session and load its history."""
    init_session()
    
    recent = pipeline.memory.get_recent_sessions()
    
    # Check if session exists in DB
    valid = any(s['id'] == session_id for s in recent)
    if not valid:
        return jsonify({"error": "Invalid session ID"}), 403
        
    session['active_session_id'] = session_id
    session.modified = True
    
    # Fetch history from memory
    history = pipeline.memory.get_history(session_id)
    return jsonify({"history": history})

@web_bp.route('/session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a chat session."""
    init_session()
    
    pipeline.memory.delete_session(session_id)
    
    # If the user deleted their active session, reset it to a new one
    if session.get('active_session_id') == session_id:
        new_id = pipeline.memory.create_session()
        session['active_session_id'] = new_id
        session.modified = True
        
    return jsonify({"status": "success"})
