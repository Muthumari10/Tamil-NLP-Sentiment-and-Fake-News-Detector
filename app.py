import streamlit as st
import joblib
import re

st.set_page_config(
    page_title="Tamil NLP Detector",
    page_icon="🔍",
    layout="wide"
)

# ── Shared CSS (used on BOTH pages) ──────────────────────────
SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; }

.hero-banner {
    background: linear-gradient(135deg, #FF6B35, #F7C59F, #004E89, #1A936F, #FF6B35);
    background-size: 300% 300%;
    animation: gradientShift 6s ease infinite;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
    position: relative;
    overflow: hidden;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
.hero-watermark-top {
    position: absolute; top: 8px; left: 0; right: 0;
    font-size: 10px; color: rgba(255,255,255,0.25);
    letter-spacing: 6px; font-family: 'Noto Sans Tamil', sans-serif;
    text-align: center;
}
.hero-watermark-bot {
    position: absolute; bottom: 8px; left: 0; right: 0;
    font-size: 10px; color: rgba(255,255,255,0.25);
    letter-spacing: 6px; font-family: 'Noto Sans Tamil', sans-serif;
    text-align: center;
}
.hero-title { font-size:2.8rem; font-weight:700; color:white; text-shadow:0 2px 20px rgba(0,0,0,0.5); margin:0; line-height:1.2; }
.hero-tamil { font-family:'Noto Sans Tamil',sans-serif; font-size:1.3rem; color:rgba(255,255,255,0.95); margin-top:0.4rem; text-shadow:0 1px 8px rgba(0,0,0,0.3); }
.hero-sub   { font-size:1rem; color:rgba(255,255,255,0.85); margin-top:0.5rem; font-weight:300; }

.stat-box   { background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.13); border-radius:12px; padding:1rem; text-align:center; }
.stat-num   { font-size:1.8rem; font-weight:700; color:white; }
.stat-label { font-size:0.72rem; color:rgba(255,255,255,0.5); text-transform:uppercase; letter-spacing:1px; margin-top:2px; }

.section-title { color:rgba(255,255,255,0.45); font-size:0.7rem; text-transform:uppercase; letter-spacing:2px; margin-bottom:0.8rem; font-weight:500; }
.glass-card { background:rgba(255,255,255,0.07); border:1px solid rgba(255,255,255,0.13); border-radius:14px; padding:1.2rem; margin-bottom:1rem; }

div[data-testid="stButton"] button {
    background: rgba(255,255,255,0.1) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 50px !important;
    font-size: 0.82rem !important;
    font-family: 'Noto Sans Tamil', sans-serif !important;
    transition: all 0.2s ease !important;
    box-shadow: none !important;
}
div[data-testid="stButton"] button:hover {
    background: rgba(255,255,255,0.22) !important;
    border-color: rgba(255,255,255,0.5) !important;
    transform: scale(1.04) !important;
}
div[data-testid="stButton"]:has(button[kind="primary"]) button {
    background: linear-gradient(135deg, #FF6B35, #F7931E) !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px rgba(255,107,53,0.4) !important;
    color: white !important;
}

.stTextArea > div > div > textarea,
.stTextArea textarea,
textarea {
    background-color: rgba(40,40,80,0.95) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border: 2px solid rgba(255,255,255,0.3) !important;
    border-radius: 12px !important;
    font-size: 1.05rem !important;
    font-family: 'Noto Sans Tamil', sans-serif !important;
    padding: 1rem !important;
    caret-color: #FF6B35 !important;
}
.stTextArea > div > div > textarea:focus,
textarea:focus {
    border-color: #FF6B35 !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,0.25) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    outline: none !important;
}
textarea::placeholder {
    color: rgba(255,255,255,0.35) !important;
    -webkit-text-fill-color: rgba(255,255,255,0.35) !important;
}

.tamil-warning {
    background: rgba(255,165,0,0.15);
    border: 1px solid rgba(255,165,0,0.4);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #FFD580;
    font-family: 'Noto Sans Tamil', sans-serif;
    font-size: 0.9rem;
    margin: 0.5rem 0;
}

.result-box {
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 2.5rem 2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
    margin: 1rem 0;
}
.result-badge { border-radius:50px; padding:0.6rem 1.8rem; font-size:1.2rem; font-weight:700; color:white; display:inline-block; letter-spacing:1px; text-transform:uppercase; box-shadow:0 4px 20px rgba(0,0,0,0.3); }
.badge-positive { background: linear-gradient(135deg,#11998e,#38ef7d); }
.badge-negative { background: linear-gradient(135deg,#c0392b,#e74c3c); }
.badge-fake     { background: linear-gradient(135deg,#f39c12,#f1c40f); }
.badge-real     { background: linear-gradient(135deg,#2980b9,#3498db); }
.confidence-big { font-size:3.5rem; font-weight:700; color:white; margin:0.5rem 0; }
.result-message { color:rgba(255,255,255,0.8); font-size:1rem; margin-top:0.8rem; font-family:'Noto Sans Tamil',sans-serif; line-height:1.7; }

.conf-label { display:flex; justify-content:space-between; color:rgba(255,255,255,0.7); font-size:0.85rem; margin-bottom:4px; }
.conf-bar-container { background:rgba(255,255,255,0.08); border-radius:50px; height:12px; overflow:hidden; margin-bottom:12px; }
.conf-bar-pos { background:linear-gradient(90deg,#11998e,#38ef7d); height:100%; border-radius:50px; }
.conf-bar-neg { background:linear-gradient(90deg,#c0392b,#e74c3c); height:100%; border-radius:50px; }
.conf-bar-fk  { background:linear-gradient(90deg,#f39c12,#f1c40f); height:100%; border-radius:50px; }
.conf-bar-rl  { background:linear-gradient(90deg,#2980b9,#3498db); height:100%; border-radius:50px; }

.history-item { background:rgba(255,255,255,0.05); border-radius:10px; padding:0.6rem 1rem; margin:0.3rem 0; font-size:0.85rem; color:rgba(255,255,255,0.7); border-left:3px solid; font-family:'Noto Sans Tamil',sans-serif; }

.back-btn-wrap { margin-bottom: 1.5rem; }

#MainMenu { visibility:hidden; }
footer    { visibility:hidden; }
header    { visibility:hidden; }
</style>
"""

# ── Load model ───────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load('tamil_nlp_model.pkl')

model = load_model()

# ── Tamil detection ──────────────────────────────────────────
def is_tamil(text):
    """Returns True ONLY if text contains Tamil Unicode characters (rejects numbers/symbols/English)."""
    tamil_pattern = re.compile(r'[\u0B80-\u0BFF]')
    tamil_chars = len(tamil_pattern.findall(text))
    if tamil_chars == 0:
        return False
    total_alpha = len(re.findall(r'[a-zA-Z\u0B80-\u0BFF]', text))
    if total_alpha == 0:
        return True
    return tamil_chars / total_alpha >= 0.3

# ── Session state ────────────────────────────────────────────
for key, val in {
    'history': [],
    'total_analyzed': 0,
    'selected_example': "",
    'last_result': None,
    'show_warning': False,
    'page': 'home',          # 'home' or 'result'
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ════════════════════════════════════════════════════════════
#  PAGE: RESULT
# ════════════════════════════════════════════════════════════
def show_result_page():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)

    r          = st.session_state.last_result
    prediction = r["prediction"]
    confidence = r["confidence"]
    proba      = r["proba"]
    classes    = r["classes"]

    label_config = {
        "positive": {
            "emoji":"✅","name":"POSITIVE — நேர்மறை","badge":"badge-positive",
            "msg_ta":"இந்த வாக்கியம் மகிழ்ச்சி, வெற்றி அல்லது நன்றி உணர்வை வெளிப்படுத்துகிறது.",
            "msg_en":"This text expresses happiness, achievement, or appreciation.",
            "glow":"rgba(56,239,125,0.25)"
        },
        "negative": {
            "emoji":"❌","name":"NEGATIVE — எதிர்மறை","badge":"badge-negative",
            "msg_ta":"இந்த வாக்கியம் சோகம், கோபம் அல்லது புகார் உணர்வை வெளிப்படுத்துகிறது.",
            "msg_en":"This text expresses sadness, frustration, or complaint.",
            "glow":"rgba(231,76,60,0.25)"
        },
        "fake": {
            "emoji":"⚠️","name":"FAKE NEWS — தவறான செய்தி","badge":"badge-fake",
            "msg_ta":"இந்த வாக்கியம் தவறான தகவல் அல்லது WhatsApp வதந்தியாக இருக்கலாம்.",
            "msg_en":"This text appears to be misinformation, scam, or WhatsApp forward.",
            "glow":"rgba(241,196,15,0.25)"
        },
        "real": {
            "emoji":"📰","name":"REAL NEWS — உண்மையான செய்தி","badge":"badge-real",
            "msg_ta":"இந்த வாக்கியம் உண்மையான செய்தி அல்லது அரசு அறிவிப்பாக இருக்கலாம்.",
            "msg_en":"This text resembles verified news or government announcement.",
            "glow":"rgba(52,152,219,0.25)"
        },
    }
    cfg = label_config[prediction]

    # ── Hero (result variant) ────────────────────────────────
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-watermark-top">தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ்</div>
        <div class="hero-title">🔍 Tamil NLP Detector</div>
        <div class="hero-tamil">பகுப்பாய்வு முடிவு — Analysis Result</div>
        <div class="hero-sub">Sentiment Analysis · Fake News Detection · Real News Verification</div>
        <div class="hero-watermark-bot">தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ்</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Stats row ────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="stat-box"><div class="stat-num">820</div><div class="stat-label">Training Rows</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-box"><div class="stat-num">4</div><div class="stat-label">Label Classes</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{st.session_state.total_analyzed}</div><div class="stat-label">Analyzed Today</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="stat-box"><div class="stat-num">TF-IDF</div><div class="stat-label">Model Type</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Two-column layout (mirrors home page) ───────────────
    left_col, right_col = st.columns([3, 2])

    with left_col:

        # Back button
        st.markdown('<div class="back-btn-wrap">', unsafe_allow_html=True)
        if st.button("← Back — புதிய உரை பகுப்பாய்வு செய்", use_container_width=True):
            st.session_state.page             = 'home'
            st.session_state.last_result      = None
            st.session_state.selected_example = ""
            st.session_state.show_warning     = False
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Main result card
        st.markdown(f"""
        <div class="result-box" style="box-shadow: 0 0 60px {cfg['glow']};">
            <div style="font-size:4.5rem;margin-bottom:0.5rem">{cfg['emoji']}</div>
            <div class="result-badge {cfg['badge']}">{cfg['name']}</div>
            <div class="confidence-big">{confidence}%</div>
            <div style="color:rgba(255,255,255,0.4);font-size:0.82rem;margin-bottom:1rem">
                Confidence Score — நம்பகத்தன்மை
            </div>
            <div class="result-message">
                {cfg['msg_ta']}<br>
                <span style="opacity:0.6;font-family:Inter;font-size:0.88rem">{cfg['msg_en']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Confidence breakdown bars
        st.markdown('<div class="section-title" style="margin-top:1.5rem">📊 Confidence Breakdown — நம்பகத்தன்மை விவரம்</div>', unsafe_allow_html=True)
        bar_map  = {"positive":"conf-bar-pos","negative":"conf-bar-neg","fake":"conf-bar-fk","real":"conf-bar-rl"}
        name_map = {"positive":"✅ Positive","negative":"❌ Negative","fake":"⚠️ Fake","real":"📰 Real"}
        for lbl, prob in sorted(zip(classes, proba), key=lambda x: -x[1]):
            pct = round(prob * 100, 1)
            st.markdown(f"""
            <div class="conf-label">
                <span>{name_map[lbl]}</span>
                <span style="font-weight:600;color:white">{pct}%</span>
            </div>
            <div class="conf-bar-container">
                <div class="{bar_map[lbl]}" style="width:{pct}%"></div>
            </div>
            """, unsafe_allow_html=True)

        # Analyzed text preview
        st.markdown(f"""
        <div class="glass-card" style="margin-top:1.2rem">
            <div style="color:rgba(255,255,255,0.4);font-size:0.72rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px">📄 Analyzed Text — பகுப்பாய்வு செய்யப்பட்ட உரை</div>
            <div style="color:white;font-family:'Noto Sans Tamil',sans-serif;font-size:1rem;line-height:1.7">{r['text']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Analyze new text button at the bottom
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔎 Analyze New Text — புதிய உரை", use_container_width=True, type="primary"):
            st.session_state.page             = 'home'
            st.session_state.last_result      = None
            st.session_state.selected_example = ""
            st.session_state.show_warning     = False
            st.rerun()

    with right_col:

        # Label meanings
        st.markdown('<div class="section-title">📖 What Each Label Means</div>', unsafe_allow_html=True)
        labels_info = [
            ("✅","Positive — நேர்மறை","#38ef7d","Happy, achieved, grateful, love, success","மகிழ்ச்சி, வெற்றி, நன்றி, அன்பு உணர்வுகள்"),
            ("❌","Negative — எதிர்மறை","#e74c3c","Sad, frustrated, complaint, loss, loneliness","சோகம், கோபம், புகார், தோல்வி, தனிமை"),
            ("⚠️","Fake — தவறான","#f1c40f","WhatsApp scams, false health cures, fake schemes","WhatsApp மோசடி, போலி மருத்துவம், தவறான திட்டம்"),
            ("📰","Real — உண்மையான","#3498db","Verified news, court orders, govt announcements","உண்மையான செய்தி, நீதிமன்றம், அரசு அறிவிப்பு"),
        ]
        for emoji, name, color, desc_en, desc_ta in labels_info:
            # Highlight the current prediction
            border = f"border: 1px solid {color}; box-shadow: 0 0 12px {color}33;" if name.split("—")[0].strip() == cfg['name'].split("—")[0].strip() else ""
            st.markdown(f"""
            <div class="glass-card" style="{border}">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                    <span style="font-size:1.3rem">{emoji}</span>
                    <span style="color:white;font-weight:600;font-size:0.88rem">{name}</span>
                </div>
                <div style="color:rgba(255,255,255,0.6);font-size:0.78rem">{desc_en}</div>
                <div style="color:{color};font-size:0.78rem;font-family:'Noto Sans Tamil',sans-serif;margin-top:3px">{desc_ta}</div>
            </div>
            """, unsafe_allow_html=True)

        # Recent history
        if st.session_state.history:
            st.markdown('<div class="section-title" style="margin-top:1rem">🕐 Recent Analysis</div>', unsafe_allow_html=True)
            border_colors = {"positive":"#38ef7d","negative":"#e74c3c","fake":"#f1c40f","real":"#3498db"}
            label_emojis  = {"positive":"✅","negative":"❌","fake":"⚠️","real":"📰"}
            for item in st.session_state.history:
                bc = border_colors.get(item['label'], '#fff')
                em = label_emojis.get(item['label'], '🔍')
                st.markdown(f"""
                <div class="history-item" style="border-left-color:{bc}">
                    {em} <strong style="color:white">{item['conf']}%</strong> · {item['text']}
                </div>
                """, unsafe_allow_html=True)

        # Dataset links
        st.markdown('<div class="section-title" style="margin-top:1rem">🔗 Dataset Links</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <div style="color:rgba(255,255,255,0.8);font-size:0.85rem;line-height:2.2">
                📦 <strong style="color:white">820 rows</strong> · 4 balanced labels<br>
                🌐 Formal + Colloquial Tamil<br>
                📊 <a href="https://www.kaggle.com/datasets/muthumarii/tamil-nlp-sentiment-and-fake-news-dataset" target="_blank" style="color:#3498db;text-decoration:none">View on Kaggle ↗</a><br>
                🤗 <a href="https://huggingface.co/datasets/Muthumari10/tamil-nlp-sentiment-and-fake-news-dataset" target="_blank" style="color:#ff7c7c;text-decoration:none">View on Hugging Face ↗</a><br>
                🔤 UTF-8 · Seed 42 · CC BY 4.0
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;color:rgba(255,255,255,0.2);font-size:0.75rem;padding:1.5rem;margin-top:1rem">
        🔍 Tamil NLP Detector · Built by Sudalaimuthumari M · Streamlit<br>
        <span style="font-family:'Noto Sans Tamil',sans-serif;font-size:0.85rem;opacity:0.5">தமிழ் · அறிவியல் · தொழில்நுட்பம்</span>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  PAGE: HOME
# ════════════════════════════════════════════════════════════
def show_home_page():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-watermark-top">தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ்</div>
        <div class="hero-title">🔍 Tamil NLP Detector</div>
        <div class="hero-tamil">தமிழ் உரை பகுப்பாய்வி</div>
        <div class="hero-sub">Sentiment Analysis · Fake News Detection · Real News Verification</div>
        <div class="hero-watermark-bot">தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ் • தமிழ்</div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="stat-box"><div class="stat-num">820</div><div class="stat-label">Training Rows</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="stat-box"><div class="stat-num">4</div><div class="stat-label">Label Classes</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="stat-box"><div class="stat-num">{st.session_state.total_analyzed}</div><div class="stat-label">Analyzed Today</div></div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="stat-box"><div class="stat-num">TF-IDF</div><div class="stat-label">Model Type</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    left_col, right_col = st.columns([3, 2])

    with left_col:

        st.markdown('<div class="section-title">⚡ Click any example to auto-fill</div>', unsafe_allow_html=True)

        examples = [
            ("😊 இன்று மகிழ்ச்சி",  "இன்று மிகவும் மகிழ்ச்சியாக இருக்கிறேன்"),
            ("😢 வேலை போச்சு",       "வேலை போய்விட்டது என்ன செய்வதென்று தெரியவில்லை"),
            ("⚠️ இலவச தங்கம்",       "அரசு இலவச தங்கம் வழங்குகிறது உடனே பதிவு செய்யுங்கள்"),
            ("📰 சட்டமன்றம்",        "தமிழ்நாடு சட்டமன்றம் புதிய சட்டம் நிறைவேற்றியது"),
            ("🌟 கனவு நனவாச்சு",     "என் கனவு நனவாகிறது மகிழ்ச்சி தாங்கவில்லை"),
            ("💔 தனிமை",             "யாரும் என்னை புரிந்துகொள்வதில்லை தனிமை கொல்கிறது"),
            ("🚨 WhatsApp மோசடி",    "WhatsApp செய்தி அனுப்பினால் 5000 ரூபாய் கிடைக்கும்"),
            ("📡 கிரிக்கெட் வெற்றி", "இந்திய கிரிக்கெட் அணி தொடரில் வெற்றி பெற்றது"),
        ]

        row1 = st.columns(4)
        row2 = st.columns(4)
        for i, (label, text) in enumerate(examples):
            col = row1[i] if i < 4 else row2[i - 4]
            with col:
                if st.button(label, key=f"ex_{i}", use_container_width=True):
                    st.session_state.selected_example = text
                    st.session_state.last_result = None
                    st.session_state.show_warning = False
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="section-title">✍️ Enter Tamil Text — தமிழ் உரையை உள்ளிடுங்கள்</div>', unsafe_allow_html=True)

        if st.session_state.selected_example:
            st.info(f"📌 Loaded: **{st.session_state.selected_example}**")

        user_input = st.text_area(
            label="",
            label_visibility="collapsed",
            value=st.session_state.selected_example,
            height=140,
            placeholder="உங்கள் தமிழ் வாக்கியம் இங்கே தட்டச்சு செய்யுங்கள்...\nType your Tamil sentence here...",
            key="text_input_box"
        )

        st.caption(f"📝 Characters: {len(user_input.strip())}")

        if st.session_state.show_warning:
            st.markdown("""
            <div class="tamil-warning">
                ⚠️ தமிழ் மொழியில் மட்டுமே உரையை உள்ளிடுங்கள்.<br>
                <span style="font-family:Inter;font-size:0.82rem;opacity:0.8">
                Please enter text in Tamil script only. English, numbers, or symbols alone are not supported.
                </span>
            </div>
            """, unsafe_allow_html=True)

        analyze = st.button(
            "🔎  Analyze Text — பகுப்பாய்வு செய்",
            use_container_width=True,
            type="primary"
        )

        if analyze:
            if user_input.strip() == "":
                st.session_state.show_warning = True
                st.session_state.last_result  = None
            elif not is_tamil(user_input.strip()):
                st.session_state.show_warning = True
                st.session_state.last_result  = None
            else:
                st.session_state.show_warning = False
                prediction = model.predict([user_input])[0]
                proba      = model.predict_proba([user_input])[0]
                confidence = round(max(proba) * 100, 2)
                classes    = model.classes_

                st.session_state.total_analyzed += 1
                st.session_state.last_result = {
                    "text":       user_input,
                    "prediction": prediction,
                    "confidence": confidence,
                    "proba":      list(proba),
                    "classes":    list(classes)
                }
                st.session_state.history.insert(0, {
                    "text":  user_input[:55] + ("..." if len(user_input) > 55 else ""),
                    "label": prediction,
                    "conf":  confidence
                })
                if len(st.session_state.history) > 5:
                    st.session_state.history = st.session_state.history[:5]

                # ── Navigate to result page ──────────────────
                st.session_state.page = 'result'

            st.rerun()

    with right_col:

        st.markdown('<div class="section-title">📖 What Each Label Means</div>', unsafe_allow_html=True)
        labels_info = [
            ("✅","Positive — நேர்மறை","#38ef7d","Happy, achieved, grateful, love, success","மகிழ்ச்சி, வெற்றி, நன்றி, அன்பு உணர்வுகள்"),
            ("❌","Negative — எதிர்மறை","#e74c3c","Sad, frustrated, complaint, loss, loneliness","சோகம், கோபம், புகார், தோல்வி, தனிமை"),
            ("⚠️","Fake — தவறான","#f1c40f","WhatsApp scams, false health cures, fake schemes","WhatsApp மோசடி, போலி மருத்துவம், தவறான திட்டம்"),
            ("📰","Real — உண்மையான","#3498db","Verified news, court orders, govt announcements","உண்மையான செய்தி, நீதிமன்றம், அரசு அறிவிப்பு"),
        ]
        for emoji, name, color, desc_en, desc_ta in labels_info:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px">
                    <span style="font-size:1.3rem">{emoji}</span>
                    <span style="color:white;font-weight:600;font-size:0.88rem">{name}</span>
                </div>
                <div style="color:rgba(255,255,255,0.6);font-size:0.78rem">{desc_en}</div>
                <div style="color:{color};font-size:0.78rem;font-family:'Noto Sans Tamil',sans-serif;margin-top:3px">{desc_ta}</div>
            </div>
            """, unsafe_allow_html=True)

        if st.session_state.history:
            st.markdown('<div class="section-title" style="margin-top:1rem">🕐 Recent Analysis</div>', unsafe_allow_html=True)
            border_colors = {"positive":"#38ef7d","negative":"#e74c3c","fake":"#f1c40f","real":"#3498db"}
            label_emojis  = {"positive":"✅","negative":"❌","fake":"⚠️","real":"📰"}
            for item in st.session_state.history:
                bc = border_colors.get(item['label'], '#fff')
                em = label_emojis.get(item['label'], '🔍')
                st.markdown(f"""
                <div class="history-item" style="border-left-color:{bc}">
                    {em} <strong style="color:white">{item['conf']}%</strong> · {item['text']}
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:1rem">🔗 Dataset Links</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="glass-card">
            <div style="color:rgba(255,255,255,0.8);font-size:0.85rem;line-height:2.2">
                📦 <strong style="color:white">820 rows</strong> · 4 balanced labels<br>
                🌐 Formal + Colloquial Tamil<br>
                📊 <a href="https://www.kaggle.com/datasets/muthumarii/tamil-nlp-sentiment-and-fake-news-dataset" target="_blank" style="color:#3498db;text-decoration:none">View on Kaggle ↗</a><br>
                🤗 <a href="https://huggingface.co/datasets/Muthumari10/tamil-nlp-sentiment-and-fake-news-dataset" target="_blank" style="color:#ff7c7c;text-decoration:none">View on Hugging Face ↗</a><br>
                🔤 UTF-8 · Seed 42 · CC BY 4.0
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;color:rgba(255,255,255,0.2);font-size:0.75rem;padding:1.5rem;margin-top:1rem">
        🔍 Tamil NLP Detector · Built by Sudalaimuthumari M · Streamlit<br>
        <span style="font-family:'Noto Sans Tamil',sans-serif;font-size:0.85rem;opacity:0.5">தமிழ் · அறிவியல் · தொழில்நுட்பம்</span>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  ROUTER — decides which page to render
# ════════════════════════════════════════════════════════════
if st.session_state.page == 'result' and st.session_state.last_result:
    show_result_page()
else:
    show_home_page()