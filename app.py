"""
╔══════════════════════════════════════════════════════════════════╗
║       AI STUDY ASSISTANT — ULTRA PREMIUM EDITION                ║
║       Model: llama-3.3-70b-versatile (Groq, 2025)              ║
║       Features: 12 AI Tools in one SaaS-grade Streamlit App    ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ── stdlib ────────────────────────────────────────────────────────
import os
import tempfile
import textwrap
import streamlit as st

# ── third-party ───────────────────────────────────────────────────
from groq import Groq

# ── dotenv (optional – silently skipped if not installed) ─────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIG  — MUST be first Streamlit call
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════
# DESIGN SYSTEM — Clean, Scalable, Production-Level CSS
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ============================================================
   0. FONT IMPORT
   ============================================================ */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ============================================================
   1. DESIGN TOKENS
   ============================================================ */
:root {
  --bg:          #f4f6fb;
  --surface:     #ffffff;
  --surface-2:   #f0f2f9;
  --surface-3:   #e8ecf8;
  --border:      #e0e4f0;
  --border-focus:#6366f1;
  --p:           #6366f1;
  --p-lt:        #eef2ff;
  --p-dk:        #4338ca;
  --p-ring:      rgba(99,102,241,0.18);
  --teal:        #0d9488;   --teal-lt:   #f0fdfa;
  --amber:       #d97706;   --amber-lt:  #fffbeb;
  --rose:        #e11d48;   --rose-lt:   #fff1f2;
  --green:       #16a34a;   --green-lt:  #f0fdf4;
  --sky:         #0284c7;   --sky-lt:    #f0f9ff;
  --violet:      #7c3aed;   --violet-lt: #f5f3ff;
  --orange:      #ea580c;   --orange-lt: #fff7ed;
  --text:        #1a1b2e;
  --text-2:      #4b5275;
  --text-3:      #8b90b0;
  --r:           10px;
  --r-lg:        16px;
  --r-xl:        22px;
  --sh:    0 1px 3px rgba(26,27,46,.07), 0 1px 2px rgba(26,27,46,.04);
  --sh-md: 0 4px 16px rgba(26,27,46,.08), 0 1px 4px rgba(26,27,46,.04);
  --sh-lg: 0 12px 40px rgba(26,27,46,.11);
  --font: 'Plus Jakarta Sans', sans-serif;
  --mono: 'JetBrains Mono', monospace;
}

/* ============================================================
   2. BASE — app background, hide chrome, remove top black border
   ============================================================ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
  background:  var(--bg)   !important;
  color:       var(--text) !important;
  font-family: var(--font) !important;
}

/* Remove the black top bar/border Streamlit injects */
[data-testid="stHeader"],
[data-testid="stDecoration"],
.stApp > header,
section[data-testid="stSidebar"] + div > div:first-child > div:first-child {
  display:    none !important;
  height:     0    !important;
  min-height: 0    !important;
}

/* Hide other Streamlit chrome */
#MainMenu,
footer,
header,
[data-testid="stStatusWidget"] {
  display: none !important;
}

/* Scrollbar */
::-webkit-scrollbar       { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: #cdd0e4; border-radius: 99px; }

/* Typography */
.stMarkdown p, .stMarkdown li {
  font-family: var(--font) !important;
  color:       var(--text) !important;
  line-height: 1.72 !important;
}
.stMarkdown h2, .stMarkdown h3 {
  font-family: var(--font) !important;
  font-weight: 700 !important;
  color:       var(--text) !important;
}
code {
  font-family:   var(--mono)      !important;
  background:    var(--surface-2) !important;
  border:        1px solid var(--border) !important;
  border-radius: 4px !important;
  padding:       1px 5px !important;
  font-size:     .85em !important;
  color:         var(--p-dk) !important;
}
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* ============================================================
   3. SIDEBAR
   ============================================================ */
[data-testid="stSidebar"] {
  background:   var(--surface) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

.sb-head { background:linear-gradient(135deg,#6366f1,#818cf8); padding:26px 20px 20px; }
.sb-head-title { font-weight:800; font-size:1.15rem; color:#fff !important; margin:0 0 3px; }
.sb-head-sub   { font-size:.75rem; color:rgba(255,255,255,.72) !important; margin:0; }
.sb-sec  { padding:14px 18px; border-bottom:1px solid var(--border); }
.sb-lbl  { font-size:.67rem; font-weight:700; letter-spacing:.1em; text-transform:uppercase;
           color:var(--text-3) !important; margin-bottom:8px; }

.sb-stat-row { display:flex; gap:7px; margin-top:4px; }
.sb-stat     { flex:1; background:var(--surface-2); border-radius:var(--r); padding:9px 10px; text-align:center; }
.sb-stat-v   { font-size:1.15rem; font-weight:800; color:var(--p) !important; display:block; }
.sb-stat-l   { font-size:.64rem; color:var(--text-3) !important; font-weight:600;
               text-transform:uppercase; letter-spacing:.05em; }

.sb-feat   { display:flex; align-items:flex-start; gap:9px; padding:6px 0; }
.sb-icon   { width:26px; height:26px; border-radius:7px; display:flex; align-items:center;
             justify-content:center; font-size:.8rem; flex-shrink:0; }
.ic-p { background:var(--p-lt); }   .ic-t { background:var(--teal-lt); }
.ic-a { background:var(--amber-lt); } .ic-r { background:var(--rose-lt); }
.ic-s { background:var(--sky-lt); }  .ic-v { background:var(--violet-lt); }
.sb-feat strong { display:block; font-size:.79rem; font-weight:600; margin-bottom:1px; }
.sb-feat span   { font-size:.72rem; color:var(--text-3) !important; }
.sb-footer { padding:13px 18px; font-size:.72rem; color:var(--text-3) !important; text-align:center; }

/* ============================================================
   4. HERO SECTION
   ============================================================ */
.hero       { text-align:center; padding:40px 20px 28px; }
.hero-badge {
  display:inline-flex; align-items:center; gap:5px; background:var(--p-lt);
  color:var(--p) !important; border:1px solid #c7d2fe; border-radius:99px;
  padding:4px 14px; font-size:.71rem; font-weight:700;
  letter-spacing:.05em; text-transform:uppercase; margin-bottom:16px;
}
.hero-title {
  font-weight:800; font-size:clamp(1.9rem,4.5vw,3rem);
  color:var(--text) !important; letter-spacing:-.04em; line-height:1.1; margin:0 0 9px;
}
.hero-title span {
  background:linear-gradient(135deg,#6366f1,#8b5cf6);
  -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
}
.hero-sub { font-size:.97rem; color:var(--text-2) !important; margin:0 auto 22px;
            max-width:480px; line-height:1.65; }
.hero-div { width:50px; height:3px; background:linear-gradient(90deg,#6366f1,#8b5cf6);
            border-radius:99px; margin:0 auto; }

/* ============================================================
   5. TOOL GRID CARDS
   ============================================================ */
.tool-card {
  background:    var(--surface);
  border:        1.5px solid var(--border);
  border-radius: var(--r-lg);
  padding:       16px 16px 13px;
  cursor:        pointer;
  transition:    border-color .18s, box-shadow .18s, transform .18s;
  box-shadow:    var(--sh);
  text-align:    center;
}
.tool-card:hover {
  border-color: var(--border-focus);
  box-shadow:   var(--sh-md);
  transform:    translateY(-2px);
}
.tool-card.active {
  border-color: var(--p);
  background:   var(--p-lt);
  box-shadow:   0 0 0 3px var(--p-ring), var(--sh-md);
}
.tool-card-icon { font-size:1.6rem; margin-bottom:7px; }
.tool-card-name { font-size:.8rem; font-weight:700; color:var(--text); margin-bottom:2px; }
.tool-card-desc { font-size:.7rem; color:var(--text-3); }

/* ============================================================
   6. INPUT CARD
   ============================================================ */
.inp-card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--r-xl); padding:24px 28px 20px;
  box-shadow:var(--sh-md); margin-bottom:20px;
}
.inp-lbl {
  font-size:.72rem; font-weight:700; letter-spacing:.08em;
  text-transform:uppercase; color:var(--text-3); margin-bottom:8px;
}

/* ============================================================
   7. TEXTAREA
   ============================================================ */
.stTextArea label { display: none !important; }
.stTextArea textarea {
  background:    var(--surface-2) !important;
  border:        1.5px solid var(--border) !important;
  border-radius: var(--r) !important;
  color:         var(--text) !important;
  font-family:   var(--font) !important;
  font-size:     .92rem !important;
  line-height:   1.6 !important;
  padding:       12px 14px !important;
  resize:        none !important;
}
.stTextArea textarea:focus {
  border-color: var(--border-focus) !important;
  box-shadow:   0 0 0 3px var(--p-ring) !important;
  background:   var(--surface) !important;
}
.stTextArea textarea::placeholder { color: var(--text-3) !important; }

/* ============================================================
   8. TEXT INPUT
   ============================================================ */
.stTextInput label,
.stTextInput label p {
  color:       var(--text) !important;
  font-family: var(--font) !important;
  font-size:   .85rem !important;
  font-weight: 600 !important;
}
.stTextInput input {
  background:    var(--surface-2) !important;
  border:        1.5px solid var(--border) !important;
  border-radius: var(--r) !important;
  color:         var(--text) !important;
  font-family:   var(--font) !important;
  font-size:     .92rem !important;
  padding:       10px 14px !important;
}
.stTextInput input:focus {
  border-color: var(--border-focus) !important;
  box-shadow:   0 0 0 3px var(--p-ring) !important;
  background:   var(--surface) !important;
}
.stTextInput input::placeholder { color: var(--text-3) !important; }

/* ============================================================
   9. SELECTBOX
   ============================================================ */
.stSelectbox label,
.stSelectbox label p,
[data-testid="stSelectbox"] label,
[data-testid="stSelectbox"] label p {
  color:       var(--text) !important;
  font-family: var(--font) !important;
  font-size:   .85rem !important;
  font-weight: 600 !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] > div:first-child,
[data-baseweb="select"] > div:first-child {
  background:    var(--surface) !important;
  border:        1.5px solid var(--border) !important;
  border-radius: var(--r) !important;
}
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div,
[data-baseweb="select"] [class*="singleValue"],
[data-baseweb="select"] [class*="placeholder"],
[data-baseweb="select"] [class*="ValueContainer"] span,
[data-baseweb="select"] [class*="ValueContainer"] div {
  color:       var(--text) !important;
  font-family: var(--font) !important;
}
[data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] li,
[role="listbox"] [role="option"],
[role="listbox"] li {
  background:  var(--surface) !important;
  color:       var(--text)    !important;
  font-family: var(--font)    !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[role="listbox"] [role="option"]:hover {
  background: var(--p-lt) !important;
  color:      var(--p)    !important;
}

/* ============================================================
   10. BUTTON SYSTEM — FIXED
       White background, dark text, light-blue hover.
       Uses every possible selector to override Streamlit's
       injected inline dark styles.
   ============================================================ */

/* — Global button reset (catches ALL stButton instances) — */
.stButton > button,
.stButton > button:link,
.stButton > button:visited,
div[data-testid="stButton"] > button,
div[data-testid="column"] .stButton > button,
[data-testid="stVerticalBlock"] .stButton > button {
  width:            100%                      !important;
  border-radius:    var(--r)                  !important;
  font-family:      var(--font)               !important;
  font-weight:      600                       !important;
  font-size:        .84rem                    !important;
  padding:          .6rem 1rem                !important;
  border:           1.5px solid var(--border) !important;
  background:       #ffffff                   !important;
  background-color: #ffffff                   !important;
  color:            #1a1b2e                   !important;
  box-shadow:       var(--sh)                 !important;
  cursor:           pointer                   !important;
  line-height:      1.4                       !important;
  transition:       background-color .18s ease, border-color .18s ease,
                    color .18s ease, transform .18s ease,
                    box-shadow .18s ease      !important;
  /* Override any inline style Streamlit injects */
  -webkit-appearance: none                   !important;
  appearance:         none                   !important;
}

/* Force inner <p> / <span> text colour */
.stButton > button p,
.stButton > button span,
div[data-testid="stButton"] > button p,
div[data-testid="stButton"] > button span {
  color: #1a1b2e !important;
}

/* Hover — light indigo tint */
.stButton > button:hover,
div[data-testid="stButton"] > button:hover,
div[data-testid="column"] .stButton > button:hover {
  background:       #eef2ff !important;
  background-color: #eef2ff !important;
  border-color:     #a5b4fc !important;
  color:            #4338ca !important;
  transform:        translateY(-1px) !important;
  box-shadow:       var(--sh-md)     !important;
}

.stButton > button:hover p,
.stButton > button:hover span,
div[data-testid="stButton"] > button:hover p,
div[data-testid="stButton"] > button:hover span {
  color: #4338ca !important;
}

/* Active */
.stButton > button:active,
div[data-testid="stButton"] > button:active {
  transform:        translateY(0) !important;
  box-shadow:       var(--sh)     !important;
  background:       #e0e7ff       !important;
  background-color: #e0e7ff       !important;
}

/* Focus ring */
.stButton > button:focus,
div[data-testid="stButton"] > button:focus {
  outline:    none                        !important;
  box-shadow: 0 0 0 3px var(--p-ring)     !important;
}

/* Download button — green variant */
.stDownloadButton > button {
  background:       var(--green-lt)    !important;
  background-color: var(--green-lt)    !important;
  border:           1.5px solid #86efac !important;
  color:            var(--green)        !important;
  border-radius:    var(--r)            !important;
  font-family:      var(--font)         !important;
  font-size:        .8rem               !important;
  font-weight:      600                 !important;
  padding:          .45rem 1rem         !important;
  box-shadow:       none                !important;
}
.stDownloadButton > button:hover {
  background:       #dcfce7  !important;
  background-color: #dcfce7  !important;
  border-color:     #4ade80  !important;
  transform:        translateY(-1px) !important;
}

/* ============================================================
   11. TABS
   ============================================================ */
[data-testid="stTabs"] {
  background:    var(--surface);
  border:        1px solid var(--border);
  border-radius: var(--r-xl);
  box-shadow:    var(--sh-md);
  overflow:      hidden;
}
[data-testid="stTabs"] [role="tablist"] {
  background:    var(--surface-2) !important;
  border-bottom: 1px solid var(--border) !important;
  gap: 0 !important; padding: 0 12px !important;
}
[data-testid="stTabs"] button[role="tab"] {
  font-family:   var(--font)  !important;
  font-size:     .81rem       !important;
  font-weight:   600          !important;
  color:         var(--text-2)!important;
  padding:       12px 16px    !important;
  border-radius: 0            !important;
  border:        none         !important;
  border-bottom: 2px solid transparent !important;
  background:    transparent  !important;
  margin-bottom: -1px         !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
  color:      var(--p) !important;
  background: rgba(99,102,241,.05) !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
  color:              var(--p) !important;
  border-bottom-color:var(--p) !important;
}
[data-testid="stTabs"] [role="tabpanel"] { padding: 24px 28px 20px !important; }

/* ============================================================
   12. BADGES
   ============================================================ */
.badge {
  display:inline-flex; align-items:center; gap:4px;
  border-radius:99px; padding:3px 11px;
  font-size:.7rem; font-weight:700; letter-spacing:.04em;
}
.bd-p { background:var(--p-lt);      color:var(--p);      border:1px solid #c7d2fe; }
.bd-t { background:var(--teal-lt);   color:var(--teal);   border:1px solid #99f6e4; }
.bd-a { background:var(--amber-lt);  color:var(--amber);  border:1px solid #fde68a; }
.bd-r { background:var(--rose-lt);   color:var(--rose);   border:1px solid #fecdd3; }
.bd-s { background:var(--sky-lt);    color:var(--sky);    border:1px solid #bae6fd; }
.bd-v { background:var(--violet-lt); color:var(--violet); border:1px solid #ddd6fe; }
.bd-o { background:var(--orange-lt); color:var(--orange); border:1px solid #fed7aa; }
.bd-g { background:var(--green-lt);  color:var(--green);  border:1px solid #bbf7d0; }
.bd-c { background:var(--surface-2); color:var(--text-2); border:1px solid var(--border);
        font-family:var(--mono); }

/* ============================================================
   13. QUERY ECHO / SECTION DIVIDER / MISC
   ============================================================ */
.out-meta { display:flex; align-items:center; gap:7px; margin-bottom:16px; flex-wrap:wrap; }

.q-echo {
  display:flex; align-items:flex-start; gap:11px; background:var(--surface);
  border:1px solid var(--border); border-left:3px solid var(--p);
  border-radius:var(--r); padding:12px 16px; margin-bottom:16px; box-shadow:var(--sh);
}
.q-lbl {
  font-size:.68rem; font-weight:700; letter-spacing:.07em;
  text-transform:uppercase; color:var(--p); white-space:nowrap; margin-top:2px;
}
.q-txt { font-size:.88rem; font-weight:500; color:var(--text); line-height:1.5; }

.sec-div      { display:flex; align-items:center; gap:12px; margin:28px 0 20px; }
.sec-div-line { flex:1; height:1px; background:var(--border); }
.sec-div-txt  { font-size:.7rem; font-weight:700; letter-spacing:.1em;
                text-transform:uppercase; color:var(--text-3); }

.fb-lbl { font-size:.78rem; font-weight:500; color:var(--text-3); }

.empty-wrap  { text-align:center; padding:56px 24px 48px; }
.empty-icon  { width:64px; height:64px; background:var(--p-lt); border-radius:50%;
               display:flex; align-items:center; justify-content:center;
               font-size:1.7rem; margin:0 auto 16px; }
.empty-title { font-size:1rem; font-weight:700; color:var(--text); margin-bottom:7px; }
.empty-sub   { font-size:.85rem; color:var(--text-3); max-width:340px;
               margin:0 auto; line-height:1.65; }

[data-testid="stFileUploader"] {
  background:    var(--surface-2) !important;
  border:        1.5px dashed var(--border) !important;
  border-radius: var(--r) !important;
  padding:       8px !important;
}

[data-testid="stAlert"] {
  border-radius: var(--r) !important;
  font-family:   var(--font) !important;
}

.audio-tab-info {
  background:var(--p-lt); border:1px solid #c7d2fe; border-radius:var(--r);
  padding:10px 14px; font-size:.8rem; color:var(--p-dk); margin-bottom:10px; font-weight:500;
}

/* Mental health chat input */
div[data-baseweb="input"] input              { color: var(--text)   !important; }
div[data-baseweb="input"] input::placeholder { color: var(--text-3) !important; }
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# GROQ CLIENT
# ═══════════════════════════════════════════════════════════════════
@st.cache_resource
def get_groq_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY", "")
    if not api_key:
        st.error(
            "**⚠️ GROQ_API_KEY not found.**  \n"
            "Create a `.env` file with `GROQ_API_KEY=gsk_...` and restart."
        )
        st.stop()
    return Groq(api_key=api_key)

client = get_groq_client()

LLM_MODEL = "llama-3.3-70b-versatile"
STT_MODEL = "whisper-large-v3-turbo"

# ═══════════════════════════════════════════════════════════════════
# CORE LLM WRAPPER
# ═══════════════════════════════════════════════════════════════════
def llm(prompt: str, system: str = "", max_tokens: int = 1500) -> str:
    try:
        msgs = []
        if system:
            msgs.append({"role": "system", "content": system})
        msgs.append({"role": "user", "content": prompt})
        resp = client.chat.completions.create(
            model=LLM_MODEL, messages=msgs,
            temperature=0.7, max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ **Error:** {e}"

# ═══════════════════════════════════════════════════════════════════
# FEATURE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def explain_concept(topic: str) -> str:
    sys = ("You are an expert, friendly tutor who explains concepts in "
           "simple English AND Roman Urdu (Urdu written in English letters). "
           "Always give real-world examples. Avoid jargon.")
    return llm(f"""Explain: **{topic}**

