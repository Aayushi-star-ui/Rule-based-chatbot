import streamlit as st
import pandas as pd
import re
import time

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)

# ===============================
# SESSION STATE (Chat History)
# ===============================
if "chat" not in st.session_state:
    st.session_state.chat = []

# ===============================
# CUSTOM CSS (LIGHT & EYE-FRIENDLY)
# ===============================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #a18cd1, #84fab0, #fbc2eb);
    background-size: 400% 400%;
    animation: gradientBG 20s ease-in-out infinite;
    color: #111827;
}

@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

.chat {
    max-height: 420px;
    overflow-y: auto;
    margin-top: 15px;
}

.user {
    background: #f9a8d4;
    color: #111827;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: right;
    font-weight: 500;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}

.bot {
    background: #7dd3fc;
    color: #111827;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: left;
    font-weight: 500;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
}
</style>
""", unsafe_allow_html=True)

# ===============================
# DATA LOAD
# ===============================
CSV_PATH = r"C:\Users\hp\OneDrive\Desktop\Final_bot\data.csv"

df = pd.read_csv(CSV_PATH)
df["Keywords"] = df["Keywords"].fillna("").str.lower()
df["Answer"] = df["Answer"].fillna("")
df["Language"] = df["Language"].fillna("").str.lower()

# ===============================
# FUNCTIONS
# ===============================
def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

# ===============================
# UI
# ===============================
st.markdown(
    "<h1 style='text-align:center;'>🤖 Rule-Based Chatbot</h1>",
    unsafe_allow_html=True
)

# Language selection
lang_ui = st.radio("🌍 Select Language / भाषा चुनें", ["English", "Hindi"])
lang = "en" if lang_ui == "English" else "hi"

# Suggested questions
st.write("💡 Suggested Questions:")
cols = st.columns(3)
suggestions = ["Admission process", "Fee structure", "Courses offered"]

for i, q in enumerate(suggestions):
    if cols[i].button(q):
        st.session_state.user_input = q

# User input
user_input = st.text_input("💬 Ask me something...", key="user_input")

# ===============================
# CHAT LOGIC
# ===============================
if user_input:
    st.session_state.chat.append(("user", user_input))

    with st.spinner("🤖 Bot is thinking..."):
        time.sleep(1)

    words = tokenize(user_input)
    response = ""

    for _, row in df.iterrows():
        keywords = [k.strip() for k in row["Keywords"].split(",")]
        if any(w in keywords for w in words) and row["Language"] == lang:
            response = row["Answer"]
            break

    if response == "":
        response = (
            "Sorry, I don’t have an answer for that 😔"
            if lang == "en"
            else "माफ़ कीजिए, इस सवाल का जवाब उपलब्ध नहीं है 😔"
        )

    response += " 😊"
    st.session_state.chat.append(("bot", response))

# ===============================
# DISPLAY CHAT
# ===============================
st.markdown("<div class='chat'>", unsafe_allow_html=True)

for sender, msg in st.session_state.chat:
    if sender == "user":
        st.markdown(f"<div class='user'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot'>{msg}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ===============================
# FOOTER
# ===============================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; opacity:0.8;'>✨ Designed by Chatbot Innovators | G.M.N. College Ambala Cantt</div>",
    unsafe_allow_html=True
)
