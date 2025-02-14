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

# Function to load chat count and last reset time
def load_chat_count():
    if not os.path.exists(CHAT_COUNT_FILE):
        return 0, time.time()  # Start fresh

    with open(CHAT_COUNT_FILE, "r") as file:
        data = file.read().split()
        if len(data) == 2:
            count, last_reset = int(data[0]), float(data[1])
        else:
            count, last_reset = 0, time.time()  # Fallback case

    # Reset after 1 hour (3600 seconds)
    if time.time() - last_reset > 3600: 
        return 0, time.time()  # Reset chat count

    return count, last_reset

# Function to save chat count and last reset time
def save_chat_count(count, last_reset):
    with open(CHAT_COUNT_FILE, "w") as file:
        file.write(f"{count} {last_reset}")

# Load chat count and timestamp
chat_count, last_reset_time = load_chat_count()

# Function to get chatbot response
def get_chatbot_response(user_input):
    global chat_count, last_reset_time  # Ensure correct scope handling

    if chat_count >= 10:  # Limit is 10 queries per day
        return "⚠️ You have reached the limit of 10 queries. Please wait before asking more."

    try:
        response = requests.post(API_GATEWAY_URL, json={"query": user_input})
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "Error: No response from API")
            if 'claude' in chatbot_response.lower():
                chatbot_response = 'I am SM-VITA chatbot, a virtual assistant designed to provide information about SM VITA, CDAC programs, courses, admissions, and campus-related queries.'

            # Increment and save chat count
            chat_count += 1
            save_chat_count(chat_count, last_reset_time)  # Persist count across refresh
            return chatbot_response
        else:
            return "⚠️ Error: Unable to reach chatbot API"
    except Exception as e:
        return f"⚠️ Error: {e}"

# Initialize session state for chat history
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = [[]]
if "current_session" not in st.session_state:
    st.session_state.current_session = 0
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True  # Only show suggestions at start

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

    num_columns = min(len(suggested_questions), 3)  # Adjust number of columns as needed
    cols = st.columns(num_columns)  # Create dynamic columns

    for idx, question in enumerate(suggested_questions):
        with cols[idx % num_columns]:  # Distribute buttons evenly across columns
            if st.button(question, key=f"q{idx}"):
                st.session_state["user_input"] = question
                st.session_state.show_suggestions = False  # Hide suggestions after first interaction
                st.rerun()

# Check if the limit is reached
if chat_count >= 10:
    st.warning("🚨 Chat limit reached (10 queries). Please try again later.")
else:
    # User input
    user_query = st.chat_input("💬 Ask me about VITA courses, admission, and more...")
    if "user_input" in st.session_state:
        user_query = st.session_state["user_input"]
        del st.session_state["user_input"]

    if user_query:
        # Hide suggestions after first user query
        st.session_state.show_suggestions = False

        # Store user query
        chat_session.append({"role": "user", "content": user_query})

        # Get chatbot response
        response = get_chatbot_response(user_query)
        chat_session.append({"role": "assistant", "content": response})

        # Display messages
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            st.markdown(response)
