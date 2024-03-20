import streamlit as st
import requests
from PyPDF2 import PdfReader
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/google-bert/bert-large-uncased-whole-word-masking-finetuned-squad"
API_TOKEN = "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"  # Replace with your actual API token

headers = {"Authorization": f"Bearer {API_TOKEN}"}

def extract_text_from_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def query(payload, context):
    payload["inputs"]["context"] = context
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def load_chatbot(context):
    return lambda payload: query(payload, context)

def main():
    session_state = st.session_state
    if 'chat_history' not in session_state:
        session_state.chat_history = []
    if 'uploaded_file' not in session_state:
        session_state.uploaded_file = None
    
    # Display image
    image = Image.open("AI-chatbot.jpg")
    st.image(image, use_column_width=True)
    
    st.title("ChatWithDoc")
    st.write("Hopefully we can use this to generate answers for my periodic tests.")
    
    # Upload file
    session_state.uploaded_file = st.file_uploader("Upload Data File", type=['txt', 'csv', 'png', 'jpg', 'pdf'])
    
    # Check if a file is uploaded
    if session_state.uploaded_file is not None:
        # Check file type
        if session_state.uploaded_file.type == 'application/pdf':
            # Extract text from PDF
            context = extract_text_from_pdf(session_state.uploaded_file)
        else:
            # Read file content
            context = session_state.uploaded_file.getvalue().decode("utf-8")
        
        # Load the chatbot
        chatbot = load_chatbot(context)
        
        # Chat interface
        user_input = st.text_input("You:", "")
        
        # Check if user inputs something
        if user_input:
            # Get chatbot response
            bot_response = chatbot({
                "inputs": {
                    "question": user_input,
                    "context": context
                }
            })
            
            # Add user input and bot response to chat history
            session_state.chat_history.append((user_input, bot_response))
    
    # Display chat history
    for user_input, bot_response in session_state.chat_history:
        st.markdown("### You:")
        st.write(user_input)
        st.markdown("### Chatbot's Response:")
        st.write(bot_response["answer"])
        st.markdown("---")
    
    # Add footer
    st.write("Developed with ❤️ by anu.")
    
if __name__ == "__main__":
    main()
