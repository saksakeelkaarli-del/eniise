import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Eniise — Kaasava õppimise assistent",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;1,400&family=Jost:wght@300;400;500&display=swap');

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
}
[data-testid="stChatInput"] textarea {
    font-family: 'Jost', sans-serif !important;
    color: #1C1710 !important;
    background: #fff !important;
}
.stButton > button {
    font-family: 'Jost', sans-serif !important;
    transition: all 0.15s !important;
}
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 0.5px solid #C8DEC9 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Jost', sans-serif !important;
    font-size: 0.88rem !important;
    color: #5A7A5C !important;
}
.stTabs [aria-selected="true"] {
    color: #2A4A33 !important;
    border-bottom: 2px solid #2A4A33 !important;
    font-weight: 500 !important;
}
.stTextArea textarea {
    font-family: 'Jost', sans-serif !important;
    border: 0.5px solid #C8DEC9 !important;
    border-radius: 10px !important;
    background: #fff !important;
}
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── ANDMED ────────────────────────────────────────────────────────────────────

TEEMAD = [
    {
        "id": "kaasav",
        "ikoon": "🏫",
        "pealkiri": "Kaasav haridus",
        "lühikirjeldus": "Iga laps õpib tavakoolis vastavalt oma vajadustele",
        "värv": "#2A4A33",
        "taust": "#EAF5EB",
        "mis_on": """Kaasav haridus tähendab, et **kõik lapsed** — sõltumata nende võimetest, erivajadusest või taustast — õpivad koos tavaklassis.

Kaasava hariduse põhimõte on lihtne: **kool kohandub lapse järgi, mitte laps kooli järgi.** ❤️

See ei tähenda, et kõik peavad tegema täpselt sama — see tähendab, et igaühele luuakse tingimused, kus ta saab õppida ja areneda.""",
        "soovitused": [
            "🤝 Loo klassis turvaline ja lugupidav õhkkond — kõik on teretulnud",
            "📋 Kohanda ülesandeid vastavalt õpilase vajadustele",
            "👥 Kasuta paaristöid ja rühmatöid — kaasamine toimib läbi koostöö",
            "💬 Räägi avameelselt erinevustest — mitmekesisus on rikkus",
            "🎯 Sea igale lapsele tema tasemele sobivad eesmärgid",
        ],
        "toimetulek": """**Kui kaasamine tundub keeruline:**

Algus võib olla raske — see on täiesti normaalne! Siin on mida teha:

1. **Alusta väikesest** — üks kohandus, üks samm korraga
2. **Küsi abi** — tugiõpetaja, tugispetsialist on olemas selleks, et aidata
3. **Räägi lapsevanemaga** — nemad tunnevad last kõige paremini
4. **Pea meeles** — kaasamine on protsess, mitte kohene tulemus 💚""",
    },
    {
        "id": "hev",
        "ikoon": "👶",
        "pealkiri": "HEV õpilane",
        "lühikirjeldus": "Hariduslike erivajadustega laps vajab lisatuge ja mõistmist",
        "värv": "#1A4A7A",
        "taust": "#EAF0FA",
        "mis_on": """HEV tähendab **hariduslikud erivajadused** — see hõlmab väga erinevaid lapsi:

- 📚 Õpiraskustega lapsed (düsleksia, düskalkuulia jt)
- 🧠 Intellektipuudega lapsed
- 👁 Nägemis- või kuulmispuudega lapsed
- 🌟 Andekad lapsed (ka nemad vajavad eriprogrammi!)
- 💬 Kõne- ja keeleprobleemidega lapsed
- 🎭 Käitumis- ja tundeprobleemidega lapsed

**Iga HEV laps on erinev** — üks diagnoos ei tähenda sama lähenemist kõigile! 💙""",
        "soovitused": [
            "🔍 Märka ja dokumenteeri lapse tugevused, mitte ainult raskused",
            "📋 Taotle IÕK (individuaalne õppekava) kui laps vajab kohandusi",
            "🤝 Tee koostööd lapsevanemaga — nad on parimad eksperdid oma lapse kohta",
            "🎯 Sea realistlikud ja saavutatavad eesmärgid",
            "✅ Tähista edusid — isegi väikesed sammud on olulised!",
            "💬 Räägi lapsega ausalt — ta tunneb ennast ise kõige paremini",
        ],
        "toimetulek": """**Kuidas toime tulla HEV lapse õpetamisel:**

See võib tunduda üle jõu käiv — aga sa ei ole üksi! 🤗

1. **Küsi tugiteenuseid** — tugiõpetaja, logopeed, psühholoog on siin selleks
2. **Pea meeles lapse tugevusi** — igal lapsel on midagi, milles ta hiilgab
3. **Ära võrdle** — HEV lapse areng ei pea sarnanema teiste omaga
4. **Hoolitse ka enda eest** — läbipõlemine ei aita kedagi""",
    },
    {
        "id": "iok",
        "ikoon": "📋",
        "pealkiri": "Individuaalne õppekava",
        "lühikirjeldus": "IÕK on lapsele kohandatud isiklik õppeplaan",
        "värv": "#5A3A7A",
        "taust": "#F0EAF8",
        "mis_on": """**Individuaalne õppekava (IÕK)** on kirjalik dokument, mis kirjeldab:

- Millised on lapse **tugevused ja vajadused**
- Millised on lapsele seatud **õpieesmärgid**
- Kuidas **kohandatakse** õppesisu, -mahtu või -meetodeid
- Kes **toetab** last ja kuidas
- Kuidas **hinnatakse** lapse arengut

IÕK ei ole märgistamine — see on **lapse parim sõber koolis!** 💜""",
        "soovitused": [
            "📝 Kaasa IÕK koostamisse laps ise, lapsevanem ja kõik toetajad",
            "🎯 Sea konkreetsed ja mõõdetavad eesmärgid (mitte 'laps areneb', vaid 'laps loeb 50 sõna minutis')",
            "📅 Vaata IÕK üle vähemalt kord trimestris",
            "✅ Dokumenteeri edusammud — see motiveerib kõiki!",
            "💬 Selgita lapsele tema IÕK-d lihtsas keeles",
        ],
        "toimetulek": """**IÕK tundub keeruline? Alusta siit:**

1. **Kogu infot** — vaatlused, testimised, lapsevanema kirjeldused
2. **Kirjuta lihtsalt** — IÕK peab olema arusaadav kõigile
3. **Ära tee üksinda** — kaasa tugipersonal
4. **Kasuta malle** — paljud koolid ja omavalitsused pakuvad valmis vormi
5. **Pea meeles** — IÕK on elav dokument, mida tohib muuta! 📋""",
    },
    {
        "id": "tugi",
        "ikoon": "🤝",
        "pealkiri": "Tugiteenused koolis",
        "lühikirjeldus": "Tugiõpetaja, logopeed, psühholoog — sinu meeskond",
        "värv": "#1D7A5A",
        "taust": "#EAF5F0",
        "mis_on": """Kaasav haridus toimib **meeskonnatööna** — üks õpetaja ei pea kõike üksi tegema! 💚

**Tugiteenused koolis:**
- 👩‍🏫 **Tugiõpetaja** — aitab klassis õpilasi otse tundides
- 👩‍💼 **Abiõpetaja** — toetab konkreetselt üht või mitut last
- 🗣 **Logopeed** — kõne, lugemise ja kirjutamise toetamine
- 🧠 **Koolipsühholoog** — emotsionaalse heaolu toetamine
- 👁 **Sotsiaalpedagoog** — käitumise ja suhtlemise toetamine
- 🌟 **Eripedagoog** — HEV laste spetsialist""",
        "soovitused": [
            "📞 Pöördu tugispetsialisti poole varakult — ära oota, kuni olukord on kriis",
            "🤝 Tee tihedat koostööd — jaga infot regulaarselt",
            "📋 Kogu kõik meeskonnaliikmed IÕK koosolekule",
            "💬 Räägi lapsevanemale, millised tugiteenused on olemas",
            "✍️ Dokumenteeri kõik — see kaitseb kõiki osapooli",
        ],
        "toimetulek": """**Kui tugiteenuseid ei ole piisavalt:**

See on kahjuks sage probleem — aga on lahendusi! 🤗

1. **Räägi juhtkonnaga** — tugiteenuste vajadus peab olema dokumenteeritud
2. **Kasuta omavalitsuse ressursse** — mõned teenused on väljastpoolt kooli
3. **Võrgusta** — õpetajad õpivad üksteiselt palju
4. **Pea meeles** — lapsevanem on samuti tiimi osa!""",
    },
    {
        "id": "opiraskused",
        "ikoon": "📚",
        "pealkiri": "Õpiraskused",
        "lühikirjeldus": "Düsleksia, düsprakssia, tähelepanuraskused ja muud",
        "värv": "#7A3A1A",
        "taust": "#F5EDE0",
        "mis_on": """**Õpiraskused** ei tähenda, et laps on loll — see tähendab, et tema aju töötab **natuke teisiti!** 🧠

**Levinumad õpiraskused:**
- 📖 **Düsleksia** — lugemis- ja kirjutamisraskused
- 🔢 **Düskalkuulia** — arvutamisraskused
- ✍️ **Düsgraafia** — kirjutamisraskused (käekiri, korrektuur)
- 🎯 **ADHD** — tähelepanu ja aktiivsuse probleemid
- 🗣 **Kõnearengu hilinemine** — hiljem arenev kõne

**Tähtis teada:** õpiraskus ei ole iseloomuviga ega laiskus! 💙""",
        "soovitused": [
            "⏰ Anna lapsele rohkem aega ülesannete täitmiseks",
            "📝 Luba kasutada abivahendeid (kalkulaator, sõnaraamat, diktofon)",
            "👁 Kasuta visuaalseid abivahendeid — pildid, skeemid, värvid",
            "✂️ Jaga suuremad ülesanded väikesteks sammudeks",
            "🌟 Tähista iga edusammu — eneseusk on kõige tähtsam!",
            "🔄 Korda ja kinnita — õpiraskusega laps vajab rohkem kordamist",
        ],
        "toimetulek": """**Kuidas aidata õpiraskusega last:**

1. **Ära häbista** — "proovi rohkem" ei aita, kui laps juba pingutab
2. **Leia tugevused** — õpiraskusega lastel on sageli erakordsed oskused muudes valdkondades
3. **Muuda keskkonda** — istumiskoht, valgustus, müra tase — kõik loeb
4. **Räägi lapsega ausalt** — selgita, miks tema aju vajab teistsugust lähenemist
5. **Taotle hindamiskohandusi** — see on lapse õigus! 📚""",
    },
    {
        "id": "andekus",
        "ikoon": "🌟",
        "pealkiri": "Andekas laps",
        "lühikirjeldus": "Andekad lapsed vajavad samuti eriprogrammi ja tähelepanu",
        "värv": "#B8832A",
        "taust": "#FBF0E0",
        "mis_on": """**Andekus** on samuti hariduslik erivajadus — ka andekas laps vajab eriprogrammi! 🌟

Andekas laps võib:
- Olla kaugelt ees eakaaslastest ühes või mitmes valdkonnas
- Igavleda tavapärasel õppetasemel
- Olla sotsiaalselt ebaküps, kuigi intellektuaalselt edasijõudnud
- Tunduda "probleemne", kui teda ei stimuleerita piisavalt

**Andekus ei ole ainult IQ** — andekus võib avalduda kunstis, muusikas, spordis, sotsiaalses intelligentsuses jne. 💛""",
        "soovitused": [
            "📚 Paku lisaväljakutseid — sügavamad teemad, keerukamad ülesanded",
            "🚀 Lase andekal lapsel minna oma tempos edasi",
            "🤝 Ühenda eakaaslastega, kellel on sarnased huvid",
            "🎨 Toeta mitmekülgset arengut — mitte ainult tugevaid valdkondi",
            "💬 Kuula last — ka andekad lapsed vajavad emotsionaalset tuge",
        ],
        "toimetulek": """**Kui andekas laps on rahulolematu:**

1. **Uurige koos** — mis teda huvitab ja millele tähelepanu suunata
2. **Kiirendamine vs rikastamine** — mõnikord on parem lähenemine sügavam, mitte kiirem
3. **Sotsiaalsed oskused** — andekad lapsed vajavad sageli abi sõprussuhetes
4. **Pea meeles** — ka andekas laps võib olla ebakindel ja vajada julgustust! 🌟""",
    },
    {
        "id": "lapsevanem",
        "ikoon": "👨‍👩‍👧",
        "pealkiri": "Lapsevanemale",
        "lühikirjeldus": "Kuidas toetada last kodus ja teha koostööd kooliga",
        "värv": "#3A5A7A",
        "taust": "#EAF2FA",
        "mis_on": """**Lapsevanem on lapse kõige tähtsam toetaja!** 💙

Kooli ja kodu koostöö on eduka kaasava hariduse alus. Lapsevanemana:

- **Sina tunned last kõige paremini** — sinu info on hindamatu
- **Sina oled meeskonna oluline liige** — mitte kõrvalseisja
- **Sinu suhtumine mõjutab last** — positiivne lähenemine kandub üle
- **Sul on õigused** — teada saada, osaleda, kaasa rääkida""",
        "soovitused": [
            "📞 Hoia regulaarselt kontakti õpetajaga — ära oota, kuni tekib probleem",
            "🏠 Loo kodus struktureeritud õpikeskkond",
            "✅ Tähista lapse edusamme — isegi väikeseid!",
            "💬 Räägi lapsega koolist positiivselt",
            "📋 Tutvu IÕK-ga ja osale selle koostamisel",
            "🤗 Otsi tuge ka endale — lapsevanema tee võib olla raske",
        ],
        "toimetulek": """**Kui kool ei mõista sinu last:**

1. **Räägi rahulikult** — emotsionaalne vestlus harva aitab
2. **Too faktid** — kirjelda konkreetseid olukordi
3. **Küsi kirjalikku vastust** — tähtis info paber on usaldusväärne
4. **Otsi liitlasi** — tugirühmad, teised lapsevanemad
5. **Pea meeles** — sa ei ole üksi! 💙""",
    },
    {
        "id": "kaitumine",
        "ikoon": "🎭",
        "pealkiri": "Käitumisraskused",
        "lühikirjeldus": "Iga käitumine räägib vajadusest — õpime kuulama",
        "värv": "#5A2A5A",
        "taust": "#F5EAF5",
        "mis_on": """**Käitumisraskused** on sageli lapse katse öelda: *"Ma vajan abi!"* 💜

Problemaatiline käitumine võib tuleneda:
- 😟 Emotsionaalsetest raskustest (ärevus, depressioon)
- 🏠 Kodusest olukorrast
- 🧠 Neuroarengulisest eripärast (ADHD, autism jt)
- 📚 Õpiraskustest, mis tekitavad frustratsiooni
- 👥 Suhtlemisprobleemidest eakaaslastega

**Karistamine harva lahendab probleemi** — oluline on mõista, mis vajadust käitumine väljendab.""",
        "soovitused": [
            "🔍 Uuri põhjust — mis juhtus enne problemaatilist käitumist?",
            "🗣 Räägi lapsega rahulikult — pärast olukorra rahustumist",
            "📋 Loo selged ja järjepidevad reeglid",
            "✅ Märka ja tähista head käitumist",
            "🤝 Tee koostööd lapsevanema ja tugispetsialistiga",
            "💚 Hoia suhet lapsega — turvaline suhe on muutuse alus",
        ],
        "toimetulek": """**Kui käitumine on väga keeruline:**

1. **Jää rahulikuks** — su emotsioon kandub lapsele edasi
2. **Ära võta isiklikult** — käitumine on suunatud olukorra vastu, mitte sinu vastu
3. **Küsi abi** — koolipsühholoog, sotsiaalpedagoog on selleks olemas
4. **Dokumenteeri** — millal, kus, mis juhtus — see aitab mustrit näha
5. **Hoolitse enda eest** — keeruline käitumine on kurnav! 🎭""",
    },
]

