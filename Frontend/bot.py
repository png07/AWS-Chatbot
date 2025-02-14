import base64
import streamlit as st
import requests
import os
import time

# Configure Streamlit page
st.set_page_config(
    page_title="SM VITA",
    page_icon="🏢",
    layout="wide"
)

API_GATEWAY_URL = "https://79mo988gpl.execute-api.us-east-1.amazonaws.com/dev/chatbot"
CHAT_COUNT_FILE = "chat_count.txt"

# Function to encode image to base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    return None  # Return None if file is missing

# Load logo
logo_base64 = get_base64_image("VITA_logo.png")

# Function to load chat count and last reset time
def load_chat_count():
    if not os.path.exists(CHAT_COUNT_FILE):
        return 0, time.time()  

    with open(CHAT_COUNT_FILE, "r") as file:
        data = file.read().split()
        if len(data) == 2:
            count, last_reset = int(data[0]), float(data[1])
        else:
            count, last_reset = 0, time.time()  

    if time.time() - last_reset > 3600:  # Reset after 1 hour
        return 0, time.time()  

    return count, last_reset

# Function to save chat count
def save_chat_count(count, last_reset):
    with open(CHAT_COUNT_FILE, "w") as file:
        file.write(f"{count} {last_reset}")

# Load chat count
chat_count, last_reset_time = load_chat_count()

# Function to get chatbot response
def get_chatbot_response(user_input):
    global chat_count, last_reset_time

    if chat_count >= 10:  
        return "⚠️ You have reached the limit of 10 queries. Please wait before asking more."

    try:
        response = requests.post(API_GATEWAY_URL, json={"query": user_input})
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "Error: No response from API")
            if 'claude' in chatbot_response.lower():
                chatbot_response = 'I am SM-VITA chatbot, a virtual assistant for SM VITA, answering queries about CDAC courses, admissions, and campus information.'

            chat_count += 1
            save_chat_count(chat_count, last_reset_time)
            return chatbot_response
        else:
            return "⚠️ Error: Unable to reach chatbot API"
    except Exception as e:
        return f"⚠️ Error: {e}"

# Initialize session state
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [[]]
if "current_session" not in st.session_state:
    st.session_state.current_session = 0
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True  

# Get current chat session
chat_session = st.session_state.chat_sessions[st.session_state.current_session]

# Display chat history
if logo_base64:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; text-align: center;">
            <img src="data:image/png;base64,{logo_base64}" width="150">
            <h2 style="margin: 0; font-size: 50px; font-weight: bold;">SMVITA Bot</h2>
        </div>
        <p style="text-align: left; font-size: 20px;">Hello, I am <b>SMVITA Bot</b> 😎 and I will try my best to resolve all your VITA-related queries.</p>
        """, unsafe_allow_html=True
    )
else:
    st.warning("⚠️ Logo file 'VITA_logo.png' not found. Please ensure it is in the correct directory.")

for message in chat_session:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Suggested Questions
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

# Check query limit
if chat_count >= 10:
    st.warning("🚨 Chat limit reached (10 queries). Please try again later.")
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

        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            st.markdown(response)