## 🔵 Simple English Explanation
(2-3 beginner-friendly paragraphs)

## 🟠 Roman Urdu Mein Samjhein
(Same explanation in Roman Urdu)

## 💡 Real-World Example
(One vivid, relatable example)

## 🔑 Key Takeaway
(One sentence summary)
""", sys)

def generate_quiz(topic: str) -> str:
    sys = "You are a professional exam question writer. Use clear language, plausible distractors, and always mark correct answers."
    return llm(f"""Create a complete quiz on: **{topic}**

## 📝 Quiz: {topic}

**Q1 (MCQ)** — [question]
- A) ... B) ... C) ... D) ...
✅ **Answer:** [letter] — [brief reason]

**Q2 (MCQ)** — [question]
- A) ... B) ... C) ... D) ...
✅ **Answer:** [letter] — [brief reason]

**Q3 (MCQ)** — [question]
- A) ... B) ... C) ... D) ...
✅ **Answer:** [letter] — [brief reason]

**Q4 (Short Answer)** — [question]
✅ **Model Answer:** [2-3 sentences]
""", sys)

def suggest_topics(topic: str) -> str:
    sys = "You are a curriculum designer. Suggest logical, motivating next-step topics with clear reasons and difficulty ratings."
    return llm(f"""Student just studied: **{topic}**

