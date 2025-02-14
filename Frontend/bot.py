import base64
import streamlit as st
import requests
import time
import hashlib
import os
from datetime import datetime, timedelta

# API Gateway URL
API_GATEWAY_URL = "https://79mo988gpl.execute-api.us-east-1.amazonaws.com/dev/chatbot"

# Helper function to get user's unique ID (stored in session state)
def get_user_id():
    if "user_id" not in st.session_state:
        # Generate a unique ID using the current timestamp and a random value
        user_fingerprint = str(time.time()) + os.urandom(16).hex()
        hashed_id = hashlib.sha256(user_fingerprint.encode()).hexdigest()
        # Store user_id in session state
        st.session_state.user_id = hashed_id
    return st.session_state.user_id

# Function to get current chat count from query parameters
def load_chat_count():
    user_id = get_user_id()
    current_time = time.time()
    
    # Retrieve stored chat data from query parameters
    chat_data = st.query_params.get("chat_data", [{}])
    if isinstance(chat_data, list) and chat_data:
        chat_data = chat_data[0]

    if isinstance(chat_data, str):
        chat_data = eval(chat_data)  # Convert string to dictionary

    # Check if reset is needed
    last_reset = chat_data.get("last_reset", 0)
    if current_time - last_reset > 60:  # 1 hour limit
        chat_data = {"count": 0, "last_reset": current_time}

    # Store chat count persistently
    st.session_state[f"chat_count_{user_id}"] = chat_data
    st.query_params.update(chat_data=str(chat_data))  # Store in URL
    return chat_data

# Function to update and save chat count
def save_chat_count():
    user_id = get_user_id()
    chat_data = load_chat_count()
    chat_data["count"] += 1  # Increment count

    # Save updated data
    st.session_state[f"chat_count_{user_id}"] = chat_data
    st.query_params.update(chat_data=str(chat_data))  # Persist in URL

# Load user chat count
user_data = load_chat_count()
chat_count = user_data["count"]

# Function to get chatbot response
def get_chatbot_response(user_input):
    global chat_count  
    if chat_count >= 2:  # Enforce limit of 10 queries per user
        return "⚠ You have reached the limit of 10 queries. Please wait before asking more."
    try:
        response = requests.post(API_GATEWAY_URL, json={"query": user_input})
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "Error: No response from API")
            if 'claude' in chatbot_response.lower():
                chatbot_response = 'I am SM-VITA chatbot, a virtual assistant designed to provide information about SM VITA, CDAC programs, courses, admissions, and campus-related queries.'
            save_chat_count()
            return chatbot_response
        else:
            return "⚠ Error: Unable to reach chatbot API"
    except Exception as e:
        return f"⚠ Error: {e}"

# Load Local image with error handling
logo_path = os.path.join(os.path.dirname(__file__), "VITA_logo.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()
else:
    st.warning("⚠ Warning: Logo file VITA_logo.png not found! Upload it in the same directory.")
    logo_base64 = ""

# Config Streamlit page 
st.set_page_config(
    page_title="SM VITA",
    page_icon="🏢",
    layout="wide"
)

# Initialize session state for chat history
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [[]]
if "current_session" not in st.session_state:
    st.session_state.current_session = 0
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True

# Get the selected chat session
chat_session = st.session_state.chat_sessions[st.session_state.current_session]

# Display chat history
st.markdown(
    f"""
    <div style="display: flex; align-items: center; text-align: center;">
        <img src="data:image/png;base64,{logo_base64}" width="150">
        <h2 style="margin: 0; font-size: 50px; font-weight: bold;">SMVITA Bot</h2>
    </div>
    <p style="text-align: left; font-size: 20px;">Hello, I am <b>SMVITA Bot</b> 😎 and I will try my best to resolve all your VITA-related queries.</p>
    """, unsafe_allow_html=True
)

for message in chat_session:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Suggested Questions (Only show at the start)
if st.session_state.show_suggestions and not chat_session:
    st.markdown("#### 🔥 Suggested Questions:")
    suggested_questions = [
        "📚 What are the courses offered by SMVITA?",
        "📚 What are the exam dates for C-Cat?",
        "📅 What is the fee for Pre-Cat in SMVITA?",
        "🎓 What are the eligibility criteria for doing CDAC?",
        "📍 Where is SMVITA located?",
        "📝 How can I register for C-CAT?"
    ]
    num_columns = min(len(suggested_questions), 3)
    cols = st.columns(num_columns)
    for idx, question in enumerate(suggested_questions):
        with cols[idx % num_columns]:
            if st.button(question, key=f"q{idx}"):
                st.session_state["user_input"] = question
                st.session_state.show_suggestions = False
                st.rerun()

if chat_count >= 10:
    st.warning("🚨 Chat limit reached (10 queries). Please try again later.")
else:
    user_query = st.chat_input("💬 Ask me about VITA courses, admission, and more...")
    if "user_input" in st.session_state:
        user_query = st.session_state["user_input"]
        del st.session_state["user_input"]
    if user_query:
        st.session_state.show_suggestions = False
        chat_session.append({"role": "user", "content": user_query})
        response = get_chatbot_response(user_query)
        chat_session.append({"role": "assistant", "content": response})
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            st.markdown(response)
