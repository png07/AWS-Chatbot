import streamlit as st
import requests
import json

# API Endpoint
API_URL = "https://79mo988gpl.execute-api.us-east-1.amazonaws.com/dev/chatbot"

# Streamlit UI
st.title("Chatbot Interface")
st.write("Ask the chatbot anything!")

# Initialize chat history if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.text_input("You:", "", key="user_input")

if st.button("Send") and user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call API
    payload = json.dumps({"query": user_input})
    headers = {'Content-Type': 'application/json'}
    response = requests.post(API_URL, headers=headers, data=payload)

    # Get response
    if response.status_code == 200:
        bot_response = response.json().get("response", "No response from chatbot.")
    else:
        bot_response = "Error communicating with chatbot."

    # Add bot response to chat history
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Refresh chat
    st.rerun()