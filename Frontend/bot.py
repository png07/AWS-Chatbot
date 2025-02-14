import base64
import streamlit as st
import requests
import time
import os
from datetime import datetime, timedelta

import streamlit_cookie_manager

API_GATEWAY_URL = "https://79mo988gpl.execute-api.us-east-1.amazonaws.com/dev/chatbot"

# Initialize cookie manager
cookie_manager = streamlit_cookie_manager.CookieManager()

# Function to get or set user chat count in cookies
def get_user_chat_count():
    # Fetch existing count and timestamp from cookies
    count = cookie_manager.get_cookie("chat_count")
    last_reset_time = cookie_manager.get_cookie("chat_reset_time")

    # If cookies are missing, initialize them
    if count is None or last_reset_time is None:
        count = 0
        last_reset_time = time.time()
        cookie_manager.set_cookie("chat_count", str(count), expires_at=datetime.now() + timedelta(hours=1))
        cookie_manager.set_cookie("chat_reset_time", str(last_reset_time), expires_at=datetime.now() + timedelta(hours=1))
    
    # Convert values
    count = int(count)
    last_reset_time = float(last_reset_time)

    # Reset count if 1 hour has passed
    if time.time() - last_reset_time > 60:
        count = 0
        last_reset_time = time.time()
        cookie_manager.set_cookie("chat_count", str(count), expires_at=datetime.now() + timedelta(hours=1))
        cookie_manager.set_cookie("chat_reset_time", str(last_reset_time), expires_at=datetime.now() + timedelta(hours=1))

    return count, last_reset_time

# Function to update user chat count
def update_user_chat_count(count):
    cookie_manager.set_cookie("chat_count", str(count), expires_at=datetime.now() + timedelta(hours=1))

# Load user-specific chat count
chat_count, last_reset_time = get_user_chat_count()

# Function to get chatbot response
def get_chatbot_response(user_input):
    global chat_count

    if chat_count >= 2:  # Per-user limit
        return "⚠️ You have reached the limit of 10 queries. Please wait before asking more."

    try:
        response = requests.post(API_GATEWAY_URL, json={"query": user_input})
        if response.status_code == 200:
            chatbot_response = response.json().get("response", "Error: No response from API")
            if 'claude' in chatbot_response.lower():
                chatbot_response = 'I am SM-VITA chatbot, a virtual assistant designed to provide information about SM VITA, CDAC programs, courses, admissions, and campus-related queries.'

            # Increment and store count in cookies
            chat_count += 1
            update_user_chat_count(chat_count)

            return chatbot_response
        else:
            return "⚠️ Error: Unable to reach chatbot API"
    except Exception as e:
        return f"⚠️ Error: {e}"

# Streamlit UI
st.set_page_config(
    page_title="SM VITA",
    page_icon="🏢",
    layout="wide"
)

st.title("SMVITA Bot")

# Check if user limit is reached
if chat_count >= 2:
    st.warning("🚨 Chat limit reached (10 queries). Please try again later.")
else:
    user_query = st.chat_input("💬 Ask me about VITA courses, admission, and more...")
    if user_query:
        response = get_chatbot_response(user_query)
        st.chat_message("user").markdown(user_query)
        st.chat_message("assistant").markdown(response)