## 🗺️ Your Learning Roadmap

### 1️⃣ [Topic Name]
**Why learn this?** | **What you gain:** | **Difficulty:** ⭐⭐☆☆☆

### 2️⃣ [Topic Name]
**Why learn this?** | **What you gain:** | **Difficulty:** ⭐⭐⭐☆☆

### 3️⃣ [Topic Name]
**Why learn this?** | **What you gain:** | **Difficulty:** ⭐⭐⭐⭐☆

---
💬 **Pro Tip:** Follow this order for the smoothest learning curve!
""", sys)

def generate_notes(topic: str) -> str:
    sys = "You are an expert note-taker. Create clean, structured study notes that students can revise from quickly."
    return llm(f"""Generate complete study notes for: **{topic}**

## 📒 Study Notes: {topic}

### 📌 Overview
(2-3 sentences defining the topic)

### 🧩 Key Concepts
(Bullet-pointed list of 5-7 core ideas, each with a one-line explanation)

### 📊 Important Facts / Formulas / Dates
(Any numbers, formulas, or key data in a clean list)

### 🔗 Connections to Other Topics
(2-3 related topics and how they connect)

### ✍️ Quick Revision Summary
(5-bullet cheat sheet a student can glance at before an exam)
""", sys)

def generate_exam_paper(topic: str, marks: int, exam_type: str) -> str:
    sys = "You are an experienced teacher. Create a professional, well-structured exam paper with clear instructions and a variety of question types."
    return llm(f"""Create a {exam_type} exam paper on: **{topic}**
