import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from config import config
import os
from prompts.system_prompt import SYSTEM_PROMPT

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
            system_instruction=SYSTEM_PROMPT,
            safety_settings=self.safety_settings,
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

    def generate_simple(self, prompt: str) -> str:
        """
        Sends a single prompt to Gemini and returns the raw text response.
        """
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    response_mime_type="application/json"
                )
            )
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API for simple generation: {e}")
            return ""
