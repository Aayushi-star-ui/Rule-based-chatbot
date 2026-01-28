import streamlit as st
import pandas as pd
import re

# ===============================
# CONFIG
# ===============================
CSV_PATH = "data.csv"
df=pd.read_csv(CSV_PATH)

# ===============================
# STOPWORDS
# ===============================

EN_STOPWORDS = [
    "is","are","am","was","were","the","a","an","in","on","at","of","to",
    "for","what","why","how","where","when","who","which","do","does",
    "did","can","could","should","would","please"
]

HI_STOPWORDS = [
    "kya","kyu","kyun","kyon","kab","kaha","kahan","kaise","kaisa",
    "kaun","kon","kis","kisko","kisliye","liye","hai","ho","hoga",
    "hogi","tha","thi","the","me","mein","par","se","ko","ki","ka",
    "ke","aur","ya","to","hi","bhi","plz","please"
]

# ===============================
# FUNCTIONS
# ===============================

def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())

def remove_stopwords(words, lang):
    stopwords = EN_STOPWORDS if lang == "en" else HI_STOPWORDS
    return [w for w in words if w not in stopwords]

# ===============================
# LOAD DATA
# ===============================

df = pd.read_csv(CSV_PATH)
df["Keywords"] = df["Keywords"].fillna("").str.lower()
df["Answer"] = df["Answer"].fillna("")
df["Language"] = df["Language"].fillna("").str.lower()

# ===============================
# STREAMLIT UI
# ===============================

st.title("🤖 Rule Based Chatbot")

ui_lang = st.radio("Select language / भाषा चुनें", ["English", "Hindi"])
lang = "en" if ui_lang == "English" else "hi"

user_input = st.text_input("Type your question")

if user_input:
    text = user_input.lower()

    # Simple replies
    if text in ["hi","hello","hey","namaste","namaskar","hy"]:
        st.write("Hello 👋" if lang=="en" else "नमस्ते 🙏")

    elif text in ["ok","okay","haan","ha","theek","thik"]:
        st.write("Okay 👍" if lang=="en" else "ठीक है 👍")

    elif "thank" in text or "dhanyavaad" in text:
        st.write("You're welcome 🙂" if lang=="en" else "धन्यवाद 🙏")

    else:
        # NLP PROCESS
        words = tokenize(text)
        meaningful_words = remove_stopwords(words, lang)

        found = False

        for _, row in df.iterrows():
            keywords = [k.strip() for k in row["Keywords"].split(",")]

            # 🔥 MAIN LOGIC: ANY MATCH
            if any(w in keywords for w in meaningful_words):
                if row["Language"] == lang:
                    st.write(row["Answer"])
                    found = True
                    break

        if not found:
            st.write(
                "Sorry, I don’t have an answer for that."
                if lang=="en"
                else
                "माफ़ कीजिए, इस सवाल का जवाब उपलब्ध नहीं है।"

            )

