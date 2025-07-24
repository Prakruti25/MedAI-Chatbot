import streamlit as st
import os
import openai

# Load API credentials from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]
openai.api_base = st.secrets["OPENAI_BASE_URL"]

# Streamlit UI setup
st.set_page_config(page_title="MedAI Chatbot", page_icon="🩺")
st.title("🩺 MedAI Chatbot")
st.write("Describe your symptoms, and I'll give general health guidance.")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("What are your symptoms?")
if prompt:
    # Store user input
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show assistant reply placeholder
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🧠 Thinking...")

        try:
            # Add system message for MedAI persona
            full_messages = [
                {
                    "role": "system",
                    "content": """
You are MedAI, a kind and knowledgeable AI health assistant.
When a user describes their symptoms, respond in **3 parts**:
1. **Possible Explanation** – Likely causes (not a diagnosis)
2. **Recommended Next Steps** – Suggestions like rest, fluids, doctor visit
3. **Panic Level** – One of: Low / Medium / High
Be helpful, calm, and responsible.
"""
                }
            ] + st.session_state.messages

            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=full_messages,
                temperature=0.7
            )
            reply = response["choices"][0]["message"]["content"]

        except Exception as e:
            reply = f"⚠️ Error: {e}"

        # Display and store assistant reply
        message_placeholder.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
