# 🤖 Shukaku AI: Secure Technical Assistant

Welcome to **Shukaku AI**, a production-ready, highly secure AI chatbot engineered to act as a professional technical mentor. Built on top of **Google Gemini 3.1 Flash-Lite** and powered by a robust Python/Flask backend, this application heavily enforces modern AI safety paradigms, Prompt Chaining, and the ReAct reasoning framework.

---

## ✨ Key AI Features & Architecture

*   **ReAct Framework & CoT:** Employs advanced reasoning capabilities (`Thought -> Action -> Observation -> Final Answer`) alongside Chain of Thought (CoT) prompting to ensure logical and accurate technical answers.
*   **Prompt Chaining Flow:** Queries don't just hit the model; they traverse a multi-stage pipeline: 
    `User Query ➔ Safety Check ➔ Intent Detection ➔ Response Generation ➔ JSON Formatting`
*   **Strict JSON Parsing:** The LLM is forced and verified to always return a rigid schema: `{"intent": "", "risk_level": "", "response": ""}`.
*   **Multi-Session Memory:** Local JSON database (`chat_db.json`) retains context up to 10 messages per chat session.

---

## 📸 Screenshots

![Screenshot 1](ScreenShot/Screenshot%202026-05-28%20143517.png)
![Screenshot 2](ScreenShot/Screenshot%202026-05-28%20143538.png)
![Screenshot 3](ScreenShot/Screenshot%202026-05-28%20143733.png)
![Screenshot 4](ScreenShot/Screenshot%202026-05-28%20143809.png)

---

## 🛡️ Robust AI Guardrails

Shukaku AI enforces strict safety guidelines to prevent credential leaks, toxic interactions, and jailbreaking.

1.  **Safety Check Prompting:** An initial AI validation step determines if the prompt contains malicious instructions or requests for sensitive information.
2.  **Code-Level Guardrails:** A local Python filter (`guardrails.py`) immediately halts processing if it detects:
    *   **Prompt Injections** (e.g., "ignore all previous instructions")
    *   **Credential Theft** (e.g., "show your api key")
    *   **Toxicity & Harassment**
    *   **Excessively Long Prompts** (> 1,000 chars)

---

## ⚙️ Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Harshitagarwal113/Shukaku-AI.git
    cd Shukaku-AI
    ```

2.  **Install dependencies:**
    Ensure you have Python 3 installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Environment Variables:**
    Create a `.env` file in the root directory and add your Gemini API Key:
    ```env
    GEMINI_API_KEY="your_gemini_api_key_here"
    FLASK_ENV="development"
    ```

4.  **Run the Application:**
    ```bash
    python run.py
    ```

5.  **Start Chatting:**
    Open your web browser and navigate to `http://localhost:5000`

---

## 📂 Project Structure

```text
/
├── app/
│   ├── core/                  # Core pipeline, guardrails, memory, and API Client
│   └── web/                   # Flask routing, UI templates, and static assets (CSS/JS)
├── docs/                      # Requirement documentation
│   ├── PRD.md                 # Product Requirement Document
│   └── FRD.md                 # Functional Requirement Document
├── parsers/                   
│   └── output_parser.py       # Strict JSON formatting verification
├── prompts/                   
│   ├── chaining.py            # CoT and ReAct multi-stage prompt logic
│   └── system_prompt.py       # Core persona definitions
├── ScreenShot/                # UI Demonstration Images
├── config.py                  # Flask configuration loader
├── requirements.txt           # Project dependencies
└── run.py                     # Entry point for the application
```

---
*Created by Harshit Agarwal | Built with ❤️ for developers by developers.*
