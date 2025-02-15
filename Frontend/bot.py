import base64
import streamlit as st
import requests
import os

# Set page configuration **as the very first Streamlit command**
st.set_page_config(
    page_title="SM VITA BOT",
    page_icon="\U0001F3E2",
    layout="wide"
)

API_GATEWAY_URL = "https://79mo988gpl.execute-api.us-east-1.amazonaws.com/dev/chatbot"

# Authentication
USERS = {
    "admin": "password123",
    "user1": "user1pass",
    "user2": "user2pass"
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "logout_clicked" not in st.session_state:
    st.session_state.logout_clicked = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

def login():
    st.title("SM VITA Bot Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.authenticated = True
            st.session_state.current_user = username
            st.session_state.logout_clicked = False
            st.rerun()
        else:
            st.error("Invalid username or password")

def logout():
    st.session_state.authenticated = False
    st.session_state.current_user = None
    st.session_state.chat_sessions = {}  # Clear chat sessions
    st.session_state.show_suggestions = True  # Reset suggestions

if not st.session_state.authenticated:
    login()
    st.stop()

st.sidebar.button("Logout", on_click=logout)

# Function to get chatbot response
def get_chatbot_response(user_input):
    try:
        response = requests.post(API_GATEWAY_URL, json={"query": user_input})
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "Error: No response from API")
            if 'claude' in chatbot_response.lower():
                chatbot_response = 'I am SM-VITA chatbot, a virtual assistant designed to provide information about SM VITA, CDAC programs, courses, admissions, and campus-related queries.'
            return chatbot_response
        else:
            return "⚠️ Error: Unable to reach chatbot API"
    except Exception as e:
        return f"⚠️ Error: {e}"

# Load Local image with error handling
logo_path = os.path.join(os.path.dirname(__file__), "VITA_logo.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()
else:
    st.warning("⚠️ Warning: Logo file `VITA_logo.png` not found! Upload it in the same directory.")
    logo_base64 = ""

# Initialize session state for each user
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
if st.session_state.current_user not in st.session_state.chat_sessions:
    st.session_state.chat_sessions[st.session_state.current_user] = []
if "show_suggestions" not in st.session_state:
    st.session_state.show_suggestions = True  # Only show suggestions at start

# Get the selected chat session
chat_session = st.session_state.chat_sessions[st.session_state.current_user]

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
        "📖 What are the exam dates for C-Cat?",
        "📅 What is the fees for Pre-Cat in SMVITA?",
        "🎓 What are the eligibility criteria for doing CDAC?",
        "📍 Where is SMVITA located?",
        "📝 How can I register for C-CAT?"
    ]
    
    num_columns = min(len(suggested_questions), 3)  # Adjust number of columns as needed
    cols = st.columns(num_columns)  # Create dynamic columns

    for idx, question in enumerate(suggested_questions):
        with cols[idx % num_columns]:  # Distribute buttons evenly across columns
            if st.button(question, key=f"q{idx}"):
                chat_session.append({"role": "user", "content": question})
                response = get_chatbot_response(question)
                chat_session.append({"role": "assistant", "content": response})
                st.session_state.show_suggestions = False  # Hide suggestions after first interaction
                st.rerun()

# Chat input field
user_query = st.chat_input("💬 Ask me about VITA courses, admission, and more...")
if user_query:
    st.session_state.show_suggestions = False
    chat_session.append({"role": "user", "content": user_query})
    response = get_chatbot_response(user_query)
    chat_session.append({"role": "assistant", "content": response})
    with st.chat_message("user"):
        st.markdown(user_query)
    with st.chat_message("assistant"):
        st.markdown(response)
