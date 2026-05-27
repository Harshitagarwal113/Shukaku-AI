import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from config import config
import os
from .prompt_chain import PromptChain

class GeminiClient:
    """
    Handles initialization and interaction with the Gemini API.
    """
    
    def __init__(self, api_key: str = None, model_name: str = "gemini-3.1-flash-lite"):
        self.api_key = api_key or config['default'].GEMINI_API_KEY
        self.model_name = model_name
        
        if not self.api_key or self.api_key == "your_api_key_here":
            # Just log a warning, don't crash yet, it might be testing.
            print("WARNING: Gemini API Key is missing. Chat will fail.")
            
        genai.configure(api_key=self.api_key)
        
        # Configure Strict Safety Settings
        self.safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        }
        
        # Initialize model with system instruction
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=PromptChain.SYSTEM_INSTRUCTION,
            safety_settings=self.safety_settings,
            # Force JSON response type if using compatible model version
            generation_config={"response_mime_type": "application/json"}
        )

    def generate_response(self, user_message: str, history: list) -> str:
        """
        Sends the prompt and history to Gemini and returns the raw text response.
        """
        try:
            # We start a chat session with the provided history
            chat = self.model.start_chat(history=history)
            
            # Send the new user message
            response = chat.send_message(user_message)
            return response.text
            
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return '{"response": "I encountered an error communicating with the AI service. Please check your API key and connection.", "status": "error", "code_snippet": null}'