LIHTSA_KEELE_TEKSTID = [
    {
        "kategooria": "🏫 Kool",
        "tekstid": [
            {
                "pealkiri": "Mis on kaasav haridus?",
                "tekst": """Kaasav haridus tähendab, et kõik lapsed käivad ühes koolis.

Ka lapsed, kes vajavad rohkem abi.
Ka lapsed, kes õpivad teisiti.
Ka lapsed, kellel on puue.

Kõik lapsed on võrdsed.
Kõigil lastel on õigus head haridust saada.

Kool aitab igat last.
Kool muudab ennast, et aidata last.

See on kaasav haridus. 💚""",
            },
            {
                "pealkiri": "Mis on IÕK?",
                "tekst": """IÕK on individuaalne õppekava.

IÕK on eriplaan sinu lapsele.
Selles plaanis on kirjas:
• Milles laps on hea
• Millega lapsel on raske
• Kuidas koolis last aidatakse
• Millised on lapse eesmärgid

IÕK teevad koos:
• Õpetaja
• Lapsevanem
• Laps ise
• Tugispetsialist

IÕK on lapse parim sõber koolis. 📋""",
            },
            {
                "pealkiri": "Mis on tugiõpetaja?",
                "tekst": """Tugiõpetaja on õpetaja, kes aitab lapsi.

Tugiõpetaja on klassis koos õpetajaga.
Ta aitab lapsi, kes vajavad rohkem abi.

Tugiõpetaja:
• Selgitab ülesandeid uuesti
• Aitab lapsel keskenduda
• Kohandab ülesandeid
• Toetab ja julgustab

Tugiõpetaja on sõber ja abi. 🤝""",
            },
        ],
    },
    {
        "kategooria": "📚 Õppimine",
        "tekstid": [
            {
                "pealkiri": "Mis on düsleksia?",
                "tekst": """Düsleksia on lugemis- ja kirjutamisraskus.

Düsleksiaga inimese aju töötab teisiti.
See ei ole laiskus.
See ei ole rumalus.

Düsleksiaga inimesed:
• Segavad tähti
• Loevad aeglasemalt
• Teevad rohkem kirjavigu

Aga düsleksiaga inimesel on sageli:
• Hea fantaasia
• Hea suuline kõne
• Loov mõtlemine

Düsleksiaga inimesed saavad abi.
Õppimine läheb paremaks. 📖""",
            },
            {
                "pealkiri": "Mis on ADHD?",
                "tekst": """ADHD on tähelepanu häire.

ADHD-ga inimestel on raske:
• Kaua ühele asjale tähelepanu pöörata
• Paigal olla
• Järjekorras oodata

See ei ole iseloomuviga.
See on ajutöö eripära.

ADHD-ga lapsed on sageli:
• Loomingulised
• Energilised
• Kiired mõtlejad

Abi võib olla:
• Lühemad ülesanded
• Sagedased pausid
• Selge struktuur 🎯""",
            },
            {
                "pealkiri": "Kuidas õppida paremini?",
                "tekst": """Kõik inimesed õpivad erinevalt.

Mõned inimesed õpivad nägemisega.
Nad vajavad pilte ja jooniseid.

Mõned inimesed õpivad kuulmisega.
Nad vajavad selgitusi ja arutelusid.

Mõned inimesed õpivad tegemisega.
Nad vajavad harjutusi ja katseid.

Proovi järele:
• Tee väikseid pause
• Korda õpitut
• Selgita sõbrale
• Joonista skeeme

Leia oma viis! 💡""",
            },
        ],
    },
    {
        "kategooria": "👨‍👩‍👧 Perekond",
        "tekstid": [
            {
                "pealkiri": "Kuidas last kodus aidata?",
                "tekst": """Saad last kodus palju aidata.

Loo kindel kord:
• Õpi iga päev samal ajal
• Tee enne õppimist lühike paus
• Lülita telefon välja

Loo hea koht:
• Vaikne ruum
• Hea valgustus
• Kõik vajalik olemas

Toeta last:
• Küsi kuidas koolis läks
• Tähista edusamme
• Ära sõima vigade pärast

Sa oled parim, kes saab last aidata! 💙""",
            },
            {
                "pealkiri": "Kuidas kooliga suhelda?",
                "tekst": """Lapsevanem ja kool on meeskond.

Suhtlemise nõuanded:

Helista või kirjuta õpetajale.
Räägi murest varakult.
Ära oota, kuni olukord on halb.

Küsi küsimusi:
• Kuidas mu laps koolis läheb?
• Kuidas saan kodus aidata?
• Milliseid teenuseid saame kasutada?

Osale koosolekutel.
Loo ka IÕK koostamisel osaleda.

Sina tunned last kõige paremini. 🤝""",
            },
        ],
    },
]

