import streamlit as st
import requests
import os

API_URL = "http://localhost:8000"


st.set_page_config(page_title="NVIDIA NIM RAG Chat", page_icon="🤖")

st.title("🤖 NVIDIA NIM Based RAG System")
st.markdown("Ask questions about your documents using NVIDIA NIM")

# Sidebar for document upload
with st.sidebar:
    st.header("🗎 Document Management")

    # File path input
    file_path = st.text_input(
        "Document Path",
        value="data/sample_doc.txt",
        help="Path to your text document"
    )

    if st.button("Load Document"):
        with st.spinner("Loading document..."):
            try:
                response = requests.post(
                    f"{API_URL}/upload",
                    json={"file_path": file_path}
                )
                if response.status_code == 200:
                    st.success(response.json()["message"])
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to API: {str(e)}")


# Main chat interface
st.header("💬 Chat")

# Initialize chat history
if "message" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user messages to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(
                    f"{API_URL}/query",
                    json={"question": prompt}
                )
                if response.status_code == 200:
                    answer = response.json()["answeer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error: {response.txt}"
                    st.error(error_msg)
            except Exception as e:
                error_msg = f"Failed to eonnct to API: {str(e)}"
                st.error(error_msg)