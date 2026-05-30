import uuid
import json
import os
from typing import List, Dict

class ChatMemory:
    """
    Simple file-backed chat history manager.
    Persists data to chat_db.json so history survives server reloads and browser clears.
    """
    
    def __init__(self, max_history=10, db_file="chat_db.json"):
        self.max_history = max_history
        
        # Vercel's root filesystem is read-only. We must write to /tmp.
        if os.environ.get("VERCEL") == "1":
            self.db_file = f"/tmp/{db_file}"
        else:
            self.db_file = db_file
            
        # Format: { "session_id": [{"role": "user", "content": "..."}] }
        self.sessions: Dict[str, List[Dict[str, str]]] = {}
        # Format: [{"id": "...", "title": "..."}]
        self.metadata: List[Dict[str, str]] = []
        self._load_from_disk()

    def _load_from_disk(self):
        """Load session data from JSON file."""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "metadata" in data and "sessions" in data:
                        self.metadata = data["metadata"]
                        self.sessions = data["sessions"]
                    else:
                        # Migrate old format
                        self.sessions = data
                        self.metadata = []
            except Exception as e:
                print(f"Error loading chat database: {e}")
                self.sessions = {}
                self.metadata = []
                
    def _save_to_disk(self):
        """Save session data to JSON file."""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump({
                    "metadata": self.metadata,
                    "sessions": self.sessions
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving chat database: {e}")

    def create_session(self) -> str:
        """Create a new chat session and return the ID."""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = []
        
        # Add to metadata
        self.metadata.insert(0, {"id": session_id, "title": "New Chat"})
        
        # Keep only 5
        if len(self.metadata) > 5:
            self.metadata = self.metadata[:5]
            
        self._save_to_disk()
        return session_id
        
    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        """Retrieve the chat history for a given session."""
        return self.sessions.get(session_id, [])
        
    def get_recent_sessions(self) -> List[Dict[str, str]]:
        """Get the recent sessions list."""
        return self.metadata
        
    def update_session_title(self, session_id: str, title: str):
        """Update the title of a session."""
        for s in self.metadata:
            if s['id'] == session_id:
                s['title'] = title
                break
        self._save_to_disk()
        
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to the session history and save it."""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            
        self.sessions[session_id].append({
            "role": role,
            "content": content
        })
        
        # Enforce max history limit (keep last N messages)
        if len(self.sessions[session_id]) > self.max_history * 2:
            self.sessions[session_id] = self.sessions[session_id][-self.max_history * 2:]
            
        self._save_to_disk()
            
    def clear_session(self, session_id: str):
        """Clear the history for a session."""
        if session_id in self.sessions:
            self.sessions[session_id] = []
            self._save_to_disk()
            
    def delete_session(self, session_id: str):
        """Completely delete a session from history and metadata."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            
        self.metadata = [s for s in self.metadata if s['id'] != session_id]
        self._save_to_disk()