CHAT_PROMPT = """Sa oled Eniise — armas, soe ja sõbralik kaasava õppimise assistent, kes aitab õpetajaid, lapsevanemaid ja tugispetsialiste.

Sa räägid alati soojalt ja julgustades — nagu hea sõber, kes juhtub olema ekspert. Kasuta emojisid mõõdukalt. Ära ole kunagi külm või ametlik.

Sinu peamised ülesanded:
1. Selgitada kaasava hariduse põhimõtteid — iga laps on eriline ja väärib tuge 💚
2. Nõustada HEV õpilaste teemal — õpiraskused, käitumisraskused, andekus, erivajadused
3. Selgitada tugiteenuseid — tugiõpetaja, abiõpetaja, logopeedi, psühholoogi roll
4. Aidata koostada individuaalset õppekava (IÕK) ja teha kohandusi
5. Nõustada lapsevanemaid — kuidas last kodus ja koolis toetada
6. Toetada ja motiveerida — kaasav haridus on meeskonnatöö!

Stiil:
- Ole VÄGA sõbralik, soe ja empaatiline
- Alusta sageli julgustava sõnaga
- Tunnusta pingutust ja muret lapse heaolu pärast
- Anna praktilisi nõuandeid
- Iga vastuse lõpus esita üks sõbralik küsimus
- Räägi eesti keeles"""

LIHTNE_KEEL_PROMPT = """Sa oled lihtsa keele ekspert. Muuda keeruline tekst lihtsaks ja arusaadavaks.

Lihtsa keele põhimõtted:
- Lühikesed laused (max 15 sõna)
- Lihtsad ja tavalised sõnad
- Üks mõte ühe lause kohta
- Aktiivne kõneviis
- Kasuta loendeid
- Selgita eritermineid kohe

Säilita originaalteksti tähendus.
Väljund peab olema eesti keeles.
Kõigepealt lihtne tekst, siis lühike selgitus mis muudeti."""

# ── SEISUND ───────────────────────────────────────────────────────────────────

if "leht" not in st.session_state:
    st.session_state.leht = "avaleht"
if "aktiivne_teema" not in st.session_state:
    st.session_state.aktiivne_teema = None
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": """Tere tulemast! 🌿 Olen **Eniise** — sinu sõbralik kaasava õppimise assistent!

Olen siin, et sind toetada — pole rumalaid küsimusi, ainult head vestlused! 💚

