import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Eniise — Õppimise assistent",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Jost:wght@300;400;500&display=swap');

/* Põhifoon — heleroheline */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMain"] {
    background-color: #EBF3EC !important;
    font-family: 'Jost', sans-serif !important;
    color: #1C1710 !important;
}

/* Külgriba — helerohekas valge */
[data-testid="stSidebar"] {
    background-color: #FAFDF9 !important;
    border-right: 0.5px solid #C8DEC9 !important;
}
[data-testid="stSidebar"] * {
    color: #3A5A3C !important;
    font-family: 'Jost', sans-serif !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2 {
    font-family: 'Cormorant Garamond', serif !important;
    color: #2A4A33 !important;
}

/* Sõnumid */
[data-testid="stChatMessage"] {
    background: #fff !important;
    border: 0.5px solid #C8DEC9 !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.5rem !important;
    font-size: 0.95rem !important;
}

/* Kasutaja sõnum */
[data-testid="stChatMessage"][data-testid*="human"] {
    background: #2A4A33 !important;
    border-color: #2A4A33 !important;
}
[data-testid="stChatMessage"][data-testid*="human"] p {
    color: #fff !important;
}

/* Sisestusväli */
[data-testid="stChatInput"] {
    background: #fff !important;
    border: 0.5px solid #C8DEC9 !important;
    border-radius: 10px !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.9rem !important;
    color: #1C1710 !important;
    background: #fff !important;
}

/* Nupud külgribas */
.stButton > button {
    background: transparent !important;
    color: #3A5A3C !important;
    border: 0.5px solid #C8DEC9 !important;
    border-radius: 7px !important;
    font-family: 'Jost', sans-serif !important;
    font-size: 0.82rem !important;
    padding: 0.4rem 0.7rem !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.15s !important;
}
.stButton > button:hover {
    background: #D6EBD7 !important;
    color: #1A3020 !important;
    border-color: #B0CEB2 !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #EAF5EB !important;
    border: 0.5px solid #C8DEC9 !important;
    border-radius: 8px !important;
    color: #3A5A3C !important;
}

/* Peida Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }

/* Teksti suurus vestluses */
[data-testid="stMarkdownContainer"] p {
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
}
</style>
""", unsafe_allow_html=True)

# ── SÜSTEEMI PROMPT ────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Sa oled Eniise — sõbralik ja tark õppimise assistent, kes aitab õpilastel avastada ennast juhtivat õppimist.

Sinu peamised ülesanded:
1. Aidata õpilastel mõista oma õpistiili (visuaalne, auditiivne, kinesteetiline, lugemis/kirjutamispõhine)
2. Anda nõu meetodite kohta: Pomodoro, märkmekast, aktiivne kordamine, mõistekaardid
3. Aidata seada SMART õpieesmärke
4. Motiveerida ja julgustada
5. Vastata küsimustele konkreetsete ainete kohta lihtsas ja arusaadavas keeles
6. Selgitada tugevusi ja arenguvaldkondi

Räägi eesti keeles — soojalt, sõbralikult, kuid professionaalselt.
Ole lühike ja selge — praktilised nõuanded on paremad kui pikad teooriad.
Iga vastuse lõpus esita üks konkreetne küsimus, mis aitab vestlust edasi viia.
Kasuta emojisid mõõdukalt."""

TERVITUS = """Tere! Olen **Eniise** — sinu isiklik õppimise assistent. ◆

Saan sulle aidata:
- 🎯 Seada õpieesmärke
- 📚 Leida sinu õpistiil
- ⏱ Planeerida aega ja õppimist
- 💡 Õppida efektiivseid meetodeid
- 💪 Avastada tugevusi ja arenguvaldkondi

Mida sa täna soovid teada või arutada?"""

KIIRTEEMAD = [
    "Milline õppija ma olen?",
    "Kuidas eksamiks valmistuda?",
    "Selgita Pomodoro meetodit",
    "Aita mul seada õpieesmärk",
    "Kuidas infot paremini meelde jätta?",
    "Mul on raske keskenduda — mida teha?",
    "Mis on märkmekast?",
    "Kuidas ületada prokrastineerimist?",
]

# ── KÜLGRIBA ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1.75rem 0 1.25rem;'>
        <div style='font-family:"Cormorant Garamond",serif; font-size:2.5rem;
                    font-weight:600; color:#2A4A33; letter-spacing:-1px; line-height:1;'>
            Eni<span style="color:#B8832A">ise</span>
        </div>
        <div style='font-size:0.65rem; color:#8A9A89; margin-top:0.3rem;
                    letter-spacing:0.12em; text-transform:uppercase;'>
            Õppimise assistent
        </div>
    </div>
    <hr style='border:none; border-top:0.5px solid #C8DEC9; margin:0 0 1rem;'>
    <div style='font-size:0.65rem; color:#8A9A89; text-transform:uppercase;
                letter-spacing:0.1em; margin-bottom:0.5rem; padding:0 0.25rem;'>
        Kiirteemad
    </div>
    """, unsafe_allow_html=True)

    for teema in KIIRTEEMAD:
        if st.button(teema, key=f"kt_{teema}"):
            st.session_state.kiirteema = teema

    st.markdown("""
    <hr style='border:none; border-top:0.5px solid #C8DEC9; margin:1rem 0;'>
    """, unsafe_allow_html=True)

    if st.button("🗑  Tühjenda vestlus", key="tyhjenda"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div style='margin-top:1rem; padding:0.625rem 0.75rem; background:#EAF5EB;
                border-radius:8px; border:0.5px solid #C8DEC9;'>
        <div style='font-size:0.65rem; color:#8A9A89; text-transform:uppercase;
                    letter-spacing:0.08em; margin-bottom:0.2rem;'>Mudel</div>
        <div style='font-size:0.78rem; color:#3A5A3C;'>llama-3.3-70b-versatile</div>
        <div style='font-size:0.62rem; color:#8A9A89; margin-top:0.15rem;'>⚡ Powered by Groq</div>
    </div>
    <div style='margin-top:0.75rem; text-align:center; font-size:0.62rem; color:#C8DEC9;'>
        © 2026 Eniise
    </div>
    """, unsafe_allow_html=True)