Total Marks: {marks}

# 📄 EXAMINATION PAPER
**Subject:** {topic}
**Total Marks:** {marks} | **Time Allowed:** {marks} minutes

---
## SECTION A — Multiple Choice Questions (1 mark each)
(5 MCQs with 4 options each — mark correct answers at the end)

## SECTION B — Short Answer Questions (3 marks each)
(3 short-answer questions requiring 3-5 sentence answers)

## SECTION C — Long Answer / Essay Questions (5 marks each)
(2 detailed questions requiring structured paragraph answers)

---
## ✅ ANSWER KEY
(Correct answers for Section A + model answers for B & C)
""", sys, max_tokens=2000)

def verify_content(text: str) -> str:
    sys = ("You are a critical-thinking AI fact-checker. Analyse content objectively. "
           "Be careful and nuanced — do not fabricate specific fact-check results. "
           "Focus on logical analysis, red flags, and verification guidance.")
    return llm(f"""Analyse this content for credibility and potential misinformation:

---
{text[:2000]}
---

## 🔍 Content Analysis Report

### 📊 Credibility Assessment
(Rate: High / Medium / Low / Uncertain — with reasoning)

### ⚠️ Red Flags Detected
(List any suspicious claims, emotional language, missing sources, logical fallacies)

### ✅ What Seems Credible
(List elements that appear factual or well-supported)

### 🔎 How to Verify This
(3-5 specific steps the reader should take to verify this content)

### 📌 Verdict Summary
(One-paragraph balanced conclusion)
""", sys)

def mental_health_chat(message: str, history: list) -> str:
    sys = textwrap.dedent("""
        You are a compassionate, non-judgmental mental wellness companion for students.
        You do NOT diagnose or prescribe. You listen, validate emotions, and offer
        evidence-based coping suggestions (breathing, journaling, grounding techniques).
        Always remind users to seek professional help for serious issues.
        Keep responses warm, concise (3-5 sentences), and empathetic.
        End with one gentle supportive question or coping suggestion.
    """).strip()
    msgs = [{"role": "system", "content": sys}]
    for h in history[-6:]:
        msgs.append({"role": h["role"], "content": h["content"]})
    msgs.append({"role": "user", "content": message})
    try:
        resp = client.chat.completions.create(
            model=LLM_MODEL, messages=msgs, temperature=0.75, max_tokens=400
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ **Error:** {e}"

def requirements_to_code(requirements: str, language: str) -> str:
    sys = (f"You are a senior {language} engineer. Write clean, production-quality, "
           "well-commented code. Follow best practices. Include brief inline comments.")
    return llm(f"""Convert these requirements into working {language} code:

REQUIREMENTS:
{requirements}

Provide:
1. Complete, runnable {language} code
2. Brief explanation of the approach
3. How to run / use the code
4. Any dependencies needed
""", sys, max_tokens=2000)

def summarize_research(text: str) -> str:
    sys = "You are an academic research assistant skilled in summarizing papers and improving writing originality."
    return llm(f"""Process this academic content:

---
{text[:3000]}
---

## 📑 Research Summary

### 🎯 Main Objective
(What problem does this research address?)

### 🔬 Methodology
(How was the research conducted?)

### 📊 Key Findings
(3-5 bullet points of main results)

### 💡 Conclusions & Implications
(What does this mean for the field?)

### ✍️ Improved / Paraphrased Version
(Rewrite the above in original academic language to reduce similarity)

### 📚 Suggested Citation Format (APA)
(Best-guess APA citation based on available info)
""", sys, max_tokens=2000)

def create_storyboard(concept: str, scenes: int) -> str:
    sys = "You are a creative director and visual storyteller. Create detailed, vivid storyboards suitable for educational or creative projects."
    return llm(f"""Create a {scenes}-scene storyboard for: **{concept}**

## 🎬 Storyboard: {concept}

For each scene provide:
- **Scene #** | **Title**
- 🖼️ **Visual Description:** (what the audience sees — camera angle, setting, characters)
- 🎙️ **Narration / Dialogue:** (what is spoken or shown as text)
- 🎵 **Mood / Music:** (emotional tone and suggested background)
- ⏱️ **Duration:** (suggested seconds)

Create all {scenes} scenes with this format.

---
### 📋 Production Notes
(Overall tone, target audience, key visual style recommendations)
""", sys, max_tokens=2000)

def review_code(code: str, language: str) -> str:
    sys = (f"You are a senior {language} engineer and code quality expert. "
           "Provide thorough, actionable reviews. Be constructive and educational.")
    return llm(f"""Review this {language} code:

