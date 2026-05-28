from .guardrails import Guardrails
from .memory import ChatMemory
from .gemini_client import GeminiClient
from prompts.chaining import PromptChainer
from parsers.output_parser import OutputParser

class AIPipeline:
    """
    Orchestrates the entire AI flow:
    Input -> Guardrails -> Memory -> Chaining -> Parse -> Output
    """
    
    def __init__(self):
        self.guardrails = Guardrails()
        self.memory = ChatMemory(max_history=10)
        self.client = GeminiClient()
        self.prompt_chain = PromptChainer(self.client)
        self.parser = OutputParser()
        
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
        
        # Step 3 & 4: Prompt Chaining & Model Execution (Safety Check -> Intent -> Generation -> JSON)
        raw_json_response = self.prompt_chain.execute_chain(user_message, history)
        
        # Step 5: Parse Response
        parsed_response = self.parser.parse(raw_json_response)
        
        # Step 6: Update Memory (Only if successful)
        if parsed_response.get("intent") != "malicious_activity" and parsed_response.get("risk_level") == "low":
            self.memory.add_message(session_id, "user", user_message)
            
            assistant_content = parsed_response.get("response", "")
            self.memory.add_message(session_id, "assistant", assistant_content)
            
        return parsed_response
        
    def get_or_create_session(self, session_id: str = None) -> str:
        """Helper to manage session IDs"""
        if not session_id or session_id not in self.memory.sessions:
            return self.memory.create_session()
        return session_id