Kellena sa täna küsimust esitad — õpetaja, lapsevanem või tugispetsialist? 😊"""}]
if "kiirteema" not in st.session_state:
    st.session_state.kiirteema = None
if "lihtne_tulemus" not in st.session_state:
    st.session_state.lihtne_tulemus = ""

# ── KÜLGRIBA ──────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1.5rem 0 1rem;'>
        <div style='font-family:"Cormorant Garamond",serif; font-size:2.25rem;
                    font-weight:600; color:#2A4A33; letter-spacing:-1px; line-height:1;'>
            Eni<span style="color:#B8832A">ise</span>
        </div>
        <div style='font-size:0.62rem; color:#8A9A89; margin-top:0.25rem;
                    letter-spacing:0.12em; text-transform:uppercase;'>
            Kaasava õppimise platvorm
        </div>
    </div>
    <hr style='border:none; border-top:0.5px solid #C8DEC9; margin:0 0 0.875rem;'>
    """, unsafe_allow_html=True)

    # Navigatsioon
    nav_nupud = [
        ("🏠", "Avaleht", "avaleht"),
        ("⭐", "Päeva inspiratsioon", "inspiratsioon"),
        ("💬", "Assistent", "assistent"),
        ("📝", "Lihtne keel", "lihtne"),
        ("📚", "Tekstikogumik", "kogumik"),
    ]

    for ikoon, nimi, leht_id in nav_nupud:
        aktiivne = st.session_state.leht == leht_id
        stiil = "background:#2A4A33 !important; color:#fff !important;" if aktiivne else ""
        if st.button(f"{ikoon}  {nimi}", key=f"nav_{leht_id}", use_container_width=True):
            st.session_state.leht = leht_id
            st.session_state.aktiivne_teema = None
            st.rerun()

    st.markdown("""
    <hr style='border:none; border-top:0.5px solid #C8DEC9; margin:0.875rem 0;'>
    <div style='font-size:0.62rem; color:#8A9A89; text-transform:uppercase;
                letter-spacing:0.1em; margin-bottom:0.5rem; padding:0 0.25rem;'>
        Kiirteemad
    </div>
    """, unsafe_allow_html=True)

    for teema in TEEMAD[:4]:
        if st.button(f"{teema['ikoon']} {teema['pealkiri']}", key=f"sb_{teema['id']}", use_container_width=True):
            st.session_state.leht = "teema_detail"
            st.session_state.aktiivne_teema = teema["id"]
            st.rerun()

    st.markdown("""
    <div style='margin-top:0.75rem; padding:0.625rem 0.75rem; background:#EAF5EB;
                border-radius:8px; border:0.5px solid #C8DEC9;'>
        <div style='font-size:0.72rem; color:#3A5A3C; font-family:"Jost",sans-serif;'>
            llama-3.3-70b-versatile
        </div>
        <div style='font-size:0.62rem; color:#8A9A89; margin-top:0.1rem;'>⚡ Powered by Groq</div>
    </div>
    <div style='margin-top:0.625rem; text-align:center; font-size:0.62rem; color:#C8DEC9;'>
        © 2026 Eniise
    </div>
    """, unsafe_allow_html=True)

# ── LEHEKÜLGEDE RENDERDAMINE ──────────────────────────────────────────────────

leht = st.session_state.leht

# ── AVALEHT ───────────────────────────────────────────────────────────────────

