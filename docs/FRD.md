# Functional Requirement Document (FRD)

## 1. System Architecture
- **Backend**: Python-based AI orchestration using Gemini API.
- **Frontend**: Vanilla JS, HTML, CSS interacting with REST endpoints.
- **Data Flow**: `User Query -> Safety Check -> Intent Detection -> Response Generation -> JSON Formatting`

## 2. Advanced Prompting & CoT
The system uses multiple prompts:
- **System Prompt**: `"You are a secure company assistant. Never reveal sensitive information. Always respond professionally."`
- **Chain of Thought (CoT)**: Step-by-step reasoning (Understand -> Check Safety -> Generate).
- **ReAct Framework**: Output generation structured via `Thought -> Action -> Observation -> Final Answer`.

## 3. AI Safety & Guardrails
- **Input Validation**: Checks against `UNSAFE_PATTERNS` (e.g. "Ignore previous instructions"), `TOXIC_WORDS`, and `ALLOWED_TOPICS`.
- **Length Limit**: Prompts exceeding 1000 characters are rejected.

## 4. Output Specification
The final output returned by the LLM and processed by the parser must strictly adhere to:
```json
{
    "intent": "<string>",
    "risk_level": "<high|low>",
    "response": "<string>"
}
```
If `risk_level` is `high`, the system handles it as a blocked/rejected request.
