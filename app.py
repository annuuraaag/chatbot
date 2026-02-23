import streamlit as st
from rag_pipeline import run_rag

# ---------- Page Config ----------
st.set_page_config(
    page_title="RAG-Based Chatbot Avatar with LangGraph",
    page_icon="🧠",
    layout="centered"
)

# ---------- Clean Minimal Header ----------
st.title("RAG-Based Chatbot Avatar with LangGraph")
st.caption(
    "A Retrieval-Augmented Generation system with dynamic workflow orchestration"
)

# ---------- Session State ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Chat Input ----------
query = st.chat_input("Ask something about your knowledge base...")

if query:
    answer = run_rag(query)

    st.session_state.history.append(("user", query))
    st.session_state.history.append(("bot", answer))

# ---------- Display Chat ----------
for role, msg in st.session_state.history:
    if role == "user":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)