if leht == "avaleht":
    st.markdown("""
    <div style='padding:1.5rem 0 0.5rem;'>
        <h1 style='font-family:"Cormorant Garamond",serif; font-size:2rem;
                   font-weight:600; color:#2A4A33; margin:0; letter-spacing:-0.5px;'>
            Tere tulemast Eniisesse! 🌿
        </h1>
        <p style='color:#5A7A5C; font-size:0.9rem; margin-top:0.35rem; line-height:1.6;'>
            Siin leiad kõik, mida vajad kaasava õppimise toetamiseks.
            Vali teema, mida soovid uurida! 💚
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Päeva inspiratsioon banner
    import datetime as _dt
    _idx = _dt.date.today().toordinal() % 11
    _names = ["Temple Grandin","Stephen Hawking","Agatha Christie",
              "Nick Vujicic","Helen Keller","Michael Phelps","Frida Kahlo",
              "Albert Einstein","Simone Biles","Richard Branson","Aimee Mullins"]
    _icons = ["🐄","🌌","📖","💪","✋","🏊","🎨","⚛️","🤸","🚀","🏃"]
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#2A4A3320,#EAF5EB);
                border:0.5px solid #C8DEC9; border-left:4px solid #B8832A;
                border-radius:12px; padding:1rem 1.25rem; margin-bottom:1.25rem;
                display:flex; align-items:center; justify-content:space-between;'>
        <div>
            <div style='font-size:0.65rem; color:#8A9A89; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:0.2rem;'>Täna inspireerib</div>
            <div style='font-size:1rem; font-weight:500; color:#2A4A33;
                        font-family:"Cormorant Garamond",serif;'>
                {_icons[_idx]} {_names[_idx]}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("⭐ Loe päeva inspiratsioonilugu", key="home_insp"):
        st.session_state.leht = "inspiratsioon"
        st.rerun()

    # Teemade ruudustik
    st.markdown("""
    <div style='font-size:0.72rem; font-weight:500; color:#8A9A89; text-transform:uppercase;
                letter-spacing:0.1em; margin:1rem 0 0.75rem;'>
        Vali teema
    </div>
    """, unsafe_allow_html=True)

    # 4 veergu
    cols = st.columns(4)
    for i, teema in enumerate(TEEMAD):
        with cols[i % 4]:
            st.markdown(f"""
            <div style='background:{teema["taust"]}; border:1px solid {teema["värv"]}30;
                        border-radius:12px; padding:1.1rem; margin-bottom:0.75rem;
                        border-top:3px solid {teema["värv"]};'>
                <div style='font-size:1.5rem; margin-bottom:0.375rem;'>{teema["ikoon"]}</div>
                <div style='font-size:0.88rem; font-weight:500; color:{teema["värv"]};
                            font-family:"Cormorant Garamond",serif; margin-bottom:0.25rem;'>
                    {teema["pealkiri"]}
                </div>
                <div style='font-size:0.72rem; color:#5A7A5C; line-height:1.5;'>
                    {teema["lühikirjeldus"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Vaata lähemalt →", key=f"home_{teema['id']}", use_container_width=True):
                st.session_state.leht = "teema_detail"
                st.session_state.aktiivne_teema = teema["id"]
                st.rerun()

    # Kiirlingid
    st.markdown("""
    <div style='margin-top:1.25rem; display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.75rem;'>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px;
                    padding:1rem; text-align:center;'>
            <div style='font-size:1.5rem;'>💬</div>
            <div style='font-size:0.85rem; font-weight:500; color:#2A4A33; margin-top:0.25rem;'>AI Assistent</div>
            <div style='font-size:0.72rem; color:#5A7A5C; margin-top:0.15rem;'>Küsi küsimus, saa vastus</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ava assistent →", key="home_chat", use_container_width=True):
            st.session_state.leht = "assistent"
            st.rerun()
    with col2:
        st.markdown("""
        <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px;
                    padding:1rem; text-align:center;'>
            <div style='font-size:1.5rem;'>📝</div>
            <div style='font-size:0.85rem; font-weight:500; color:#2A4A33; margin-top:0.25rem;'>Lihtne keel</div>
            <div style='font-size:0.72rem; color:#5A7A5C; margin-top:0.15rem;'>Muuda tekst lihtsamaks</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ava tööriist →", key="home_lihtne", use_container_width=True):
            st.session_state.leht = "lihtne"
            st.rerun()
    with col3:
        st.markdown("""
        <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:10px;
                    padding:1rem; text-align:center;'>
            <div style='font-size:1.5rem;'>📚</div>
            <div style='font-size:0.85rem; font-weight:500; color:#2A4A33; margin-top:0.25rem;'>Tekstikogumik</div>
            <div style='font-size:0.72rem; color:#5A7A5C; margin-top:0.15rem;'>Valmis tekstid lihtsas keeles</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Ava kogumik →", key="home_kogumik", use_container_width=True):
            st.session_state.leht = "kogumik"
            st.rerun()

# ── TEEMA DETAILLEHT ──────────────────────────────────────────────────────────

elif leht == "teema_detail":
    teema_id = st.session_state.aktiivne_teema
    teema = next((t for t in TEEMAD if t["id"] == teema_id), None)

    if teema:
        # Tagasi nupp
        if st.button("← Tagasi avalehele", key="back_home"):
            st.session_state.leht = "avaleht"
            st.session_state.aktiivne_teema = None
            st.rerun()

        st.markdown(f"""
        <div style='background:{teema["taust"]}; border-radius:14px; padding:1.5rem 1.75rem;
                    margin:1rem 0; border-top:4px solid {teema["värv"]};'>
            <div style='font-size:2.5rem; margin-bottom:0.5rem;'>{teema["ikoon"]}</div>
            <h1 style='font-family:"Cormorant Garamond",serif; font-size:1.75rem;
                       font-weight:600; color:{teema["värv"]}; margin:0; letter-spacing:-0.5px;'>
                {teema["pealkiri"]}
            </h1>
            <p style='color:#5A7A5C; font-size:0.9rem; margin-top:0.35rem;'>
                {teema["lühikirjeldus"]}
            </p>
        </div>
        """, unsafe_allow_html=True)

        tab_a, tab_b, tab_c = st.tabs(["ℹ️ Mis see on?", "✅ Soovitused", "💪 Kuidas toime tulla?"])

        with tab_a:
            st.markdown(teema["mis_on"])

            # Küsi assistendilt nupp
            st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
            if st.button(f"💬 Küsi assistendilt {teema['pealkiri']} kohta", key="ask_ai_teema"):
                st.session_state.leht = "assistent"
                st.session_state.kiirteema = f"Räägi mulle lähemalt {teema['pealkiri'].lower()} kohta."
                st.rerun()

        with tab_b:
            for s in teema["soovitused"]:
                st.markdown(f"""
                <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:9px;
                            padding:0.75rem 1rem; margin-bottom:0.5rem; font-size:0.9rem;
                            color:#1C1710; line-height:1.6;'>
                    {s}
                </div>
                """, unsafe_allow_html=True)

        with tab_c:
            st.markdown(teema["toimetulek"])

        # Seotud teemad
        st.markdown("""
        <div style='margin-top:1.5rem; font-size:0.72rem; font-weight:500; color:#8A9A89;
                    text-transform:uppercase; letter-spacing:0.1em; margin-bottom:0.75rem;'>
            Vaata ka
        </div>
        """, unsafe_allow_html=True)

        muud = [t for t in TEEMAD if t["id"] != teema_id][:3]
        cols = st.columns(3)
        for i, t in enumerate(muud):
            with cols[i]:
                if st.button(f"{t['ikoon']} {t['pealkiri']}", key=f"rel_{t['id']}", use_container_width=True):
                    st.session_state.aktiivne_teema = t["id"]
                    st.rerun()

# ── ASSISTENT ─────────────────────────────────────────────────────────────────

elif leht == "assistent":
    st.markdown("""
    <div style='padding:1.25rem 0 0.75rem;'>
        <h1 style='font-family:"Cormorant Garamond",serif; font-size:1.75rem;
                   font-weight:600; color:#2A4A33; margin:0;'>
            AI Assistent 💬
        </h1>
        <p style='color:#5A7A5C; font-size:0.82rem; margin-top:0.2rem;'>
            Sinu sõbralik kaasava õppimise nõustaja
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Kiirteemad
    st.markdown("""
    <div style='font-size:0.7rem; color:#8A9A89; text-transform:uppercase;
                letter-spacing:0.1em; margin-bottom:0.5rem;'>Kiirteemad</div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    kiir = [t["pealkiri"] for t in TEEMAD]
    for i, kt in enumerate(kiir):
        with cols[i % 4]:
            if st.button(TEEMAD[i]["ikoon"] + " " + kt, key=f"quick_{i}", use_container_width=True):
                st.session_state.kiirteema = f"Räägi mulle {kt.lower()} kohta."
                st.rerun()

    st.markdown("<hr style='border:none;border-top:0.5px solid #C8DEC9;margin:0.75rem 0;'>",
                unsafe_allow_html=True)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    def küsi_ai(sõnum: str):
        st.session_state.messages.append({"role": "user", "content": sõnum})
        with st.chat_message("user"):
            st.markdown(sõnum)
        with st.chat_message("assistant"):
            koht = st.empty()
            try:
                client = Groq()
                stream = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": CHAT_PROMPT}] + st.session_state.messages,
                    max_tokens=1000, temperature=0.7, stream=True,
                )
                tekst = ""
                for chunk in stream:
                    tekst += chunk.choices[0].delta.content or ""
                    koht.markdown(tekst + "▌")
                koht.markdown(tekst)
                st.session_state.messages.append({"role": "assistant", "content": tekst})
            except Exception as e:
                koht.error(f"⚠️ Viga: {str(e)}")
        st.rerun()

    if st.session_state.kiirteema:
        t = st.session_state.kiirteema
        st.session_state.kiirteema = None
        küsi_ai(t)

    if s := st.chat_input("Kirjuta oma küsimus siia... ✍️"):
        küsi_ai(s)

    if st.button("🗑 Tühjenda vestlus", key="clear_chat"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.rerun()

# ── LIHTNE KEEL ───────────────────────────────────────────────────────────────

elif leht == "lihtne":
    st.markdown("""
    <div style='padding:1.25rem 0 0.75rem;'>
        <h1 style='font-family:"Cormorant Garamond",serif; font-size:1.75rem;
                   font-weight:600; color:#2A4A33; margin:0;'>
            Lihtsa keele tööriist 📝
        </h1>
        <p style='color:#5A7A5C; font-size:0.82rem; margin-top:0.2rem;'>
            Muudab keerulise teksti lihtsaks ja kõigile arusaadavaks
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""<div style='font-size:0.75rem;font-weight:500;color:#2A4A33;
            text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;'>
            Algne tekst</div>""", unsafe_allow_html=True)

        algne = st.text_area("Algne tekst", label_visibility="collapsed",
            placeholder="Kleebi siia keeruline tekst...",
            height=300, key="lihtne_algne")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("📄 Näidis: koolikiri", use_container_width=True):
                st.session_state.lihtne_naide = """Lugupeetud lapsevanem, teavitame Teid, et vastavalt põhikooli- ja gümnaasiumiseaduse §-le 35 lõikele 2 on kooli juhtkond otsustanud rakendada Teie lapse suhtes käitumisnõuete rikkumise tõttu ajutist õppest kõrvaldamist perioodiks kolm õppepäeva."""
                st.rerun()
        with c2:
            if st.button("📋 Näidis: IÕK tekst", use_container_width=True):
                st.session_state.lihtne_naide = """Individuaalne õppekava on hariduslike erivajadustega õpilasele koostatud õppekava, mis lähtub riiklikust õppekavast ning on kohandatud vastavalt õpilase võimetele, vajadustele ja huvidele, arvestades tema terviseseisundit, erivajadusi ning pedagoogilis-psühholoogilise uurimise tulemusi."""
                st.rerun()

        if "lihtne_naide" in st.session_state:
            algne = st.session_state.lihtne_naide

        tase = st.select_slider("Lihtsustamise tase",
            options=["Veidi lihtsam", "Lihtsam", "Lihtne keel", "Väga lihtne keel"],
            value="Lihtne keel")

        if st.button("Teisenda lihtsasse keelde →", use_container_width=True, type="primary"):
            if not algne or len(algne.strip()) < 10:
                st.warning("Palun kleebi tekst!")
            else:
                tase_j = {"Veidi lihtsam": "Muuda veidi lihtsamaks.",
                          "Lihtsam": "Muuda selgelt lihtsamaks.",
                          "Lihtne keel": "Kasuta lihtsa keele põhimõtteid täielikult.",
                          "Väga lihtne keel": "Kasuta väga lihtsat keelt — max 10 sõna lauses."}
                with st.spinner("Lihtsustан..."):
                    try:
                        client = Groq()
                        v = client.chat.completions.create(
                            model="llama-3.3-70b-versatile",
                            messages=[{"role": "system", "content": LIHTNE_KEEL_PROMPT},
                                      {"role": "user", "content": f"{tase_j[tase]}\n\nTekst:\n{algne}"}],
                            max_tokens=1500, temperature=0.4,
                        )
                        st.session_state.lihtne_tulemus = v.choices[0].message.content
                        st.rerun()
                    except Exception as e:
                        st.error(f"⚠️ Viga: {str(e)}")

    with col2:
        st.markdown("""<div style='font-size:0.75rem;font-weight:500;color:#2A4A33;
            text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.5rem;'>
            Lihtne keel</div>""", unsafe_allow_html=True)

        if st.session_state.lihtne_tulemus:
            st.markdown(f"""
            <div style='background:#fff;border:0.5px solid #C8DEC9;border-radius:10px;
                        padding:1.1rem 1.25rem;min-height:300px;font-size:0.9rem;
                        line-height:1.75;color:#1C1710;white-space:pre-wrap;'>
                {st.session_state.lihtne_tulemus}
            </div>""", unsafe_allow_html=True)
            st.download_button("⬇ Lae alla (.txt)", data=st.session_state.lihtne_tulemus,
                               file_name="lihtne_keel.txt", mime="text/plain", use_container_width=True)
        else:
            st.markdown("""
            <div style='background:#fff;border:0.5px solid #C8DEC9;border-radius:10px;
                        padding:1.1rem 1.25rem;min-height:300px;font-size:0.88rem;
                        line-height:1.75;color:#8A9A89;font-style:italic;'>
                Lihtsustatud tekst ilmub siia...<br><br>
                Kleebi tekst vasakule ja vajuta "Teisenda"
            </div>""", unsafe_allow_html=True)

# ── TEKSTIKOGUMIK ─────────────────────────────────────────────────────────────

elif leht == "kogumik":
    st.markdown("""
    <div style='padding:1.25rem 0 0.75rem;'>
        <h1 style='font-family:"Cormorant Garamond",serif; font-size:1.75rem;
                   font-weight:600; color:#2A4A33; margin:0;'>
            Tekstikogumik lihtsas keeles 📚
        </h1>
        <p style='color:#5A7A5C; font-size:0.82rem; margin-top:0.2rem;'>
            Valmis tekstid kaasava hariduse teemadel — kõigile arusaadavas keeles
        </p>
    </div>
    """, unsafe_allow_html=True)

    for kategooria in LIHTSA_KEELE_TEKSTID:
        st.markdown(f"""
        <div style='font-size:0.85rem; font-weight:500; color:#2A4A33;
                    margin:1.25rem 0 0.75rem; padding-bottom:0.375rem;
                    border-bottom:0.5px solid #C8DEC9;'>
            {kategooria["kategooria"]}
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(kategooria["tekstid"]))
        for i, txt in enumerate(kategooria["tekstid"]):
            with cols[i]:
                with st.expander(txt["pealkiri"], expanded=False):
                    st.markdown(f"""
                    <div style='font-size:0.9rem; line-height:1.8; color:#1C1710;
                                white-space:pre-wrap; padding:0.5rem 0;'>
{txt["tekst"]}
                    </div>
                    """, unsafe_allow_html=True)
                    st.download_button(
                        "⬇ Lae alla",
                        data=txt["tekst"],
                        file_name=f"{txt['pealkiri'].replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"dl_{txt['pealkiri']}",
                        use_container_width=True
                    )

    st.markdown("""
    <div style='margin-top:1.5rem; background:#EAF5EB; border:0.5px solid #C8DEC9;
                border-radius:10px; padding:1rem 1.25rem; font-size:0.85rem; color:#3A5A3C;'>
        💡 <strong>Tahad ise teksti lihtsustada?</strong> Kasuta meie Lihtne keel tööriista!
    </div>
    """, unsafe_allow_html=True)

    if st.button("📝 Mine lihtsa keele tööriista juurde →", key="goto_lihtne"):
        st.session_state.leht = "lihtne"
        st.rerun()

# ── PÄEVA INSPIRATSIOON ───────────────────────────────────────────────────────

elif leht == "inspiratsioon":
    import datetime, hashlib

    LOOD = [
        {
            "nimi": "Temple Grandin",
            "aasta": "1947–",
            "valdkond": "Teadlane, kirjanik, loengu pidaja",
            "erivajadus": "Autism",
            "ikoon": "🐄",
            "värv": "#2A4A33",
            "lugu": """Temple Grandini diagnoos pandi autismiga umbes 2-aastaselt — tema arst ütles vanematele, et ta ei õpi kunagi rääkima.

Tema ema keeldus seda uskumast.

Temple õppis rääkima. Ta õppis koolis, kuigi klassikaaslased kiusasid teda. Ta läks ülikooli. Ta tegi doktorikraadi.

Temple leiutas revolutsioonilise karjasüsteemi, mis parandas miljonite loomade heaolu. Tema projekteerimismeetodid on kasutusel tänapäeval üle kogu maailma.

Ta on kirjutanud mitu aastat bestsellerit, peetud loenguid üle kogu maailma ja saanud auastmeid paljudelt ülikoolidelt.

Temple ütleb: **"Autism ei ole haigus, mida ravida. See on erinev viis mõelda."**

Tema elu näitab, et erinev mõtlemine ei ole takistus — see on superjõud. 💚""",
            "õppetund": "Erinev mõtlemine on tugevus, mitte nõrkus.",
        },
        {
            "nimi": "Stephen Hawking",
            "aasta": "1942–2018",
            "valdkond": "Füüsik, kosmoloog",
            "erivajadus": "ALS (amüotroofiline lateraalskleroos)",
            "ikoon": "🌌",
            "värv": "#1A4A7A",
            "lugu": """21-aastaselt diagnoositi Stephen Hawkingil ALS — haigus, mis halvab järk-järgult kogu keha.

Arstid ütlesid, et tal on elada kaks aastat.

Ta elas 76 aastani.

Neist viimased 50 aastat ei saanud ta liigutada praktiliselt ühtegi lihast. Ta rääkis arvutiga häälesünteesi kaudu, mida ta juhtis oma põse liigutustega.

Just nende aastate jooksul ta lõi oma suurimad teadustööd. Ta kirjutas raamatu "Aja lühike ajalugu", mis müüdi üle 10 miljoni eksemplari. Ta tõestas musta augu kiirguse olemasolu.

Stephen ütles: **"Olenemata sellest, kui raske elu tundub, on alati midagi, mida sa suudad teha ja milles saad edu saavutada."**

Tema elu on tõestus, et keha piirangud ei piira vaimu. 🌌""",
            "õppetund": "Piirangutest hoolimata on alati võimalik luua midagi suurt.",
        },

        {
            "nimi": "Agatha Christie",
            "aasta": "1890–1976",
            "valdkond": "Kirjanik",
            "erivajadus": "Düsleksia",
            "ikoon": "📖",
            "värv": "#7A3A1A",
            "lugu": """Agatha Christie ei osanud koolis hästi lugeda ega kirjutada. Tema käekiri oli katastroofiline. Õpetajad arvasid, et tal on probleeme õppimisega.

Tegelikult tal oli düsleksia.

Aga Agatha ema ei andnud alla. Ta luges tütrele ette, rääkis temaga lugudest, toetas teda.

Agatha Christie sai maailma enim loetud krimiromaanide autoriks.

Ta kirjutas 66 krimiromaani, 14 novellide kogu ja 20 näidendit. Tema raamatud on tõlgitud 103 keelde. Tema Poirot ja Miss Marple on ikoonilised tegelased.

Ta on enim tõlgitud ingliskeelne kirjanik pärast Shakespeare'i ja Piiblit.

Agatha ütles: **"Mu aastad koolis olid kõige õnnetumad ajad minu elus."** Aga need ei takistanud teda saavutamast seda, mida ta armastas. 📖""",
            "õppetund": "Kooliaastade raskused ei määra, mis sinust saab.",
        },
        {
            "nimi": "Nick Vujicic",
            "aasta": "1982–",
            "valdkond": "Motivatsioonikõneleja, kirjanik",
            "erivajadus": "Tetramelia sündroom — sündinud ilma jalgade ja käteta",
            "ikoon": "💪",
            "värv": "#5A3A7A",
            "lugu": """Nick Vujicic sündis ilma käteta ja jalgadeta — haruldane seisund nimega tetramelia sündroom.

Lapsena oli ta sügavas depressioonis. Ta püüdis 10-aastaselt ennast uppuda.

Aga ta jäi ellu. Ja siis midagi muutus.

Nick otsustas, et ta võib valida, kuidas elada. Ta õppis kirjutama varbaga. Ta õppis ujuma. Ta õppis jalgpalli mängima.

Ja ta hakkas rääkima teistele.

Täna on Nick Vujicic üks maailma kuulsamaid motivatsioonikõnelejaid. Ta on esinenud üle 60 riigis. Ta on kohtunud presidentide ja kuningatega. Ta on abielu, tal on lapsed.

Nick ütleb: **"Kui sul pole imesid, ole ise teistele ime."**

Tema lugu on vaadanud üle 100 miljoni inimese. 💪""",
            "õppetund": "Isegi siis, kui tundub, et kõik on vastu — saab valida, kuidas edasi minna.",
        },
        {
            "nimi": "Helen Keller",
            "aasta": "1880–1968",
            "valdkond": "Kirjanik, aktivist, loengupidaja",
            "erivajadus": "Kurtpimesus",
            "ikoon": "✋",
            "värv": "#1D7A5A",
            "lugu": """19 kuu vanuselt kaotas Helen Keller haiguse tõttu nii nägemise kui kuulmise.

Aastaid elas ta pimedas ja vaikses maailmas, suutmata ühenduda teistega.

Siis tuli Anne Sullivan — õpetaja, kes keeldus uskumast, et Helen ei saa õppida.

Anne kirjutas Heleni käele tähti. Päev päeva järel. Nädalaid. Kuid.

Ühel päeval — veehoidla juures — läks midagi loksuma. Helen mõistis, et igal asjal on nimi. See avanes talle nagu imeline maailm.

Helen õppis lugema, kirjutama, rääkima. Ta astus ülikooli — esimese kurtpimeda inimesena, kes lõpetas Harvardi ülikooli. Ta kirjutas 12 raamatut. Ta reisis 39 riiki.

Helen ütles: **"Ainuke asi, mis on hullem kui olla pime, on näha, aga mitte omada visiooni."** ✋""",
            "õppetund": "Üks hea õpetaja võib muuta kogu elu.",
        },
        {
            "nimi": "Michael Phelps",
            "aasta": "1985–",
            "valdkond": "Ujuja, 23 kuldmedali omanik",
            "erivajadus": "ADHD",
            "ikoon": "🏊",
            "värv": "#1A4A7A",
            "lugu": """9-aastaselt diagnoositi Michael Phelpsi ADHD — tähelepanupuudulikkuse ja hüperaktiivsuse häire.

Kooliarstid ütlesid ta emale, et Michael ei suuda kunagi milleski keskenduda.

Ema tõi ta basseini.

Vees leidis Michael midagi, mida ta polnud kunagi varem tundnud: võime täielikult keskenduda.

ADHD-ga inimesed on sageli võimelised hüperfookuseks — lõpmatu keskendumine millelegi, mis neid tõeliselt huvitab.

Michael Phelps on kõigi aegade enim medaliseeritud olümpiasportlane. 23 kulda, 3 hõbedat, 2 pronksi. Neljas olümpiamänges.

Ta ütleb: **"ADHD ei teinud minust halba sportlast — see tegi minust parema. See andis mulle fookuse, mida teistel ei ole."** 🏊""",
            "õppetund": "See, mis tundub puudusena, võib olla su kõige suurem tugevus.",
        },
        {
            "nimi": "Frida Kahlo",
            "aasta": "1907–1954",
            "valdkond": "Kunstnik",
            "erivajadus": "Poliomüeliit lapseeas, rasked vigastused avariis",
            "ikoon": "🎨",
            "värv": "#B8832A",
            "lugu": """6-aastaselt haigestus Frida Kahlo poliomüeliiti, mis jättis ta vasaku jala invaliidiks.

18-aastaselt sattus ta raskesse bussiavariisse. Selgroo murd, vaagna murd, 30 operatsiooni elus. Kuid haigevoodis.

Ema kinkis talle lõuendi.

Frida hakkas maalima. Esmalt iseennast — ainuke mudel, kes tal alati olemas oli. Siis tuli sellest kirg, missioon, identiteet.

Tema maalid räägivad valust, identiteedist, kehast, armastusest. Need on tänapäeval muuseumides üle maailma.

Tema nägu on ühel Mehhiko 500-peso rahatähel. Tema elust on tehtud film. Tema kunstiteosed müüvad miljonite eest.

Frida ütles: **"Jalgadel on valu, aga hing ei tee mulle haiget ja ma saan maalida."** 🎨""",
            "õppetund": "Piirangutest sünnib sageli suurim loovus.",
        },
        {
            "nimi": "Albert Einstein",
            "aasta": "1879–1955",
            "valdkond": "Füüsik, matemaatik",
            "erivajadus": "Kõnearengu hilinemine, tõenäoliselt autismi spekter",
            "ikoon": "⚛️",
            "värv": "#2A4A33",
            "lugu": """Albert Einstein ei rääkinud kuni 4 eluaastani. Kuni 7 eluaastani kordas ta iga lauset mitu korda enne kui jätkas.

Kooliõpetajad arvasid, et ta on aeglane. Üks õpetaja ütles otse: "Sinust ei saa mitte midagi."

Einstein jäeti ülikoolist välja. Ta ei leidnud tööd. Ta töötas patendibüroos lihttöölisena.

Just seal, vaba aega mõeldes, tuli tal füüsika suurim läbimurre.

1905. aastal — ühel aastal — avaldas ta neli teadusartiklit, millest igaüks muutis füüsikat igaveseks. Sealhulgas E=mc².

Einstein sai Nobeli füüsikapreemia. Tema nimi on muutunud geeniuse sünonüümiks.

Einstein ütles: **"Kujutlusvõime on olulisem kui teadmised."** ⚛️""",
            "õppetund": "Tavaline haridussüsteem ei mõõda kõiki andeid.",
        },
        {
            "nimi": "Simone Biles",
            "aasta": "1997–",
            "valdkond": "Võimleja, 30+ maailmameistri medali omanik",
            "erivajadus": "ADHD",
            "ikoon": "🤸",
            "värv": "#5A2A5A",
            "lugu": """Simone Bilesi kohta lekkis 2016. aastal, et ta võtab ADHD ravimeid.

Anonüümsed häkkerid üritasid seda tema vastu kasutada.

Simone vastas avalikult: **"Mul on ADHD ja ma olen võtnud ravimeid sellele — ei midagi häbeneda seal."**

Simone Biles on kõigi aegade parim võimleja. 30 maailmameistritiitlit. 7 olümpiamedalit. Ta on teinud elemendid, mis on nimetatud tema järgi — "Biles", "Biles II" — sest teised ei suuda neid järele teha.

Ta on ka üks esimesi tippsportlasi, kes rääkis avalikult vaimse tervise vajalikkusest — 2021. aastal Tokyo olümpiamängudelt kõrvale astunud, et oma psüühilist tervist kaitsta.

Tema julgus — nii spordiplatsil kui elus — on inspireerinud miljoneid. 🤸""",
            "õppetund": "Tõeline tugevus tähendab ka enda eest hoolitsemist.",
        },
        {
            "nimi": "Richard Branson",
            "aasta": "1950–",
            "valdkond": "Ettevõtja, Virgin Group asutaja",
            "erivajadus": "Düsleksia, ADHD",
            "ikoon": "🚀",
            "värv": "#7A3A1A",
            "lugu": """Richard Branson lahkus koolist 16-aastaselt. Ta ei suutnud lugeda ega arvutada hästi. Koolidirektor ütles talle: "Sa lõpetad kas vanglas või miljonärina."

Ta valis teise variandi.

Branson asutas üle 400 ettevõtte. Virgin Records, Virgin Atlantic, Virgin Galactic. Ta on astronaut, ta on purjetanud ümber maailma, ta on ületanud Atlandi ookeani õhupalliga.

Tema varandus on üle 10 miljardi euro.

Branson ütleb: **"Düsleksia andis mulle erioskused. Ma ei suuda meelde jätta pikkasid tekste, aga ma näen suurt pilti kiiremini kui keegi teine."**

Ta kasutab oma firma juhtimiseks spetsiaalseid süsteeme ja meeskonda, mis kompenseerib tema düsleksia. See on tema meelest eelis, mitte puudus. 🚀""",
            "õppetund": "Tee ümber, mis ei sobi — ära pea kinni sellest, kuidas teised teevad.",
        },
        {
            "nimi": "Aimee Mullins",
            "aasta": "1975–",
            "valdkond": "Sportlane, näitleja, modell, kõneleja",
            "erivajadus": "Sündinud ilma sääreluudeta — mõlemad jalad amputeeritud 1-aastaselt",
            "ikoon": "🏃",
            "värv": "#1D7A5A",
            "lugu": """Aimee Mullins sündis ilma sääreluudeta. Mõlemad jalad amputeeriti tal 1-aastaselt.

Proteeside ja tohutu tahtejõuga hakkas ta käima, jooksma, sportima.

Georgetown'i ülikoolis oli ta esimene amputeeritud sportlane, kes võistles ühes NCAA divisiooni I meeskonnas.

1996. aastal osales ta paralümpial, püstitas kolm maailmarekordit.

Seejärel muutis ta moemaailma — Alexander McQueen tegi talle puust nikerdatud proteesid, millega ta kõndis moelaval. Ajalehed kirjutasid temast kui "imekaunitarist".

Aimee ütleb: **"Sõna 'puudega' eeldab, et midagi on puudu. Mina ei tunne, et mul on midagi puudu. Minu proteesid on vahendid, mis annavad mulle rohkem võimalusi, mitte vähem."** 🏃""",
            "õppetund": "Meie nägemus piiridest on sageli palju kitsam kui tegelikkus.",
        },
    ]

    # Vali päeva lugu kuupäeva põhjal
    tana = datetime.date.today()
    paevaindex = tana.toordinal() % len(LOOD)
    lugu = LOOD[paevaindex]

    st.markdown(f"""
    <div style='padding:1.25rem 0 0.5rem;'>
        <h1 style='font-family:"Cormorant Garamond",serif; font-size:1.75rem;
                   font-weight:600; color:#2A4A33; margin:0;'>
            Päeva inspiratsioon ⭐
        </h1>
        <p style='color:#5A7A5C; font-size:0.82rem; margin-top:0.2rem;'>
            Iga päev uus tõeline lugu inimesest, kes on eriline ja edukas 💚
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Päeva lugu
    st.markdown(f"""
    <div style='background:linear-gradient(135deg, {lugu["värv"]}15, {lugu["värv"]}05);
                border:1px solid {lugu["värv"]}40; border-top:4px solid {lugu["värv"]};
                border-radius:16px; padding:1.75rem 2rem; margin-bottom:1.25rem;'>
        <div style='display:flex; align-items:flex-start; gap:1rem; margin-bottom:1rem;'>
            <div style='font-size:2.5rem; line-height:1;'>{lugu["ikoon"]}</div>
            <div>
                <h2 style='font-family:"Cormorant Garamond",serif; font-size:1.5rem;
                           font-weight:600; color:{lugu["värv"]}; margin:0;'>
                    {lugu["nimi"]}
                </h2>
                <div style='font-size:0.8rem; color:#5A7A5C; margin-top:0.2rem;'>
                    {lugu["aasta"]} · {lugu["valdkond"]}
                </div>
                <div style='display:inline-block; background:{lugu["värv"]}20;
                            border:0.5px solid {lugu["värv"]}50; border-radius:99px;
                            padding:0.2rem 0.75rem; font-size:0.72rem;
                            color:{lugu["värv"]}; margin-top:0.4rem;'>
                    {lugu["erivajadus"]}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Lugu ise
    st.markdown(f"""
    <div style='background:#fff; border:0.5px solid #C8DEC9; border-radius:12px;
                padding:1.5rem 1.75rem; margin-bottom:1rem; font-size:0.95rem;
                line-height:1.85; color:#1C1710; white-space:pre-wrap;'>{lugu["lugu"]}</div>
    """, unsafe_allow_html=True)

    # Õppetund
    st.markdown(f"""
    <div style='background:{lugu["värv"]}10; border-left:4px solid {lugu["värv"]};
                border-radius:0 10px 10px 0; padding:1rem 1.25rem; margin-bottom:1.25rem;'>
        <div style='font-size:0.7rem; font-weight:500; color:{lugu["värv"]};
                    text-transform:uppercase; letter-spacing:0.08em; margin-bottom:0.25rem;'>
            Täna meenuta
        </div>
        <div style='font-size:0.95rem; color:#2A4A33; font-style:italic;'>
            "{lugu["õppetund"]}"
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Kuupäev ja järgmine lugu
    st.markdown(f"""
    <div style='display:flex; justify-content:space-between; align-items:center;
                font-size:0.75rem; color:#8A9A89;'>
        <div>📅 {tana.strftime("%d.%m.%Y")} lugu · {paevaindex + 1}/{len(LOOD)}</div>
        <div>Homme tuleb uus inspiratsioon! ✨</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:0.5px solid #C8DEC9;margin:1.25rem 0;'>",
                unsafe_allow_html=True)

    # Kõik lood ruudustikus
    st.markdown("""
    <div style='font-size:0.72rem; font-weight:500; color:#8A9A89; text-transform:uppercase;
                letter-spacing:0.1em; margin-bottom:0.875rem;'>
        Kõik inspiratsioonilood
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(3)
    for i, l in enumerate(LOOD):
        with cols[i % 3]:
            ontan = (i == paevaindex)
            border = f"border-top:3px solid {l['värv']};" if ontan else f"border-top:1px solid {l['värv']}40;"
            bg = f"background:{l['värv']}10;" if ontan else "background:#fff;"
            if st.button(
                f"{l['ikoon']} {l['nimi']}" + (" ← täna" if ontan else ""),
                key=f"lugu_{i}", use_container_width=True
            ):
                st.session_state.valitud_lugu = i
                st.rerun()

    # Valitud lugu (muu kui täna)
    if "valitud_lugu" in st.session_state and st.session_state.valitud_lugu != paevaindex:
        vl = LOOD[st.session_state.valitud_lugu]
        st.markdown(f"""
        <div style='background:{vl["värv"]}08; border:0.5px solid {vl["värv"]}40;
                    border-top:3px solid {vl["värv"]}; border-radius:12px;
                    padding:1.5rem; margin-top:1rem;'>
            <div style='font-size:1.1rem; font-weight:600; font-family:"Cormorant Garamond",serif;
                        color:{vl["värv"]}; margin-bottom:0.25rem;'>
                {vl["ikoon"]} {vl["nimi"]}
            </div>
            <div style='font-size:0.75rem; color:#5A7A5C; margin-bottom:0.875rem;'>
                {vl["aasta"]} · {vl["valdkond"]} · {vl["erivajadus"]}
            </div>
            <div style='font-size:0.9rem; line-height:1.8; color:#1C1710;
                        white-space:pre-wrap;'>{vl["lugu"]}</div>
            <div style='margin-top:1rem; background:{vl["värv"]}15; border-radius:8px;
                        padding:0.75rem 1rem; font-size:0.88rem; color:#2A4A33; font-style:italic;'>
                "{vl["õppetund"]}"
            </div>
        </div>
        """, unsafe_allow_html=True)
