import base64
import urllib.parse
import requests
import streamlit as st

API_BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="உழுதுண்டு வாழ்வாரே | Uzhudhuntu Vaazhvaare",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "lang" not in st.session_state:
    st.session_state.lang = "Tamil"

if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_audio_id" not in st.session_state:
    st.session_state.last_audio_id = None

is_ta = st.session_state.lang == "Tamil"

# --- Compact & Clean UI Styling ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Tamil:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', 'Noto Sans Tamil', sans-serif !important;
    }

    header[data-testid="stHeader"],
    [data-testid="stAppHeader"],
    [data-testid="stToolbar"],
    [data-testid="stToolbarActions"],
    [data-testid="stDeployButton"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stAppDeployButton,
    #MainMenu,
    footer,
    a[href="#main-content"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        min-height: 0 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #FAFCFA !important;
        border-right: 1.5px solid #DCE7DD !important;
        padding-top: 0.5rem !important;
    }

    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main {
        background: radial-gradient(circle at top right, #ECFDF5 0%, #F4F7F0 45%, #EEF3E8 100%) !important;
        color: #111827 !important;
        overflow-x: hidden !important;
    }
    [data-testid="stMainBlockContainer"],
    .block-container {
        max-width: 1180px !important;
        padding-top: 0.4rem !important;
        padding-bottom: 0.4rem !important;
        padding-left: 1.2rem !important;
        padding-right: 1.2rem !important;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0.35rem !important;
    }

    .kural-marquee {
        width: 100%;
        overflow: hidden;
        background: linear-gradient(90deg, #0D3B20 0%, #14532D 50%, #0D3B20 100%);
        color: #FEF08A;
        border-radius: 8px;
        padding: 4px 0;
        border: 1px solid #166534;
        box-shadow: 0 1px 6px rgba(13, 59, 32, 0.1);
    }
    .kural-track {
        display: inline-block;
        white-space: nowrap;
        padding-left: 100%;
        animation: scrollKural 44s linear infinite;
        font-size: 0.8rem;
        font-weight: 600;
    }
    @keyframes scrollKural {
        0%   { transform: translate3d(0, 0, 0); }
        100% { transform: translate3d(-100%, 0, 0); }
    }
    .kural-dot {
        color: #4ADE80;
        margin: 0 20px;
        font-weight: 800;
    }

    .sort-card {
        background: #FFFFFF;
        border: 1.5px solid #D5E3D7;
        border-radius: 12px;
        padding: 8px 12px;
        box-shadow: 0 2px 6px rgba(20, 83, 45, 0.03);
        height: 76px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .sort-card-title {
        font-size: 0.92rem;
        font-weight: 800;
        color: #14532D;
        margin-bottom: 2px;
    }
    .sort-card-desc {
        font-size: 0.74rem;
        color: #4B5563;
        line-height: 1.2;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }

    div.stButton > button {
        height: 32px !important;
        min-height: 32px !important;
        padding: 0 10px !important;
        font-size: 0.8rem !important;
        border-radius: 8px !important;
    }
    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #14532D 0%, #166534 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #14532D !important;
        font-weight: 700 !important;
    }
    div.stButton > button[kind="secondary"] {
        background-color: #FFFFFF !important;
        color: #14532D !important;
        border: 1.5px solid #C6DEC9 !important;
        font-weight: 600 !important;
    }

    [data-testid="stAudioInput"] > div {
        height: 42px !important;
        min-height: 42px !important;
        border-radius: 12px !important;
        border: 1.5px solid #C6DEC9 !important;
        background-color: #FFFFFF !important;
        display: flex !important;
        align-items: center !important;
        padding: 0 10px !important;
    }
    [data-testid="stChatInput"] {
        padding: 0 !important;
    }
    [data-testid="stChatInput"] > div {
        height: 42px !important;
        min-height: 42px !important;
        border-radius: 12px !important;
        border: 1.5px solid #C6DEC9 !important;
        background-color: #FFFFFF !important;
        display: flex !important;
        align-items: center !important;
    }
    [data-testid="stChatInput"] textarea {
        height: 38px !important;
        min-height: 38px !important;
        padding-top: 8px !important;
        padding-bottom: 8px !important;
        font-size: 0.88rem !important;
    }

    .welcome-empty {
        background: linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%);
        border: 1px dashed #86EFAC;
        border-radius: 12px;
        padding: 12px 16px;
        text-align: center;
        margin: 6px auto;
        max-width: 650px;
    }
    .welcome-empty h4 {
        color: #14532D;
        margin: 0 0 4px 0;
        font-size: 0.96rem;
        font-weight: 800;
    }
    .welcome-empty p {
        color: #374151;
        margin: 0 0 6px 0;
        font-size: 0.82rem;
    }
    .sample-chip {
        display: inline-block;
        background: #DCFCE7;
        color: #14532D;
        font-size: 0.74rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 999px;
        margin: 2px 3px;
    }

    .answer-card {
        background: #FFFFFF;
        border: 1.5px solid #CFE0D2;
        border-radius: 12px;
        padding: 10px 14px;
        margin: 2px 0 6px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .answer-title {
        font-size: 0.98rem;
        font-weight: 800;
        color: #14532D;
        border-bottom: 1px solid #E5EFE7;
        padding-bottom: 4px;
        margin-bottom: 6px;
    }
    .benefit-strip {
        background: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 7px 10px;
        border-radius: 6px;
        font-size: 0.86rem;
        margin-bottom: 6px;
    }
    .contact-strip {
        background: #FEFCE8;
        border-left: 4px solid #CA8A04;
        padding: 6px 10px;
        border-radius: 6px;
        font-size: 0.82rem;
        margin-top: 6px;
    }
    .wa-share {
        display: inline-block;
        background-color: #25D366;
        color: #FFFFFF !important;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.78rem;
        padding: 5px 12px;
        border-radius: 6px;
        margin-top: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(ttl=15)
def get_indexed_pdfs():
    try:
        r = requests.get(f"{API_BASE_URL}/indexed-pdfs", timeout=3)
        r.raise_for_status()
        return r.json()
    except Exception:
        return {"total_files": 0, "files": [], "offline": True}


def upload_scheme_pdf(uploaded_file):
    try:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
        r = requests.post(f"{API_BASE_URL}/upload-pdf", files=files, timeout=120)
        if r.status_code != 200:
            return False, r.json().get("detail", r.text)
        return True, r.json().get("message", "PDF indexed!")
    except Exception as e:
        return False, str(e)


def trigger_sync_data(rebuild: bool = False):
    try:
        r = requests.post(
            f"{API_BASE_URL}/sync-data-folder",
            params={"rebuild": rebuild},
            timeout=120,
        )
        r.raise_for_status()
        return True, r.json().get("message", "Synced!")
    except Exception as e:
        return False, str(e)


def query_backend_text(question: str, language: str) -> dict:
    try:
        r = requests.post(
            f"{API_BASE_URL}/query",
            json={"query": question, "language": language},
            timeout=30,
        )
        if r.status_code != 200:
            detail = r.json().get("detail", r.text)
            return {
                "scheme_title": "Backend Error",
                "benefit_summary": f"⚠️ {detail}",
                "eligibility_points": [],
                "contact_action": "Check FastAPI terminal.",
                "sources": [],
                "audio_base64": None,
            }
        return r.json()
    except Exception as e:
        return {
            "scheme_title": "Backend Offline",
            "benefit_summary": f"⚠️ Could not connect to FastAPI on port 8000: {e}",
            "eligibility_points": [],
            "contact_action": "Run: python -m uvicorn backend.main:app --reload --port 8000",
            "sources": [],
            "audio_base64": None,
        }


def query_backend_voice(audio_bytes, language: str) -> dict:
    try:
        files = {"audio": ("voice.wav", audio_bytes, "audio/wav")}
        data = {"language": language}
        r = requests.post(
            f"{API_BASE_URL}/voice-query", files=files, data=data, timeout=60
        )
        if r.status_code != 200:
            detail = r.json().get("detail", r.text)
            return {
                "transcribed_text": "...",
                "scheme_title": "Voice Error",
                "benefit_summary": f"⚠️ {detail}",
                "eligibility_points": [],
                "contact_action": "",
                "sources": [],
                "audio_base64": None,
            }
        return r.json()
    except Exception as e:
        return {
            "transcribed_text": "...",
            "scheme_title": "Connection Error",
            "benefit_summary": f"⚠️ {e}",
            "eligibility_points": [],
            "contact_action": "",
            "sources": [],
            "audio_base64": None,
        }


pdf_info = get_indexed_pdfs()

if not pdf_info.get("offline") and pdf_info.get("total_files", 0) == 0:
    if "initial_sync_done" not in st.session_state:
        st.session_state.initial_sync_done = True
        trigger_sync_data(rebuild=False)
        st.cache_data.clear()
        pdf_info = get_indexed_pdfs()


# =========================================================
# 1. PERSISTENT SIDEBAR: OFFICER TOGGLE & PDF MANAGEMENT
# =========================================================
with st.sidebar:
    st.subheader("⚙️ " + ("அதிகாரி மேலாண்மை" if is_ta else "Officer Management"))
    is_officer = st.toggle(
        "🔓 " + ("அதிகாரி முறை இயக்க" if is_ta else "Enable Officer Mode"),
        value=False,
    )

    if is_officer:
        st.divider()
        st.markdown(f"**📤 {'புதிய PDF சேர்' if is_ta else 'Upload Scheme PDF'}**")
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
        if st.button("➕ Index PDF", type="primary", use_container_width=True):
            if uploaded_pdf:
                with st.spinner("Indexing PDF..."):
                    ok, msg = upload_scheme_pdf(uploaded_pdf)
                    if ok:
                        st.success(msg)
                        st.cache_data.clear()
                    else:
                        st.error(msg)
            else:
                st.warning("Select a PDF first.")

        st.divider()
        files_list = pdf_info.get("files", [])
        st.markdown(f"**📚 {'ஆவணங்கள்' if is_ta else 'Indexed PDFs'} ({pdf_info.get('total_files', 0)})**")
        if pdf_info.get("offline"):
            st.error("Backend offline")
        elif files_list:
            for item in files_list:
                clean_name = item["filename"].replace(".pdf.pdf", ".pdf")
                st.caption(f"📄 {clean_name} (`{item['chunks']}`)")
        else:
            st.info("No PDFs indexed.")

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button("🔄 Sync", use_container_width=True):
                ok, msg = trigger_sync_data(rebuild=False)
                st.cache_data.clear()
                st.toast(msg)
        with col_s2:
            if st.button("🛠️ Rebuild", use_container_width=True):
                ok, msg = trigger_sync_data(rebuild=True)
                st.cache_data.clear()
                st.toast(msg)

        st.divider()
        if st.button("🗑️ " + ("உரையாடலை அழி" if is_ta else "Clear Chat"), use_container_width=True):
            st.session_state.messages = []
    else:
        st.caption(
            "விவசாயிகளுக்கான அரசு & நபார்டு திட்ட வழிகாட்டி."
            if is_ta
            else "Official Tamil Nadu agricultural schemes & NABARD assistant."
        )


# =========================================================
# 2. COMPACT LANGUAGE SWITCHER BAR
# =========================================================
top_spacer, top_lang = st.columns([3.2, 1.3])
with top_lang:
    l1, l2 = st.columns(2, gap="small")
    with l1:
        if st.button("🇮🇳 தமிழ்", type="primary" if is_ta else "secondary", use_container_width=True):
            st.session_state.lang = "Tamil"
            st.rerun()
    with l2:
        if st.button("🌐 English", type="primary" if not is_ta else "secondary", use_container_width=True):
            st.session_state.lang = "English"
            st.rerun()


# =========================================================
# 3. DAILY THIRUKKURAL TICKER
# =========================================================
kurals_stream = (
    "🌾 குறள் 1033: உழுதுண்டு வாழ்வாரே வாழ்வார்மற் றெல்லாம் தொழுதுண்டு பின்செல் பவர்"
    "<span class='kural-dot'>✦</span>"
    "🌱 குறள் 1031: சுழன்றும்ஏர்ப் பின்னது உலகம் அதனால் உழந்தும் உழவே தலை"
    "<span class='kural-dot'>✦</span>"
    "🌿 குறள் 1032: உழுவார் உலகத்தார்க்கு ஆணிஅஃ தாற்றாது எழுவாரை எல்லாம் பொறுத்து"
)

st.markdown(
    f"""
    <div class="kural-marquee">
        <div class="kural-track">{kurals_stream}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 4. COMPACT HERO BANNER (Language-Aware)
# =========================================================
banner_file = "data/2.banner_ta.png" if is_ta else "data/1.banner_en.png"
try:
    st.image(banner_file, use_container_width=True)
except Exception:
    st.markdown(
        f"""
        <div style="background:#0D3B20; color:white; padding:12px 18px; border-radius:10px; text-align:center;">
            <h3 style="margin:0; font-size:1.2rem;">🌾 {"உழுதுண்டு வாழ்வாரே" if is_ta else "Uzhudhuntu Vaazhvaare"}</h3>
            <p style="margin:2px 0 0 0; font-size:0.78rem;">{"தமிழ்நாடு விவசாய மானியங்கள் & நபார்டு கடன் வழிகாட்டி" if is_ta else "Tamil Nadu Agricultural Subsidies & NABARD Loan Guide"}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# 5. 3-CARD SORTING CATEGORIES (Aligned & Padded)
# =========================================================
cards_data = [
    {
        "title": "💧 பாசனம் & சோலார்" if is_ta else "💧 Irrigation & Solar",
        "desc": (
            "5 HP சோலார் பம்ப், சொட்டு நீர் & தெளிப்பு நீர் பாசனம்"
            if is_ta
            else "5 HP Solar pumps, drip & sprinkler irrigation"
        ),
        "btn": "விவரம் →" if is_ta else "Explore →",
        "query": (
            "5 HP சோலார் பம்ப் மற்றும் சொட்டு நீர் பாசனத்திற்கு நபார்டு கடன் அளவு மற்றும் மானியம் எவ்வளவு?"
            if is_ta
            else "What are the NABARD unit costs and subsidies for 5 HP solar pumps and drip irrigation?"
        ),
    },
    {
        "title": "🐄 கால்நடை & பண்ணை" if is_ta else "🐄 Dairy & Livestock",
        "desc": (
            "கறவை மாடு, ஆடு வளர்ப்பு மற்றும் கோழிப் பண்ணை கடன்"
            if is_ta
            else "NABARD unit costs for dairy cows, goat & poultry"
        ),
        "btn": "விவரம் →" if is_ta else "Explore →",
        "query": (
            "கறவை மாடு மற்றும் ஆடு வளர்ப்புக்கு நபார்டு கடன் அளவு, மானியம் மற்றும் தகுதிகள் என்ன?"
            if is_ta
            else "What is the NABARD unit cost, loan amount, and eligibility for dairy farming and goat rearing?"
        ),
    },
    {
        "title": "🚜 இயந்திரம் & காப்பீடு" if is_ta else "🚜 Machinery",
        "desc": (
            "டிராக்டர் மானியம், விதைகள் மற்றும் பயிர் காப்பீடு (PMFBY)"
            if is_ta
            else "Tractor subsidies, seeds, and Crop Insurance rules"
        ),
        "btn": "விவரம் →" if is_ta else "Explore →",
        "query": (
            "வேளாண் இயந்திரங்கள் (டிராக்டர்) மானியம் மற்றும் பயிர் காப்பீடு பெறுவது எப்படி?"
            if is_ta
            else "What subsidies apply for tractors/farm machinery and how to apply for Crop Insurance?"
        ),
    },
]

cols_3 = st.columns(3, gap="small")
chosen_card_query = None

for idx, c in enumerate(cards_data):
    with cols_3[idx]:
        st.markdown(
            f"""
            <div class="sort-card">
                <div class="sort-card-title">{c['title']}</div>
                <div class="sort-card-desc">{c['desc']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button(c["btn"], key=f"sort3_{idx}", type="secondary", use_container_width=True):
            chosen_card_query = c["query"]


# =========================================================
# 6. COMPACT CHAT WINDOW & WHATSAPP SHARE
# =========================================================
def render_message_pair(entry: dict):
    res = entry["response"]

    elig_html = ""
    if res.get("eligibility_points"):
        items_li = "".join([f"<li>{pt}</li>" for pt in res["eligibility_points"]])
        elig_html = f"""
        <div style="margin-top:4px;">
            <strong>📋 {"முக்கிய நிபந்தனைகள்:" if is_ta else "Key Conditions:"}</strong>
            <ul style="margin:2px 0 0 16px; color:#1F2937;">{items_li}</ul>
        </div>
        """

    contact_html = ""
    if res.get("contact_action"):
        contact_html = f"""
        <div class="contact-strip">
            <strong>📍 {"தொடர்பு கொள்ள வேண்டிய அதிகாரி:" if is_ta else "Who to Contact / Apply:"}</strong><br>
            {res['contact_action']}
        </div>
        """

    share_text = (
        f"*{res.get('scheme_title', '')}*\n\n"
        f"💰 {res.get('benefit_summary', '')}\n\n"
        f"📍 {res.get('contact_action', '')}"
    )
    wa_link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(share_text)}"

    with st.chat_message("user"):
        st.markdown(f"**{entry['question']}**")

    with st.chat_message("assistant"):
        st.markdown(
            f"""
            <div class="answer-card">
                <div class="answer-title">🌱 {res.get('scheme_title', 'Scheme Info')}</div>
                <div class="benefit-strip">
                    <strong>💰 {"நிதி உதவி & மானியம்:" if is_ta else "Benefit & Subsidy:"}</strong><br>
                    {res.get('benefit_summary', '')}
                </div>
                {elig_html}
                {contact_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<a href="{wa_link}" target="_blank" class="wa-share">📲 {"வாட்ஸ்அப்பில் பகிர்" if is_ta else "Share on WhatsApp"}</a>',
            unsafe_allow_html=True,
        )

        if entry.get("audio_bytes"):
            st.audio(entry["audio_bytes"], format="audio/mp3")

        if res.get("sources"):
            with st.expander("📌 " + ("ஆதார ஆவணம்" if is_ta else "Official Source")):
                for src in res["sources"]:
                    st.caption(f"• {src.replace('.pdf.pdf', '.pdf')}")


chat_box = st.container(height=230, border=True)

with chat_box:
    if not st.session_state.messages:
        if is_ta:
            st.markdown(
                """
                <div class="welcome-empty">
                    <h4>👋 வணக்கம்! உங்கள் விவசாயத் திட்ட உதவியாளர் தயார்</h4>
                    <p>மேலே உள்ள கார்டுகளில் ஒன்றைத் தேர்ந்தெடுக்கவும் அல்லது கீழே மைக் (🎤) மூலம் கேட்கவும்.</p>
                    <div>
                        <span class="sample-chip">☀️ “5 HP சோலார் பம்ப் மானியம் எவ்வளவு?”</span>
                        <span class="sample-chip">🐄 “கறவை மாடு கடன் அளவு என்ன?”</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="welcome-empty">
                    <h4>👋 Vanakkam! Your Tamil Nadu Farmer Scheme Assistant is Ready</h4>
                    <p>Tap a card above or use voice/text below to ask in Tamil or English.</p>
                    <div>
                        <span class="sample-chip">☀️ “5 HP Solar Pump subsidy & unit cost?”</span>
                        <span class="sample-chip">🐄 “NABARD loan for dairy cows?”</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        for msg_entry in st.session_state.messages:
            render_message_pair(msg_entry)


# =========================================================
# 7. BOTTOM INPUT DOCK
# =========================================================
dock_mic, dock_text = st.columns([1.2, 2.8], gap="small")
with dock_mic:
    audio_rec = st.audio_input("🎤 Speak", label_visibility="collapsed")
with dock_text:
    user_typed = st.chat_input(
        "உங்கள் கேள்வியை இங்கே கேளுங்கள்..." if is_ta else "Ask about subsidies, NABARD loans, or schemes..."
    )


def append_and_render(question_str: str, resp_dict: dict):
    audio_data = None
    if resp_dict.get("audio_base64"):
        audio_data = base64.b64decode(resp_dict["audio_base64"])

    record = {
        "question": question_str,
        "response": resp_dict,
        "audio_bytes": audio_data,
    }
    st.session_state.messages.append(record)

    with chat_box:
        render_message_pair(record)


if audio_rec is not None:
    rec_id = hash(audio_rec.getvalue())
    if rec_id != st.session_state.last_audio_id:
        st.session_state.last_audio_id = rec_id
        with chat_box:
            with st.spinner("🎙️ தேடுகிறது..." if is_ta else "🎙️ Searching..."):
                voice_out = query_backend_voice(audio_rec.getvalue(), st.session_state.lang)
                transcribed = voice_out.get("transcribed_text", "🎤 Voice Query")
        append_and_render(f"🎤 {transcribed}", voice_out)

final_prompt = chosen_card_query or user_typed
if final_prompt:
    with chat_box:
        with st.spinner("🌱 தேடுகிறது..." if is_ta else "🌱 Searching scheme documents..."):
            text_out = query_backend_text(final_prompt, st.session_state.lang)
    append_and_render(final_prompt, text_out)
