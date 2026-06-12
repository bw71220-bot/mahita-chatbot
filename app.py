import streamlit as st
from google import genai

# Setup the web page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")
st.title("🤖 My AI Chatbot")

# Define the API Key variable
# Replace the string below with your actual Gemini API key from Google AI Studio
API_KEY = "AQ.Ab8RN6K8pWM0mwuTFHF6bAQTjRttH5HAzQ-LXeUkmk6282gNiw" 

if API_KEY == "PASTE_YOUR_GEMINI_API_KEY_HERE":
    st.warning("Please insert your actual Gemini API Key into the code.")
else:
    # Initialize the Google GenAI client
    client = genai.Client(api_key=API_KEY)

    # Initialize the session state for chat history if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Handle new user input
    if prompt := st.chat_input("Ask me anything..."):
        # Display user message and add to history
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Generate and display assistant response
        with st.chat_message("assistant"):
            try:
                # Call the Gemini 3 Flash Preview model
                response = client.models.generate_content(
                    model='gemini-3-flash-preview', 
                    contents=prompt,
                )
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"An error occurred: {e}")