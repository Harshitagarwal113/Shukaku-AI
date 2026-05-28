# Product Requirement Document (PRD)

## 1. Objective
Build a secure AI-powered chatbot that can answer user queries while strictly following safety rules and preventing malicious instructions.

## 2. Target Audience
Developers, system administrators, and technology enthusiasts seeking secure, reliable, and professional technical assistance.

## 3. Key Features
- **Technical Q&A**: Answers questions related to programming, DevOps, Linux, and Cloud.
- **Safety First**: Rejects unsafe or harmful requests automatically.
- **Prompt Injection Protection**: Resists attempts to override system instructions or reveal sensitive data.
- **Structured Output**: Always returns responses in a structured JSON format to the frontend.

## 4. User Experience
The user interacts via a modern web interface. If a request is safe, a professional markdown-formatted response is shown. If a request is unsafe, an immediate rejection message is shown, styled as an error/alert.
