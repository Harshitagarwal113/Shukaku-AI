from .guardrails import Guardrails
from .gemini_client import GeminiClient
from prompts.chaining import PromptChainer
from parsers.output_parser import OutputParser

class AIPipeline:
    """
    Orchestrates the entire AI flow:
    Input -> Guardrails -> Chaining -> Parse -> Output
    """
    
    def __init__(self):
        self.guardrails = Guardrails()
        self.client = GeminiClient()
        self.prompt_chain = PromptChainer(self.client)
        self.parser = OutputParser()
        
    def process_message(self, user_message: str, history: list = None) -> dict:
        """
        Process a user message through the pipeline.
        """
        if history is None:
            history = []
            
        # Step 1: Guardrails Check (Security + Topic)
        guardrail_result = self.guardrails.check_message(user_message)
        if not guardrail_result["is_valid"]:
            return guardrail_result["rejection_message"]
            
        # Step 2 & 3: Prompt Chaining & Model Execution (Safety Check -> Intent -> Generation -> JSON)
        raw_json_response = self.prompt_chain.execute_chain(user_message, history)
        
        # Step 4: Parse Response
        parsed_response = self.parser.parse(raw_json_response)
        
        return parsed_response
