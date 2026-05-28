import json
import logging

class OutputParser:
    """
    Ensures the LLM output is correctly parsed into the strict JSON structure:
    {"intent": "", "risk_level": "", "response": ""}
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def parse(self, raw_text: str) -> dict:
        """
        Parses the raw text from the LLM into a dictionary.
        """
        # Clean the text: sometimes LLMs still wrap in markdown despite instructions
        clean_text = raw_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:]
            
        # Strip all remaining backticks and whitespace from the ends
        clean_text = clean_text.strip("` \n\r")
        
        try:
            parsed_data = json.loads(clean_text)
            
            # Validate expected fields
            if "response" not in parsed_data:
                parsed_data["response"] = "Response field missing from AI output."
            if "intent" not in parsed_data:
                parsed_data["intent"] = "unknown"
            if "risk_level" not in parsed_data:
                parsed_data["risk_level"] = "low"
                
            return parsed_data
            
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse LLM response as JSON. Error: {e}")
            self.logger.error(f"Raw output: {raw_text}")
            
            # Fallback response
            return {
                "intent": "unknown",
                "risk_level": "low",
                "response": "I encountered an error parsing my own response. Here is the raw output:\n\n" + raw_text
            }