```{language.lower()}
{code[:3000]}
```

## 🔍 Code Review Report

### ✅ What's Good
(Positive aspects — good patterns, readability, logic)

### 🐛 Bugs & Errors Found
(List specific bugs with line references and explanations)

### ⚠️ Code Quality Issues
(Naming, structure, efficiency, best-practice violations)

### 🔒 Security / Safety Concerns
(Any potential security issues)

### 🚀 Improved Version
(Rewrite the corrected, improved code with comments)

### 📚 What to Learn
(2-3 concepts or resources to study based on the issues found)
""", sys, max_tokens=2000)

def learning_mentor(goal: str, level: str, style: str) -> str:
    sys = "You are an expert educational mentor who creates personalised, actionable learning plans."
    return llm(f"""Create a personalised learning plan:

**Goal:** {goal}
**Current Level:** {level}
**Learning Style:** {style}

## 🎯 Personalized Learning Plan

### 📍 Where You Are Now
(Assessment of starting point for someone at {level} level)

### 🏁 Your Goal Breakdown
(Break {goal} into 3-5 achievable milestones)

### 📅 Week-by-Week Plan (4 Weeks)
**Week 1:** ...
**Week 2:** ...
**Week 3:** ...
**Week 4:** ...

### 📚 Recommended Resources
(Books, websites, YouTube channels, courses — specific and free where possible)

### 💪 Daily Practice Routine
(What to do every day — realistic for a student)

