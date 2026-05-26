# 🎓 AI Study Assistant + Smart Explainer

A production-quality Streamlit application that acts as your **personal AI tutor** — explaining concepts in English + Roman Urdu, generating quizzes, and mapping your learning path.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Groq API key
```bash
# Linux / macOS
export GROQ_API_KEY="your_groq_api_key_here"

# Windows (PowerShell)
$env:GROQ_API_KEY = "your_groq_api_key_here"

# Windows (CMD)
set GROQ_API_KEY=your_groq_api_key_here
```

Get your free API key at: https://console.groq.com

### 3. Run the app
```bash
streamlit run app.py
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 💡 Explain Concept | Simple English + Roman Urdu explanation with real-world examples |
| 📝 Generate Quiz | 3 MCQs + 1 short-answer question with correct answers |
| 🗺️ Suggest Next Topics | Smart learning roadmap with 3 related topics |
| 💾 Session Memory | Remembers your last query across interactions |
| 📥 Download Output | Export any response as a `.txt` file |

---

## 🏗️ Code Structure

```
app.py
├── PAGE CONFIG         — Streamlit page setup
├── CUSTOM CSS/JS       — Gen-Z dark theme UI
├── get_groq_client()   — Cached Groq client init
├── get_llm_response()  — Core reusable LLM wrapper
├── generate_explanation()  — Concept explainer prompts
├── generate_quiz()         — MCQ + short answer prompts
├── generate_suggestions()  — Learning roadmap prompts
├── SESSION STATE       — Persistent state management
├── SIDEBAR             — Features + clear button
├── INPUT SECTION       — Query box + 3 action buttons
├── BUTTON HANDLERS     — Validation + spinner + API call
└── OUTPUT RENDERING    — Styled cards + download buttons
```

---

## 🔐 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GROQ_API_KEY` | ✅ Yes | Your Groq API key |

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — UI framework
- **Groq SDK** — LLM API (llama3-70b-8192)
- **Custom CSS** — Dark theme, Syne + DM Sans fonts, animations

---

## 📝 Notes

- The app uses `llama3-70b-8192` model via Groq for fast inference
- All prompts are structured for consistent, formatted output
- No API keys are ever hardcoded — always uses env variables
