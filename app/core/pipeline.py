from .guardrails import Guardrails
from .memory import ChatMemory
from .prompt_chain import PromptChain
from .gemini_client import GeminiClient
from .parser import ResponseParser

class AIPipeline:
    """
    Orchestrates the entire AI flow:
    Input -> Guardrails -> Memory -> Prompt -> Gemini -> Parse -> Output
    """
    
    def __init__(self):
        self.guardrails = Guardrails()
        self.memory = ChatMemory(max_history=10)
        self.prompt_chain = PromptChain()
        self.client = GeminiClient()
        self.parser = ResponseParser()
        
    def process_message(self, session_id: str, user_message: str) -> dict:
        """
        Process a user message through the pipeline.
        """
        # Step 1: Guardrails Check (Security + Topic)
        guardrail_result = self.guardrails.check_message(user_message)
        if not guardrail_result["is_valid"]:
            return guardrail_result["rejection_message"]
            
        # Step 2: Retrieve Memory
        # If session doesn't exist, memory module will create it implicitly on add_message
        history = self.memory.get_history(session_id)
        
        # Step 3: Format Prompt/History for Gemini
        formatted_history = self.prompt_chain.build_prompt(user_message, history)
        
        # Step 4: Call Model
        raw_response = self.client.generate_response(user_message, formatted_history)
        
        # Step 5: Parse Response
        parsed_response = self.parser.parse(raw_response)
        
        # Step 6: Update Memory (Only if successful)
        if parsed_response.get("status") != "error":
            self.memory.add_message(session_id, "user", user_message)
            
            # Combine response and code for memory context
            assistant_content = parsed_response.get("response", "")
            if parsed_response.get("code_snippet"):
                assistant_content += f"\n\n```\n{parsed_response.get('code_snippet')}\n```"
                
            self.memory.add_message(session_id, "assistant", assistant_content)
            
        return parsed_response
        
    def get_or_create_session(self, session_id: str = None) -> str:
        """Helper to manage session IDs"""
        if not session_id or session_id not in self.memory.sessions:
            return self.memory.create_session()
        return session_id