# ── PÄIS ──────────────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding: 1.25rem 0 0.75rem;'>
    <h1 style='font-family:"Cormorant Garamond",serif; font-size:1.75rem;
               font-weight:600; color:#2A4A33; margin:0; letter-spacing:-0.5px;'>
        Õppimise assistent
    </h1>
    <p style='color:#5A7A5C; font-size:0.82rem; margin-top:0.2rem;'>
        Küsi küsimus või vali teema vasakult
    </p>
</div>
""", unsafe_allow_html=True)

# ── SEISUND ───────────────────────────────────────────────────────────────────

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": TERVITUS}
    ]
if "kiirteema" not in st.session_state:
    st.session_state.kiirteema = None

# ── SÕNUMID ───────────────────────────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── AI FUNKTSIOON ─────────────────────────────────────────────────────────────

def küsi_ai(kasutaja_sonum: str):
    st.session_state.messages.append({"role": "user", "content": kasutaja_sonum})

    with st.chat_message("user"):
        st.markdown(kasutaja_sonum)

    with st.chat_message("assistant"):
        vastus_koht = st.empty()
        try:
            client = Groq()
            ajalugu = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            stream = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": SYSTEM_PROMPT}] + ajalugu,
                max_tokens=1000,
                temperature=0.7,
                stream=True,
            )
            tekst = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                tekst += delta
                vastus_koht.markdown(tekst + "▌")
            vastus_koht.markdown(tekst)
            st.session_state.messages.append({"role": "assistant", "content": tekst})
        except Exception as e:
            vastus_koht.error(
                f"⚠️ Viga: {str(e)}\n\n"
                "Kontrollige, et **GROQ_API_KEY** on seadistatud.\n\n"
                "API võti: [console.groq.com](https://console.groq.com)"
            )
    st.rerun()

# ── KÄIVITAMINE ───────────────────────────────────────────────────────────────

if st.session_state.kiirteema:
    teema = st.session_state.kiirteema
    st.session_state.kiirteema = None
    küsi_ai(teema)

if syote := st.chat_input("Kirjuta siia... ✍️"):
    küsi_ai(syote)
