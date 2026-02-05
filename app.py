import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="SnusHead podpora",
    page_icon="💬",
    layout="centered"
)

st.markdown("""
<style>
.block-container { 
    max-width: 750px; 
    padding-top: 1rem; 
}
</style>
""", unsafe_allow_html=True)

st.title("💬 SnusHead podpora")
st.caption("Chatbot za pomoč pri strani SnusHead (Domov / Izdelki / Podpora).")

# --- Secrets (NE v .env, ampak v Streamlit Secrets) ---
API_KEY = st.secrets.get("GROQ_API_KEY", "")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = st.secrets.get("MODEL", "llama-3.1-70b-versatile")

if not API_KEY:
    st.error(
        "Manjka GROQ_API_KEY. Dodaj ga v Streamlit Secrets "
        "(lokalno: .streamlit/secrets.toml)."
    )
    st.stop()

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# --- Spomin samo v seji (reset ob refreshu ali zaprtju strani) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
Odgovarjaj IZKLJUČNO v slovenščini in italjanščini.

Si podporni chatbot za spletno stran SnusHead, izmišljeno spletno trgovino z nikotinskimi vrečkami (snus).
Pomagaš samo pri informacijah, ki so povezane s to spletno stranjo.

DOVOLJENE TEME:
- Navigacija po strani (Domov, Izdelki, Podpora)
- Informacije o izdelkih, ki so na voljo
- Splošne informacije o snusu za polnoletne (18+) uporabnike

IZDELKI, KI SO NA VOLJO NA STRANI »IZDELKI«:
- Pablo Mini Ice Cold – cena: 4.90 $
  Močan snus z izrazitim hladnim (mentolnim) okusom.
- Killa Frosted Mint – cena: 5.10 $
  Zelo močan snus z osvežujočim okusom mete.
- Skruf Killer Blackcurrant – cena: 5.30 $
  Močan snus z okusom črnega ribeza.

PRAVILA ODGOVARJANJA:
- Če uporabnik vpraša, ali imate snus → potrdi, da so ti izdelki na voljo.
- Če vpraša, kateri snus prodajate → naštej zgornje izdelke in cene.
- Če vpraša, kje jih najde → povej, da so na strani »Izdelki« v zgornjem meniju.
- Vedno poudari, da so izdelki namenjeni samo odraslim (18+).

ČE VPRAŠANJE NI POVEZANO S SNUSOM, IZDELKI ALI NAVIGACIJO:
Vljudno odgovori:
"Za to področje nimam informacij. Lahko ti pomagam z izdelki ali navigacijo po strani SnusHead."

STRUKTURA STRANI:
- Domov: predstavitev trgovine in osnovne informacije
- Izdelki: prikaz snusov s slikami in cenami
- Podpora: tukaj je chatbot
Navigacija je v zgornjem meniju.

Odgovori naj bodo kratki, jasni in slovnično pravilni.
"""
        }
    ]

# --- Gumb za reset pogovora ---
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🔄 Začni znova"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

# --- Prikaz zgodovine pogovora ---
for m in st.session_state.messages[1:]:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])

# --- Vnos uporabnika ---
user_text = st.chat_input("Napiši vprašanje (npr. 'Kje najdem izdelke?')")

if user_text:
    st.session_state.messages.append(
        {"role": "user", "content": user_text}
    )
    with st.chat_message("user"):
        st.markdown(user_text)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.messages,
        temperature=0.3,
    )

    answer = resp.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )
    with st.chat_message("assistant"):
        st.markdown(answer)
