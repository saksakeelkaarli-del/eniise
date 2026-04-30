import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Eniise — Kaasav haridus",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600&family=Jost:wght@300;400;500&display=swap');

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stMain"] {
    background-color: #EBF3EC !important;
    font-family: 'Jost', sans-serif !important;
    color: #1C1710 !important;
}
[data-testid="stSidebar"] {
    background-color: #FAFDF9 !important;
    border-right: 0.5px solid #C8DEC9 !important;
}
[data-testid="stSidebar"] * {
    color: #3A5A3C !important;
    font-family: 'Jost', sans-serif !important;
}
[data-testid="stChatMessage"] {
    background: #fff !important;
    border: 0.5px solid #C8DEC9 !important;
    border-radius: 12px !important;
    padding: 1rem 1.25rem !important;
    margin-bottom: 0.5rem !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatInput"] textarea {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.9rem !important;
    color: #1C1710 !important;
    background: #fff !important;
}
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
.stTextArea textarea {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.92rem !important;
    border: 0.5px solid #C8DEC9 !important;
    border-radius: 10px !important;
    background: #fff !important;
    color: #1C1710 !important;
    line-height: 1.7 !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 0.5px solid #C8DEC9 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.88rem !important;
    color: #5A7A5C !important;
    padding: 0.625rem 1.25rem !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #2A4A33 !important;
    border-bottom: 2px solid #2A4A33 !important;
    font-weight: 500 !important;
}
[data-testid="stMarkdownContainer"] p {
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── SÜSTEEMI PROMPTID ──────────────────────────────────────────────────────────

CHAT_PROMPT = """Sa oled Eniise — kaasava hariduse assistent, kes toetab õpetajaid, lapsevanemaid ja tugispetsialiste Eestis.

Sinu teadmised põhinevad Haridus- ja Noorteameti (Harno) kaasava hariduse põhimõtetel ja Eesti haridussüsteemil.

Sinu peamised ülesanded:
1. Selgitada kaasava hariduse põhimõtteid — iga laps õpib tavakoolis vastavalt oma vajadustele
2. Nõustada HEV (hariduslike erivajadustega) õpilaste teemal — õpiraskused, käitumisraskused, andekus, erivajadused
3. Selgitada tugiteenuseid — tugiõpetaja, abiõpetaja, logopeedi, psühholoogi roll
4. Aidata koostada individuaalset õppekava (IÕK) ja teha kohandusi
5. Selgitada Rajaleidja nõustamiskeskuse teenuseid
6. Nõustada lapsevanemaid — kuidas toetada last kodus ja koolis
7. Selgitada seadusandlust — PGS §46, kaasava hariduse korraldus
8. Abistada erivajadustega laste märkamisel ja toetamisel

Räägi eesti keeles — soojalt, empaatiliselt ja professionaalselt.
Ole praktiline — anna konkreetseid nõuandeid.
Iga vastuse lõpus esita üks küsimus, mis aitab vestlust edasi viia.
Vajadusel viita: harno.ee/kaasav-haridus ja rajaleidja.ee"""

LIHTNE_KEEL_PROMPT = """Sa oled lihtsa keele ekspert. Sinu ülesanne on muuta keeruline tekst lihtsaks ja arusaadavaks.

Lihtsa keele põhimõtted:
- Kasuta lühikesi lauseid (maksimaalselt 15-20 sõna)
- Kasuta lihtsaid ja tavalisi sõnu — väldi keerulist terminoloogiat
- Kui peab kasutama eriterminit, selgita see kohe ära
- Kasuta aktiivset kõneviisi (mitte "otsus tehti" vaid "me tegime otsuse")
- Üks mõte ühe lause kohta
- Kasuta loendeid ja punktide loetelu
- Ära kasuta lühendeid ilma selgituseta
- Kirjuta konkreetselt — ära kasuta umbmääraseid väljendeid

Lihtne keel on eriti oluline:
- Intellektipuudega inimestele
- Õpiraskustega lastele
- Keeleõppijatele
- Eakatele
- Kõigile, kellele lihtsam tekst on abiks

Säilita originaalteksti tähendus ja kõik olulised faktid.
Väljund peab olema eesti keeles.
Formaat: kõigepealt lihtne tekst, siis lühike selgitus mis muudeti."""

# ── KÜLGRIBA ──────────────────────────────────────────────────────────────────

KIIRTEEMAD = [
    "Mis on kaasav haridus?",
    "Kuidas koostada individuaalset õppekava?",
    "Mida teeb tugiõpetaja?",
    "Kuidas märgata õpiraskusi?",
    "Millised tugiteenused on koolides?",
    "Kuidas rääkida lapsevanemaga HEV-st?",
    "Mis on Rajaleidja?",
    "Kuidas toetada andekat last?",
]

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1.75rem 0 1.25rem;'>
        <div style='font-family:"Cormorant Garamond",serif; font-size:2.5rem;
                    font-weight:600; color:#2A4A33; letter-spacing:-1px; line-height:1;'>
            Eni<span style="color:#B8832A">ise</span>
        </div>
        <div style='font-size:0.65rem; color:#8A9A89; margin-top:0.3rem;
                    letter-spacing:0.12em; text-transform:uppercase;'>
            Kaasava hariduse platvorm
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

    st.markdown("<hr style='border:none; border-top:0.5px solid #C8DEC9; margin:1rem 0;'>",
                unsafe_allow_html=True)

    if st.button("🗑  Tühjenda vestlus", key="tyhjenda"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
    <div style='margin-top:0.75rem; padding:0.625rem 0.75rem; background:#EAF5EB;
                border-radius:8px; border:0.5px solid #C8DEC9; margin-bottom:0.5rem;'>
        <div style='font-size:0.65rem; color:#8A9A89; margin-bottom:0.2rem;
                    text-transform:uppercase; letter-spacing:0.08em;'>Allikas</div>
        <a href="https://harno.ee/kaasav-haridus" target="_blank"
           style='font-size:0.75rem; color:#2A4A33; text-decoration:none;'>
            harno.ee/kaasav-haridus ↗
        </a>
    </div>
    <div style='padding:0.625rem 0.75rem; background:#EAF5EB;
                border-radius:8px; border:0.5px solid #C8DEC9; margin-bottom:0.5rem;'>
        <div style='font-size:0.65rem; color:#8A9A89; margin-bottom:0.2rem;
                    text-transform:uppercase; letter-spacing:0.08em;'>Nõustamine</div>
        <a href="https://rajaleidja.ee" target="_blank"
           style='font-size:0.75rem; color:#2A4A33; text-decoration:none;'>
            rajaleidja.ee ↗
        </a>
    </div>
    <div style='padding:0.625rem 0.75rem; background:#EAF5EB;
                border-radius:8px; border:0.5px solid #C8DEC9;'>
        <div style='font-size:0.65rem; color:#8A9A89; text-transform:uppercase;
                    letter-spacing:0.08em; margin-bottom:0.15rem;'>Mudel</div>
        <div style='font-size:0.75rem; color:#3A5A3C;'>llama-3.3-70b-versatile</div>
        <div style='font-size:0.62rem; color:#8A9A89; margin-top:0.1rem;'>⚡ Powered by Groq</div>
    </div>
    <div style='margin-top:0.75rem; text-align:center; font-size:0.62rem; color:#C8DEC9;'>
        © 2026 Eniise
    </div>
    """, unsafe_allow_html=True)

# ── PEAMINE SISU ──────────────────────────────────────────────────────────────

st.markdown("""
<div style='padding:1.25rem 0 0.75rem;'>
    <h1 style='font-family:"Cormorant Garamond",serif; font-size:1.75rem;
               font-weight:600; color:#2A4A33; margin:0; letter-spacing:-0.5px;'>
        Kaasava hariduse platvorm
    </h1>
    <p style='color:#5A7A5C; font-size:0.82rem; margin-top:0.2rem;'>
        Allikas: <a href="https://harno.ee/kaasav-haridus" target="_blank"
        style="color:#2A4A33;">harno.ee</a> · Nõustamine: <a href="https://rajaleidja.ee"
        target="_blank" style="color:#2A4A33;">rajaleidja.ee</a>
    </p>
</div>
""", unsafe_allow_html=True)

# Vahekaardid
tab1, tab2 = st.tabs(["💬 Assistent", "📝 Lihtne keel"])

# ── VAHEKAART 1: ASSISTENT ─────────────────────────────────────────────────────

with tab1:
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": """Tere! Olen **Eniise** — kaasava hariduse assistent. ◆

Saan sind aidata:
- 🏫 Mõista kaasava hariduse põhimõtteid
- 👶 Toetada HEV õpilasi koolis ja kodus
- 📋 Koostada individuaalset õppekava (IÕK)
- 🤝 Leida sobivaid tugiteenuseid
- 💬 Nõustada lapsevanemaid ja õpetajaid

Kellena sa täna küsimust esitad — õpetaja, lapsevanem või tugispetsialist?"""}]

    if "kiirteema" not in st.session_state:
        st.session_state.kiirteema = None

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    def küsi_ai(kasutaja_sonum: str):
        st.session_state.messages.append({"role": "user", "content": kasutaja_sonum})
        with st.chat_message("user"):
            st.markdown(kasutaja_sonum)
        with st.chat_message("assistant"):
            vastus_koht = st.empty()
            try:
                client = Groq()
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": CHAT_PROMPT}] + st.session_state.messages,
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
                vastus_koht.error(f"⚠️ Viga: {str(e)}\n\nKontrollige GROQ_API_KEY seadistust.")
        st.rerun()

    if st.session_state.kiirteema:
        teema = st.session_state.kiirteema
        st.session_state.kiirteema = None
        küsi_ai(teema)

    if syote := st.chat_input("Kirjuta oma küsimus siia... ✍️"):
        küsi_ai(syote)

# ── VAHEKAART 2: LIHTNE KEEL ──────────────────────────────────────────────────

with tab2:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem;'>
        <h2 style='font-family:"Cormorant Garamond",serif; font-size:1.4rem;
                   font-weight:600; color:#2A4A33; margin:0;'>
            Lihtsa keele tööriist
        </h2>
        <p style='color:#5A7A5C; font-size:0.82rem; margin-top:0.25rem;'>
            Muudab keerulise teksti lihtsaks ja kõigile arusaadavaks — õpiraskustega lastele,
            intellektipuudega inimestele ja keeleõppijatele.
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div style='font-size:0.75rem; font-weight:500; color:#2A4A33;
                    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>
            Algne tekst
        </div>
        """, unsafe_allow_html=True)

        algne_tekst = st.text_area(
            label="Algne tekst",
            label_visibility="collapsed",
            placeholder="Kleebi siia tekst, mida soovid lihtsustada...\n\nNäiteks koolikirja, reeglite teksti, õppeülesande või muu keerulise teksti.",
            height=320,
            key="algne"
        )

        # Näidistekstid
        st.markdown("""
        <div style='font-size:0.72rem; color:#8A9A89; margin-top:0.5rem; margin-bottom:0.35rem;'>
            Proovi näidistekstiga:
        </div>
        """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns(2)
        with col_n1:
            if st.button("📄 Koolikiri", key="naide1", use_container_width=True):
                st.session_state.naide_tekst = """Lugupeetud lapsevanem, teavitame Teid, et vastavalt põhikooli- ja gümnaasiumiseaduse §-le 35 lõikele 2 on kooli juhtkond otsustanud rakendada Teie lapse suhtes käitumisnõuete rikkumise tõttu ajutist õppest kõrvaldamist perioodiks kolm õppepäeva, millest esimene on käesoleva õppeaasta veebruarikuu kaheteistkümnes kuupäev."""
                st.rerun()
        with col_n2:
            if st.button("📋 IÕK selgitus", key="naide2", use_container_width=True):
                st.session_state.naide_tekst = """Individuaalne õppekava (IÕK) on hariduslike erivajadustega õpilasele koostatud õppekava, mis lähtub riiklikust õppekavast ning on kohandatud vastavalt õpilase võimetele, vajadustele ja huvidele, arvestades tema terviseseisundit, erivajadusi ning pedagoogilis-psühholoogilise uurimise tulemusi."""
                st.rerun()

        if "naide_tekst" in st.session_state and st.session_state.naide_tekst:
            algne_tekst = st.session_state.naide_tekst

        st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

        tase = st.select_slider(
            "Lihtsustamise tase",
            options=["Veidi lihtsam", "Lihtsam", "Lihtne keel", "Väga lihtne keel"],
            value="Lihtne keel"
        )

        teisenda_btn = st.button(
            "Teisenda lihtsasse keelde →",
            key="teisenda",
            use_container_width=True,
            type="primary"
        )

    with col2:
        st.markdown("""
        <div style='font-size:0.75rem; font-weight:500; color:#2A4A33;
                    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.5rem;'>
            Lihtne keel
        </div>
        """, unsafe_allow_html=True)

        tulemus_koht = st.empty()

        if "lihtne_tulemus" not in st.session_state:
            st.session_state.lihtne_tulemus = ""

        if st.session_state.lihtne_tulemus:
            tulemus_koht.markdown(
                f"""<div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px;
                padding:1.1rem 1.25rem; min-height:320px; font-size:0.92rem; line-height:1.75;
                color:#1C1710; white-space:pre-wrap;'>{st.session_state.lihtne_tulemus}</div>""",
                unsafe_allow_html=True
            )
        else:
            tulemus_koht.markdown(
                """<div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px;
                padding:1.1rem 1.25rem; min-height:320px; font-size:0.88rem; line-height:1.75;
                color:#8A9A89; font-style:italic;'>
                Lihtsustatud tekst ilmub siia...<br><br>
                Kleebi tekst vasakule ja vajuta "Teisenda lihtsasse keelde →"
                </div>""",
                unsafe_allow_html=True
            )

        if st.session_state.lihtne_tulemus:
            st.download_button(
                label="⬇ Lae alla (.txt)",
                data=st.session_state.lihtne_tulemus,
                file_name="lihtne_keel.txt",
                mime="text/plain",
                use_container_width=True
            )

    # Teisendamine
    if teisenda_btn:
        if not algne_tekst or len(algne_tekst.strip()) < 10:
            st.warning("Palun kleebi tekst vasakule väljale.")
        else:
            tase_juhend = {
                "Veidi lihtsam": "Muuda tekst veidi lihtsamaks — eemalda kõige keerulisemad väljendid.",
                "Lihtsam": "Muuda tekst selgelt lihtsamaks — kasuta igapäevast keelt.",
                "Lihtne keel": "Kasuta lihtsa keele põhimõtteid täielikult — lühikesed laused, lihtsad sõnad.",
                "Väga lihtne keel": "Kasuta väga lihtsat keelt — nagu räägid 8-aastasele lapsele. Maksimaalselt 10 sõna lauses."
            }

            prompt = f"""{tase_juhend[tase]}

Originaaltekst:
{algne_tekst}

Kirjuta kõigepealt lihtsustatud tekst, seejärel lisa lühike selgitus (2-3 lauset) mis muudeti ja miks."""

            with st.spinner("Lihtsustан teksti..."):
                try:
                    client = Groq()
                    vastus = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": LIHTNE_KEEL_PROMPT},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=1500,
                        temperature=0.4,
                    )
                    tulemus = vastus.choices[0].message.content
                    st.session_state.lihtne_tulemus = tulemus
                    st.rerun()
                except Exception as e:
                    st.error(f"⚠️ Viga: {str(e)}\n\nKontrollige GROQ_API_KEY seadistust.")

    # Info kastid
    st.markdown("""
    <div style='margin-top:1.5rem; display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.75rem;'>
        <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px; padding:0.875rem;'>
            <div style='font-size:0.75rem; font-weight:500; color:#2A4A33; margin-bottom:0.35rem;'>👶 Kellele?</div>
            <div style='font-size:0.75rem; color:#5A7A5C; line-height:1.6;'>
                Intellektipuudega inimestele · Õpiraskustega lastele · Keeleõppijatele · Eakatele
            </div>
        </div>
        <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px; padding:0.875rem;'>
            <div style='font-size:0.75rem; font-weight:500; color:#2A4A33; margin-bottom:0.35rem;'>📋 Milleks?</div>
            <div style='font-size:0.75rem; color:#5A7A5C; line-height:1.6;'>
                Koolikirjad · IÕK tekstid · Reeglid · Ülesanded · Teavitused
            </div>
        </div>
        <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px; padding:0.875rem;'>
            <div style='font-size:0.75rem; font-weight:500; color:#2A4A33; margin-bottom:0.35rem;'>✅ Põhimõtted</div>
            <div style='font-size:0.75rem; color:#5A7A5C; line-height:1.6;'>
                Lühikesed laused · Lihtsad sõnad · Üks mõte lauses · Aktiivne kõneviis
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
