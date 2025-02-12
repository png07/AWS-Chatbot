import base64
import streamlit as st
import requests
from PIL import Image
import os

API_GATEWAY_URL = "https://79mo988gpl.execute-api.us-east-1.amazonaws.com/dev/chatbot"

# Function to get chatbot response
def get_chatbot_response(user_input):
    try:
        response = requests.post(API_GATEWAY_URL, json={"query": user_input})
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "Error: No response from API")
            if 'claude' in chatbot_response.lower():
                chatbot_response = 'I am SM-VITA chatbot, virtual assistant designed to provide information about SM VITA, CDAC programs, courses, admissions, and campus-related queries.'
            return chatbot_response
        else:
            return "\u26a0\ufe0f Error: Unable to reach chatbot API"
    except Exception as e:
        return f"\u26a0\ufe0f Error: {e}"

# Load Local image with error handling
logo_path = os.path.join(os.path.dirname(__file__), "VITA_logo.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()
else:
    st.warning("⚠️ Warning: Logo file `VITA_logo.png` not found! Upload it in the same directory.")
    logo_base64 = ""

# Config Streamlit page with fallback for missing logo
st.set_page_config(
    page_title="SM VITA",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state for chat history
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [[]]
if "current_session" not in st.session_state:
    st.session_state.current_session = 0
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True  # Only show suggestions at start
if "chat_count" not in st.session_state:
    st.session_state.chat_count = 0  # Track number of queries

MAX_CHATS = 10  # Limit of queries per session

# Get the selected chat session
chat_session = st.session_state.chat_sessions[st.session_state.current_session]

# Display chat header
st.markdown(
    f"""
    <div style="display: flex; align-items: center; text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" width="150">
        <h2 style="margin: 0; font-size: 50px; font-weight: bold;">SMVITA Bot</h2>
    </div>
    <p style="text-align: left; font-size: 20px;">Hello, I am <b>SMVITA Bot</b> 😎 and I will try my best to resolve all your VITA-related queries.</p>
    """, unsafe_allow_html=True
)

# Display chat history
for message in chat_session:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Suggested Questions (Only show at the start)
if st.session_state.show_suggestions and not chat_session:
    st.markdown("#### 🔥 Suggested Questions:")
    
    suggested_questions = [
        "📚 What are the courses offered by SMVITA?",
        "📖 What are the exam dates for C-Cat?",
        "📅 What is the fees for Pre-Cat in SMVITA?",
        "🎓 What are the eligibility criteria for doing CDAC?",
        "📍 Where is SMVITA located?",
        "📝 How can I register for C-CAT?"
    ]
    
    cols = st.columns(3)
    for idx, question in enumerate(suggested_questions):
        with cols[idx % 3]:
            if st.button(question, key=f"q{idx}"):
                st.session_state["user_input"] = question
                st.session_state.show_suggestions = False
                st.rerun()

# Check if the limit is reached
if st.session_state.chat_count >= MAX_CHATS:
    st.warning("Chat limit reached (10 queries per session)")
else:
    # User input
    user_query = st.chat_input("💬 Ask me about VITA courses, admission, and more...")
    if "user_input" in st.session_state:
        user_query = st.session_state["user_input"]
        del st.session_state["user_input"]

    if user_query:
        st.session_state.show_suggestions = False
        chat_session.append({"role": "user", "content": user_query})
        response = get_chatbot_response(user_query)
        chat_session.append({"role": "assistant", "content": response})
        st.session_state.chat_count += 1
        
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            st.markdown(response)
