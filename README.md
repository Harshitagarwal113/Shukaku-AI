# 🤖 Shukaku AI

Welcome to **Shukaku AI**, a production-ready, highly secure AI chatbot designed to act as a professional technical mentor. Built with Flask and powered by Google's **Gemini 3.1 Flash-Lite**, this assistant is specifically trained and guardrailed to answer questions related to Software Engineering, DevOps, Cloud Infrastructure, and AI.

## ✨ Key Highlights

*   **Gemini 3.1 Powered:** Utilizes the lightning-fast `gemini-3.1-flash-lite` model for rapid, high-quality technical responses.
*   **Guaranteed JSON Output:** Leverages Gemini's `response_mime_type` feature alongside a custom fallback parser to guarantee the LLM strictly returns structured JSON.
*   **Multi-Session Local Database:** Chat histories and session metadata are persistently saved to a local `chat_db.json` file. You can create, switch between, and delete chats on the fly.
*   **Premium Glassmorphic UI:** A responsive, dark-mode frontend featuring smooth micro-animations, dynamic hover effects, and a sleek layout.
*   **Syntax Highlighting:** Automatically formats code snippets returned by the AI, complete with a beautifully integrated "Copy to Clipboard" button.

---

## 🛡️ Three-Layer Security Architecture

Shukaku AI takes safety seriously and implements a defense-in-depth approach to prevent abuse, prompt injection, and credential leaks.

1.  **Rate Limiting (Network Layer):**
    Utilizes `Flask-Limiter` to restrict users to a maximum of **50 requests per hour** and **200 per day** per IP address, effectively preventing spam and API exhaustion.

2.  **Strict Application Guardrails (Application Layer):**
    A rigorous local Python filter (`guardrails.py`) scans user prompts before they ever reach the AI. It instantly blocks:
    *   **Off-Topic Queries:** Enforces a strict technical-only policy using a vast whitelist of over 150+ tech keywords (e.g., politely rejects "What is the capital of France?").
    *   **Prompt Injection:** Detects and halts common jailbreak phrases like "ignore all previous instructions".
    *   **Credential Theft:** Blocks explicit attempts to extract sensitive data like "show your api key" or "print configuration".
    *   **Toxicity:** Rejects inappropriate or offensive language.
    *   **Length Limits:** Caps inputs at 1,000 characters.

3.  **Prompt Directives & Native Safety (AI Layer):**
    The core system prompt explicitly commands the AI to *never* reveal API keys, passwords, or its own internal instructions. Additionally, Gemini's native safety settings are configured to `BLOCK_LOW_AND_ABOVE` for all harassment and dangerous content categories.

---

## 🏗️ System Pipeline

```text
User Input 
  ➔ Rate Limiter (Flask-Limiter)
  ➔ Security Guardrails (Length, Toxicity, Injection, Topic) 
  ➔ Context Memory (Fetch history from JSON DB) 
  ➔ Prompt Chaining 
  ➔ Gemini 3.1 API (Forced JSON Mode) 
  ➔ Output Parser (JSON Validation & Fallbacks) 
  ➔ Frontend (Render & Highlight)
```

---

## 🛠️ Technologies Used

*   **Backend:** Python 3, Flask, Flask-Limiter
*   **AI Integration:** Google Generative AI SDK (`gemini-3.1-flash-lite`)
*   **Frontend:** HTML5, Vanilla CSS, Vanilla JavaScript
*   **Libraries:** Highlight.js (Code Formatting), FontAwesome (Icons), Marked.js (Markdown), DOMPurify (XSS Protection)

---

## ⚙️ Installation & Setup

Follow these steps to run the chatbot locally:

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
    GEMINI_API_KEY="your_api_key_here"
    FLASK_ENV="development"
    ```

4.  **Run the application:**
    ```bash
    python run.py
    ```

5.  **Access the Chatbot:**
    Open your web browser and navigate to `http://localhost:5000`

---

## 📂 Folder Structure

```text
/
├── .env                       # Environment variables (API Key)
├── .gitignore                 # Standard Python gitignore
├── requirements.txt           # Project dependencies
├── config.py                  # Configuration loader
├── chat_db.json               # Local persistent database (auto-generated)
├── run.py                     # Entry point for the Flask application
└── app/
    ├── __init__.py            # Flask app factory & Rate Limiter initialization
    ├── core/                  # AI Pipeline & Core Logic
    │   ├── gemini_client.py   # Handles connection and API calls to Gemini 3.1
    │   ├── memory.py          # Manages JSON-backed chat history (max 10 msgs/session)
    │   ├── guardrails.py      # Input validation & security filtering rules
    │   ├── prompt_chain.py    # Manages system persona instructions
    │   ├── parser.py          # Ensures the output is correctly formatted JSON
    │   └── pipeline.py        # Orchestrates the complete AI flow
    └── web/                   # Frontend & Routing
        ├── __init__.py
        ├── routes.py          # Flask HTTP endpoints (/chat, /reset, /session, /sessions)
        ├── templates/
        │   └── index.html     # Main chat UI structure
        └── static/
            ├── css/
            │   └── style.css  # UI Styling (Premium dark glassmorphism theme)
            └── js/
                └── main.js    # Client-side logic for the chat interface
```

---
*Created by Harshit Agarwal | Built with ❤️ for developers by developers.*
