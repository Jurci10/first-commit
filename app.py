import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="SnusHead podpora", page_icon="💬", layout="centered")

st.markdown("""
<style>
.block-container { max-width: 750px; padding-top: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("💬 SnusHead podpora")
st.caption("Chatbot za pomoč pri strani SnusHead (Domov / Izdelki / Podpora).")

# --- Secrets (NE v .env, ampak v Streamlit Secrets) ---
API_KEY = st.secrets.get("GROQ_API_KEY", "")
BASE_URL = "https://api.groq.com/openai/v1"
MODEL = st.secrets.get("MODEL", "llama-3.1-70b-versatile")

if not API_KEY:
    st.error("Manjka GROQ_API_KEY. Dodaj ga v Streamlit Secrets (lokalno: .streamlit/secrets.toml).")
    st.stop()

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

# --- Spomin samo v seji (reset ob refresh/odhoda) ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "Odgovarjaj IZKLJUČNO v slovenščini. "
                "Si podporni chatbot za spletno stran SnusHead. "
                "Dovoljene teme so: navigacija po strani (Domov, Izdelki, Podpora), "
                "informacije o izdelkih na strani Izdelki in splošne informacije o snusu za odrasle (18+). "
                "Če vprašanje ni povezano s temi temami, vljudno povej, da za to področje nimaš informacij. "
                "Odgovori naj bodo kratki, pregledni in slovnično pravilni.\n\n"
                "Struktura strani:\n"
                "- Domov: predstavitev trgovine in osnovne informacije.\n"
                "- Izdelki: prikaz izdelkov s slikami in cenami.\n"
                "- Podpora: tukaj je chatbot.\n"
                "Navigacija je v zgornjem meniju."
            )
        }
    ]

col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🔄 Začni znova"):
        st.session_state.messages = st.session_state.messages[:1]
        st.rerun()

for m in st.session_state.messages[1:]:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        st.markdown(m["content"])

user_text = st.chat_input("Napiši vprašanje (npr. 'Kje najdem izdelke?')")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    resp = client.chat.completions.create(
        model=MODEL,
        messages=st.session_state.messages,
        temperature=0.3,
    )
    answer = resp.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