### 📊 How to Measure Progress
(Specific checkpoints and self-assessment methods)
""", sys, max_tokens=2000)

def transcribe_audio(audio_bytes: bytes, filename: str) -> str:
    try:
        with tempfile.NamedTemporaryFile(
            suffix=os.path.splitext(filename)[1], delete=False
        ) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        with open(tmp_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model=STT_MODEL,
                file=(filename, f.read()),
                response_format="text",
            )
        os.unlink(tmp_path)
        return result if isinstance(result, str) else result.text
    except Exception as e:
        return f"❌ **Transcription Error:** {e}"

# ═══════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════
_D = {
    "active_tool":       "explain",
    "last_query":        "",
    "query_count":       0,
    "feedback":          {},
    "mh_history":        [],
    "mh_input":          "",
    "out_explain":       "", "out_quiz":       "", "out_suggest":    "",
    "out_notes":         "", "out_exam":       "", "out_verify":     "",
    "out_code":          "", "out_research":   "", "out_storyboard": "",
    "out_review":        "", "out_mentor":     "", "out_stt":        "",
    "live_transcript":   "",
    "explain_query_val": "",
}
for k, v in _D.items():
    if k not in st.session_state:
        st.session_state[k] = v

def reset():
    for k, v in _D.items():
        st.session_state[k] = v

# ═══════════════════════════════════════════════════════════════════
# UI HELPERS
# ═══════════════════════════════════════════════════════════════════
def wc(text: str) -> int:
    return len(text.split())

def out_block(content: str, badge_cls: str, badge_label: str,
              dl_key: str, dl_name: str):
    st.markdown(f"""
    <div class="out-meta">
        <span class="badge {badge_cls}">{badge_label}</span>
        <span class="badge bd-c">≈ {wc(content)} words</span>
    </div>""", unsafe_allow_html=True)
    if content.startswith("❌"):
        st.error(content)
    else:
        st.markdown(content)
    st.divider()
    c1, c2 = st.columns([2, 3])
    with c1:
        st.download_button("📥 Download .txt", data=content,
                           file_name=dl_name, mime="text/plain", key=dl_key)
    with c2:
        _feedback(dl_key)

def _feedback(key: str):
    fb = st.session_state["feedback"].get(key)
    if fb:
        col = "#16a34a" if fb == "👍" else "#e11d48"
        st.markdown(
            f'<p style="font-size:.8rem;font-weight:600;color:{col};margin:6px 0 0;">'
            f'{fb} Thanks for your feedback!</p>',
            unsafe_allow_html=True
        )
        return
    st.markdown('<span class="fb-lbl">Was this helpful?&nbsp;</span>',
                unsafe_allow_html=True)
    c1, c2, _ = st.columns([1, 1, 3])
    with c1:
        if st.button("👍", key=f"up_{key}"):
            st.session_state["feedback"][key] = "👍"
            st.rerun()
    with c2:
        if st.button("👎", key=f"dn_{key}"):
            st.session_state["feedback"][key] = "👎"
            st.rerun()

def validate(q: str) -> bool:
    if not q or len(q.strip()) < 3:
        st.warning("⚠️ Please enter a topic or question (at least 3 characters).")
        return False
    if len(q) > 4000:
        st.warning("⚠️ Input too long (>4000 chars). Please shorten it.")
        return False
    return True

def sec_div(label: str):
    st.markdown(f"""
    <div class="sec-div">
        <div class="sec-div-line"></div>
        <span class="sec-div-txt">{label}</span>
        <div class="sec-div-line"></div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sb-head">
            <p class="sb-head-title">🎓 AI Study Assistant</p>
            <p class="sb-head-sub">12 AI Tools · Groq LLaMA 3.3 · Whisper STT</p>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sb-sec">', unsafe_allow_html=True)
        st.markdown('<p class="sb-lbl">Session Stats</p>', unsafe_allow_html=True)
        up = sum(1 for v in st.session_state["feedback"].values() if v == "👍")
        st.markdown(f"""
        <div class="sb-stat-row">
          <div class="sb-stat">
            <span class="sb-stat-v">{st.session_state["query_count"]}</span>
            <span class="sb-stat-l">Queries</span>
          </div>
          <div class="sb-stat">
            <span class="sb-stat-v">{up}</span>
            <span class="sb-stat-l">Helpful</span>
          </div>
          <div class="sb-stat">
            <span class="sb-stat-v">12</span>
            <span class="sb-stat-l">Tools</span>
          </div>
        </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-sec">', unsafe_allow_html=True)
        st.markdown('<p class="sb-lbl">All Tools</p>', unsafe_allow_html=True)
        tools_meta = [
            ("ic-p","📘","Concept Explainer",   "English + Roman Urdu"),
            ("ic-a","📝","Quiz Generator",       "MCQs + short answer"),
            ("ic-t","🗺️","Topic Suggestions",    "Smart learning roadmap"),
            ("ic-s","📒","Notes Generator",      "Structured study notes"),
            ("ic-r","📄","Exam Paper Generator", "For teachers & students"),
            ("ic-v","🔍","Fake News Detector",   "Content credibility check"),
            ("ic-p","💚","Mental Health Chat",   "Emotion-aware companion"),
            ("ic-a","💻","Requirements→Code",    "AI code generator"),
            ("ic-t","📑","Research Summarizer",  "+ plagiarism corrector"),
            ("ic-s","🎬","Storyboard Creator",   "Visual scene planning"),
            ("ic-r","🔎","Code Reviewer",        "Bug explainer + fix"),
            ("ic-v","🎓","Learning Mentor",      "Personalized study plan"),
        ]
        for ic, emoji, name, desc in tools_meta:
            st.markdown(f"""
            <div class="sb-feat">
                <div class="sb-icon {ic}">{emoji}</div>
                <div><strong>{name}</strong><span>{desc}</span></div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="sb-sec">', unsafe_allow_html=True)
        st.markdown('<p class="sb-lbl">Model Info</p>', unsafe_allow_html=True)
        st.caption(f"LLM: `{LLM_MODEL}`")
        st.caption(f"STT: `{STT_MODEL}`")
        st.caption("Via Groq API (2025)")
        st.markdown('<p class="sb-lbl">Group Member:</p>', unsafe_allow_html=True)
        st.caption("SOHAIB QURESHI")
        st.caption("UZAIR RAFIQUE")
        st.caption("ABDUL QAYYUM")
        st.markdown('</div>', unsafe_allow_html=True)

        st.write("")
        if st.button("🗑️  Clear All", use_container_width=True):
            reset()
            st.rerun()

        st.markdown(
            '<div class="sb-footer">Built with ❤️ using Streamlit + Groq</div>',
            unsafe_allow_html=True
        )

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
def render_header():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">⚡ Groq LLaMA 3.3 · Whisper STT · 12 Tools</div>
        <h1 class="hero-title">AI <span>Study Assistant</span></h1>
        <p class="hero-sub">Your all-in-one AI tutor — explain, quiz, verify, code, and more.</p>
        <div class="hero-div"></div>
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TOOL GRID
# ═══════════════════════════════════════════════════════════════════
TOOLS = [
    ("explain",    "📘", "Concept Explainer",  "English + Roman Urdu"),
    ("quiz",       "📝", "Quiz Generator",      "MCQs & short answers"),
    ("suggest",    "🗺️", "Topic Suggestions",   "Smart roadmap"),
    ("notes",      "📒", "Notes Generator",     "Structured notes"),
    ("exam",       "📄", "Exam Paper",          "Full paper + key"),
    ("verify",     "🔍", "Fake News Detector",  "Credibility check"),
    ("mental",     "💚", "Mental Health Chat",  "Emotion-aware AI"),
    ("req2code",   "💻", "Req → Code",          "Auto code generator"),
    ("research",   "📑", "Research Summarizer", "+ plagiarism fixer"),
    ("storyboard", "🎬", "Storyboard Creator",  "Scene-by-scene plan"),
    ("codereview", "🔎", "Code Reviewer",       "Bugs + improvements"),
    ("mentor",     "🎓", "Learning Mentor",     "Personalized plan"),
]

def render_tool_grid():
    sec_div("Choose a Tool")
    cols = st.columns(6)
    for i, (key, icon, name, desc) in enumerate(TOOLS):
        active_cls = "active" if st.session_state["active_tool"] == key else ""
        with cols[i % 6]:
            st.markdown(f"""
            <div class="tool-card {active_cls}" id="tc_{key}">
                <div class="tool-card-icon">{icon}</div>
                <div class="tool-card-name">{name}</div>
                <div class="tool-card-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
            if st.button(name, key=f"tool_{key}", use_container_width=True, help=desc):
                st.session_state["active_tool"] = key
                st.rerun()

# ═══════════════════════════════════════════════════════════════════
# ACTIVE TOOL DISPATCHER
# ═══════════════════════════════════════════════════════════════════
def render_active_tool():
    tool = st.session_state["active_tool"]
    sec_div("Tool Workspace")

    if st.session_state["last_query"] and tool != "mental":
        q = st.session_state["last_query"][:120]
        st.markdown(f"""
        <div class="q-echo">
            <span class="q-lbl">Last query</span>
            <span class="q-txt">{q}</span>
        </div>""", unsafe_allow_html=True)

    if   tool == "explain":    _tool_explain()
    elif tool == "quiz":       _tool_quiz()
    elif tool == "suggest":    _tool_suggest()
    elif tool == "notes":      _tool_notes()
    elif tool == "exam":       _tool_exam()
    elif tool == "verify":     _tool_verify()
    elif tool == "mental":     _tool_mental()
    elif tool == "req2code":   _tool_req2code()
    elif tool == "research":   _tool_research()
    elif tool == "storyboard": _tool_storyboard()
    elif tool == "codereview": _tool_codereview()
    elif tool == "mentor":     _tool_mentor()

# ─── standard text-area helper ───────────────────────────────────
def _std_input(placeholder, height=108, key="q"):
    st.markdown('<div class="inp-card">', unsafe_allow_html=True)
    st.markdown('<p class="inp-lbl">📌 Your Input</p>', unsafe_allow_html=True)
    val = st.text_area(
        "q", placeholder=placeholder, height=height,
        key=f"inp_{key}", label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return val.strip()

# ═══════════════════════════════════════════════════════════════════
# TOOL PANELS
# ═══════════════════════════════════════════════════════════════════

def _tool_explain():
    st.markdown("### 📘 Concept Explainer")
    st.caption("Explains any topic in simple English + Roman Urdu with real-world examples.")

    with st.expander("🎤 Voice Input — Speak Your Question (Whisper STT)", expanded=False):
        tab_live, tab_upload = st.tabs(["🔴 Live Recording", "📁 Upload Audio File"])

        with tab_live:
            st.markdown(
                '<div class="audio-tab-info">🎙️ <strong>Live Recording:</strong> '
                'Click the microphone button below, speak your question, '
                'then press <em>Transcribe & Auto-Fill</em>.</div>',
                unsafe_allow_html=True
            )
            live_audio = st.audio_input("🎤 Click to record your question",
                                        key="live_mic_input")
            if live_audio is not None:
                if st.button("🎙️ Transcribe & Auto-Fill", key="btn_transcribe_live"):
                    with st.spinner("Transcribing your voice with Whisper…"):
                        transcript = transcribe_audio(live_audio.read(), "live_recording.wav")
                    if transcript.startswith("❌"):
                        st.error(transcript)
                    else:
                        st.session_state["explain_query_val"] = transcript
                        st.session_state["live_transcript"]   = transcript
                        st.session_state["out_stt"]           = transcript
                        st.rerun()

            if st.session_state.get("live_transcript"):
                st.success(f"✅ **Transcript filled below:** {st.session_state['live_transcript']}")
                if st.button("🗑️ Clear Transcript", key="clear_live_transcript"):
                    st.session_state["live_transcript"]   = ""
                    st.session_state["out_stt"]           = ""
                    st.session_state["explain_query_val"] = ""
                    st.rerun()

        with tab_upload:
            st.markdown(
                '<div class="audio-tab-info">📁 <strong>Upload Audio:</strong> '
                'Upload an existing audio file (mp3, wav, m4a, ogg, etc.) '
                'to transcribe it.</div>',
                unsafe_allow_html=True
            )
            audio_file = st.file_uploader(
                "Upload audio (mp3 / wav / m4a / ogg / webm / flac)",
                type=["mp3","wav","m4a","ogg","webm","flac"],
                key="stt_explain_upload"
            )
            if audio_file is not None:
                st.audio(audio_file, format=f"audio/{audio_file.name.split('.')[-1]}")
                if st.button("🎙️ Transcribe Uploaded File", key="btn_stt_explain_upload"):
                    with st.spinner("Transcribing with Whisper…"):
                        transcript = transcribe_audio(audio_file.read(), audio_file.name)
                    if transcript.startswith("❌"):
                        st.error(transcript)
                    else:
                        st.session_state["explain_query_val"] = transcript
                        st.session_state["out_stt"]           = transcript
                        st.rerun()

            if st.session_state.get("out_stt") and not st.session_state.get("live_transcript"):
                st.success(f"✅ **Transcript filled below:** {st.session_state['out_stt']}")

    if "explain_query_val" not in st.session_state:
        st.session_state["explain_query_val"] = ""

    st.markdown('<div class="inp-card">', unsafe_allow_html=True)
    st.markdown('<p class="inp-lbl">📌 Your Topic / Question</p>', unsafe_allow_html=True)
    st.text_area(
        "explain_q_label",
        placeholder="e.g. 'Explain photosynthesis', 'What is machine learning?'",
        height=108,
        key="explain_query_val",
        label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    query = st.session_state["explain_query_val"].strip()

    if st.button("📘 Explain Concept", key="run_explain", use_container_width=True):
        if validate(query):
            st.session_state["last_query"] = query
            with st.spinner("Thinking like a smart tutor…"):
                st.session_state["out_explain"] = explain_concept(query)
            st.session_state["query_count"] += 1
            st.session_state["feedback"].pop("ex_explain", None)
            st.rerun()

    if st.session_state["out_explain"]:
        out_block(st.session_state["out_explain"], "bd-p", "📘 Explanation",
                  "ex_explain", f"explanation_{query[:20]}.txt")


def _tool_quiz():
    st.markdown("### 📝 Quiz Generator")
    st.caption("3 MCQs + 1 short-answer question with correct answers.")
    query = _std_input("e.g. 'Python OOP', 'World War II causes'", key="quiz")
    if st.button("📝 Generate Quiz", key="run_quiz", use_container_width=True):
        if validate(query):
            st.session_state["last_query"] = query
            with st.spinner("Writing your personalised quiz…"):
                st.session_state["out_quiz"] = generate_quiz(query)
            st.session_state["query_count"] += 1
            st.session_state["feedback"].pop("ex_quiz", None)
            st.rerun()
    if st.session_state["out_quiz"]:
        out_block(st.session_state["out_quiz"], "bd-a", "📝 Quiz",
                  "ex_quiz", f"quiz_{query[:20]}.txt")


def _tool_suggest():
    st.markdown("### 🗺️ Topic Suggestions")
    st.caption("3 personalised next topics with difficulty ratings and reasons.")
    query = _std_input("e.g. 'I just learned about SQL joins'", key="suggest")
    if st.button("🗺️ Suggest Next Topics", key="run_suggest", use_container_width=True):
        if validate(query):
            st.session_state["last_query"] = query
            with st.spinner("Mapping your learning path…"):
                st.session_state["out_suggest"] = suggest_topics(query)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_suggest"]:
        out_block(st.session_state["out_suggest"], "bd-t", "🗺️ Suggestions",
                  "ex_suggest", f"roadmap_{query[:20]}.txt")


def _tool_notes():
    st.markdown("### 📒 Smart Notes Generator")
    st.caption("Structured, revision-ready study notes on any topic.")
    query = _std_input(
        "e.g. 'Cell division (mitosis & meiosis)', 'Newton's laws of motion'",
        key="notes"
    )
    if st.button("📒 Generate Notes", key="run_notes", use_container_width=True):
        if validate(query):
            st.session_state["last_query"] = query
            with st.spinner("Compiling your study notes…"):
                st.session_state["out_notes"] = generate_notes(query)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_notes"]:
        out_block(st.session_state["out_notes"], "bd-s", "📒 Study Notes",
                  "ex_notes", f"notes_{query[:20]}.txt")


def _tool_exam():
    st.markdown("### 📄 AI Exam Paper Generator")
    st.caption("Full exam paper (MCQs + Short + Long) with answer key — for teachers & students.")

    st.markdown('<div class="inp-card">', unsafe_allow_html=True)
    st.markdown('<p class="inp-lbl">📌 Exam Settings</p>', unsafe_allow_html=True)
    subject = st.text_input(
        "Subject / Topic",
        placeholder="e.g. Chemistry — Organic Compounds",
        key="exam_subject"
    )
    c1, c2 = st.columns(2)
    with c1:
        marks = st.selectbox("Total Marks", [25, 40, 50, 75, 100], index=2, key="exam_marks")
    with c2:
        etype = st.selectbox("Exam Type", ["Mid-Term","Final","Unit Test","Practice"],
                             key="exam_type")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("📄 Generate Exam Paper", key="run_exam", use_container_width=True):
        if validate(subject):
            st.session_state["last_query"] = subject
            with st.spinner("Creating exam paper…"):
                st.session_state["out_exam"] = generate_exam_paper(subject, marks, etype)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_exam"]:
        out_block(st.session_state["out_exam"], "bd-r", "📄 Exam Paper",
                  "ex_exam", f"exam_{subject[:20]}.txt")


def _tool_verify():
    st.markdown("### 🔍 AI Content Verification (Fake News Detector)")
    st.caption("Paste any article, post, or claim. Get a credibility report with verification steps.")
    query = _std_input(
        "Paste the article, news headline, social media post, or claim here…",
        height=160, key="verify"
    )
    if st.button("🔍 Analyse Content", key="run_verify", use_container_width=True):
        if validate(query):
            st.session_state["last_query"] = query[:60] + "…"
            with st.spinner("Analysing credibility…"):
                st.session_state["out_verify"] = verify_content(query)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_verify"]:
        out_block(st.session_state["out_verify"], "bd-r", "🔍 Credibility Report",
                  "ex_verify", "credibility_report.txt")


def _tool_mental():
    st.markdown("### 💚 AI Mental Health Chat Companion")
    st.caption(
        "A safe, judgement-free space to talk. "
        "This is a supportive AI — not a substitute for professional help."
    )
    st.info(
        "💙 **Reminder:** If you're in crisis, please contact a mental health professional "
        "or helpline. In Pakistan: **Umang helpline: 0317-4288665**"
    )

    chat_area = st.container()
    with chat_area:
        for msg in st.session_state["mh_history"]:
            role_label = "🧑 You" if msg["role"] == "user" else "💚 Companion"
            st.markdown(f"**{role_label}:** {msg['content']}")
        st.markdown("---")

    user_msg = st.text_input(
        "Your message…",
        key="mh_user_input",
        placeholder="How are you feeling today?"
    )
    c1, c2 = st.columns([2, 1])
    with c1:
        if st.button("💬 Send", key="run_mental", use_container_width=True):
            if user_msg.strip():
                st.session_state["mh_history"].append(
                    {"role": "user", "content": user_msg.strip()}
                )
                with st.spinner("Listening…"):
                    reply = mental_health_chat(user_msg.strip(),
                                               st.session_state["mh_history"])
                st.session_state["mh_history"].append(
                    {"role": "assistant", "content": reply}
                )
                st.session_state["query_count"] += 1
                st.rerun()
    with c2:
        if st.button("🗑️ Clear Chat", key="clear_mental", use_container_width=True):
            st.session_state["mh_history"] = []
            st.rerun()


def _tool_req2code():
    st.markdown("### 💻 Requirements → Code Generator")
    st.caption("Describe what you need in plain English. Get working, commented code instantly.")

    st.markdown('<div class="inp-card">', unsafe_allow_html=True)
    st.markdown('<p class="inp-lbl">📌 Code Settings</p>', unsafe_allow_html=True)
    lang = st.selectbox(
        "Programming Language",
        ["Python","JavaScript","TypeScript","Java","C++","C#",
         "Go","Rust","PHP","SQL","HTML/CSS","React"],
        key="req_lang"
    )
    req = st.text_area(
        "Describe what you want to build",
        placeholder=(
            "e.g. 'A Python function that reads a CSV, filters rows where age > 25, "
            "and saves the result to a new file'"
        ),
        height=120, key="inp_req2code", label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("💻 Generate Code", key="run_req2code", use_container_width=True):
        if validate(req):
            st.session_state["last_query"] = req[:60]
            with st.spinner(f"Writing {lang} code…"):
                st.session_state["out_code"] = requirements_to_code(req, lang)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_code"]:
        out_block(st.session_state["out_code"], "bd-p", "💻 Generated Code",
                  "ex_code", f"code_{lang.lower()}.txt")


def _tool_research():
    st.markdown("### 📑 Research Paper Summarizer + Plagiarism Corrector")
    st.caption("Paste abstract, paper section, or full text. Get a structured summary + paraphrased version.")
    query = _std_input(
        "Paste research paper text, abstract, or any academic content here…",
        height=180, key="research"
    )
    if st.button("📑 Summarize & Improve", key="run_research", use_container_width=True):
        if validate(query):
            st.session_state["last_query"] = "Research paper analysis"
            with st.spinner("Analysing research content…"):
                st.session_state["out_research"] = summarize_research(query)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_research"]:
        out_block(st.session_state["out_research"], "bd-t", "📑 Research Summary",
                  "ex_research", "research_summary.txt")


def _tool_storyboard():
    st.markdown("### 🎬 AI Storyboard Creator")
    st.caption("Turn any concept or story into a detailed visual storyboard with narration and mood.")

    st.markdown('<div class="inp-card">', unsafe_allow_html=True)
    st.markdown('<p class="inp-lbl">📌 Storyboard Settings</p>', unsafe_allow_html=True)
    concept = st.text_input(
        "Concept / Story / Topic",
        placeholder=(
            "e.g. 'How the immune system fights a virus', "
            "'A student's first day at university'"
        ),
        key="sb_concept"
    )
    scenes = st.slider("Number of Scenes", 3, 8, 5, key="sb_scenes")
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🎬 Create Storyboard", key="run_storyboard", use_container_width=True):
        if validate(concept):
            st.session_state["last_query"] = concept
            with st.spinner("Directing your storyboard…"):
                st.session_state["out_storyboard"] = create_storyboard(concept, scenes)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_storyboard"]:
        out_block(st.session_state["out_storyboard"], "bd-v", "🎬 Storyboard",
                  "ex_storyboard", f"storyboard_{concept[:20]}.txt")


def _tool_codereview():
    st.markdown("### 🔎 AI Code Reviewer & Bug Explainer")
    st.caption("Paste your code. Get bugs identified, explained, and fixed with an improved version.")

    st.markdown('<div class="inp-card">', unsafe_allow_html=True)
    st.markdown('<p class="inp-lbl">📌 Code Settings</p>', unsafe_allow_html=True)
    lang = st.selectbox(
        "Language",
        ["Python","JavaScript","TypeScript","Java","C++","C#","Go","PHP","SQL","Other"],
        key="cr_lang"
    )
    code = st.text_area(
        "Paste your code here",
        placeholder=(
            "def calculate_average(numbers):\n"
            "    total = 0\n"
            "    for n in numbers:\n"
            "        total =+ n  # bug here!\n"
            "    return total / len(numbers)"
        ),
        height=200, key="inp_codereview", label_visibility="collapsed"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔎 Review Code", key="run_codereview", use_container_width=True):
        if validate(code):
            st.session_state["last_query"] = f"{lang} code review"
            with st.spinner("Reviewing your code…"):
                st.session_state["out_review"] = review_code(code, lang)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_review"]:
        out_block(st.session_state["out_review"], "bd-o", "🔎 Code Review",
                  "ex_review", f"code_review_{lang.lower()}.txt")


def _tool_mentor():
    st.markdown("### 🎓 AI Learning Mentor — Personalized Plan")
    st.caption("Tell the AI your goal and current level. Get a full week-by-week learning plan.")

    st.markdown('<div class="inp-card">', unsafe_allow_html=True)
    st.markdown('<p class="inp-lbl">📌 Your Learning Profile</p>', unsafe_allow_html=True)
    goal = st.text_input(
        "What do you want to learn / achieve?",
        placeholder="e.g. 'Become proficient in Python for data science in 3 months'",
        key="mentor_goal"
    )
    c1, c2 = st.columns(2)
    with c1:
        level = st.selectbox(
            "Current Level",
            ["Complete Beginner","Beginner","Intermediate","Advanced"],
            key="mentor_level"
        )
    with c2:
        style = st.selectbox(
            "Learning Style",
            ["Visual (videos, diagrams)","Reading (books, articles)",
             "Hands-on (projects, coding)","Mixed"],
            key="mentor_style"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🎓 Create My Plan", key="run_mentor", use_container_width=True):
        if validate(goal):
            st.session_state["last_query"] = goal
            with st.spinner("Building your personalised plan…"):
                st.session_state["out_mentor"] = learning_mentor(goal, level, style)
            st.session_state["query_count"] += 1
            st.rerun()
    if st.session_state["out_mentor"]:
        out_block(st.session_state["out_mentor"], "bd-g", "🎓 Learning Plan",
                  "ex_mentor", f"learning_plan_{goal[:20]}.txt")


# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════
def main():
    render_sidebar()
    _, col, _ = st.columns([0.3, 9.4, 0.3])
    with col:
        render_header()
        render_tool_grid()
        render_active_tool()

if __name__ == "__main__":
    main()
