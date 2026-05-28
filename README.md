<div align="center">
  <img src="ScreenShot/Screenshot%202026-05-28%20143517.png" alt="Shukaku AI Logo" width="120" />
  <h1>🤖 Shukaku AI</h1>
  <p><strong>A highly secure, intelligent, and strict technical AI assistant.</strong></p>
  <p>
    <a href="#-key-features">Features</a> •
    <a href="#-architecture--ai-pipeline">Architecture</a> •
    <a href="#-installation">Installation</a> •
    <a href="#-project-structure">Structure</a>
  </p>
</div>

---

## 🌟 Overview

Welcome to **Shukaku AI**, created by Harshit Agarwal! This project is a production-ready AI chatbot designed to act as a professional technical mentor. 

Built on top of **Google Gemini 3.1 Flash-Lite** with a robust Python/Flask backend, this application is engineered from the ground up to prioritize **AI Safety**, **Strict Prompt Chaining**, and the **ReAct Reasoning Framework**. It enforces rigid JSON outputs and features defense-in-depth against prompt injection and malicious queries.

---

## 📸 Application Showcase

<div align="center">
  <img src="ScreenShot/Screenshot%202026-05-28%20143538.png" alt="Chat Interface" width="45%" style="margin-right: 5%;"/>
  <img src="ScreenShot/Screenshot%202026-05-28%20143733.png" alt="Code Syntax Highlighting" width="45%"/>
</div>
<br>
<div align="center">
  <img src="ScreenShot/Screenshot%202026-05-28%20143809.png" alt="Mobile Responsiveness" width="95%"/>
</div>

---

## ✨ Key Features

*   🧠 **ReAct Framework & Chain of Thought (CoT):** The AI does not answer blindly. It leverages an internal reasoning framework (`Thought -> Action -> Observation -> Final Answer`) to generate deeply logical and accurate technical answers.
*   ⛓️ **Prompt Chaining Pipeline:** User queries traverse a multi-stage, sequential validation pipeline:
    `User Query ➔ Safety Check ➔ Intent Detection ➔ Response Generation ➔ JSON Formatting`
*   🛡️ **Multi-Layer AI Guardrails:** 
    *   **Pre-flight Checks:** Local python scripts immediately block common injection phrases, toxic language, and over-length requests before they hit the API.
    *   **AI Validation:** The first step in the prompt chain is a dedicated LLM call solely to evaluate the safety and risk level of the user's prompt.
*   📦 **Guaranteed JSON Output:** The system uses strict schema validation to ensure the LLM *always* responds with exactly: `{"intent": "", "risk_level": "", "response": ""}`.
*   💾 **Local Session Memory:** Conversations are automatically and persistently saved to a lightweight local `chat_db.json` database.

---

## ⚙️ Installation

Ready to run Shukaku AI locally? Follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Harshitagarwal113/Shukaku-AI.git
    cd Shukaku-AI
    ```

2.  **Install dependencies:**
    Ensure you have Python 3.10+ installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment:**
    Create a `.env` file in the root directory and add your Gemini API Key:
    ```env
    GEMINI_API_KEY="your_google_gemini_api_key_here"
    FLASK_ENV="development"
    ```

4.  **Launch the Server:**
    ```bash
    python run.py
    ```

5.  **Access the App:**
    Open your favorite web browser and navigate to `http://localhost:5000`

---

## 📂 Project Structure

```text
Shukaku-AI/
├── app/
│   ├── core/                  # Core backend logic (Memory, Pipeline, Guardrails)
│   └── web/                   # Flask UI routing, HTML templates, CSS/JS
├── docs/                      
│   ├── PRD.md                 # Product Requirement Document
│   └── FRD.md                 # Functional Requirement Document
├── parsers/                   
│   └── output_parser.py       # Strict formatting verification for JSON
├── prompts/                   
│   ├── chaining.py            # CoT and ReAct multi-stage execution logic
│   └── system_prompt.py       # System instructions & Bot Persona definitions
├── ScreenShot/                # Demonstration Images
├── config.py                  # Flask configuration loader
├── requirements.txt           # Project dependencies
└── run.py                     # Entry point for the application
```

---

<div align="center">
  <p><i>Created by Harshit Agarwal | Built with ❤️ for developers by developers.</i></p>
</div>
