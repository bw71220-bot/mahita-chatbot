import streamlit as st
import google.generativeai as genai

# 1. Configure the Streamlit page layout and title
st.set_page_config(page_title="Mahita AI Chatbot", page_icon="🤖")
st.title("🤖 My AI Chatbot")

# 2. Safely read and configure the Gemini API Key from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except Exception as e:
    st.error("Please add your 'GEMINI_API_KEY' in your Streamlit Dashboard Secrets first!")
    st.stop()

# 3. Initialize chat history in session state so messages persist on refresh
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Render existing chat history onto the interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Accept dynamic user input (e.g., "Hi", "Bye")
if prompt := st.chat_input("Ask me anything..."):
    # Display the user's message instantly
    with st.chat_message("user"):
        st.markdown(prompt)
    # Save user message to persistent history state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 6. Query the backend Gemini model for a response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Using the exact full model path to resolve the 404 error
            model = genai.GenerativeModel("models/gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            # Extract and display the generated response
            full_response = response.text
            message_placeholder.markdown(full_response)
            
            # Save the assistant response to persistent history state
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            # Capture and render any API or platform errors clearly
            st.error(f"An error occurred: {e}")
