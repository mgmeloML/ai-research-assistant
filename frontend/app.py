import streamlit as st
import requests
from datetime import datetime
import time

# API Configuration
API_BASE_URL = "http://backend_service:8000"  # Adjust this to your FastAPI server URL

# Page configuration
st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Initialize session state
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'chats_list' not in st.session_state:
    st.session_state.chats_list = []
if 'rag_mode' not in st.session_state:
    st.session_state.rag_mode = "web"
if 'chat_rag_modes' not in st.session_state:
    st.session_state.chat_rag_modes = {}  # Store RAG mode for each chat

# API Functions
def create_new_chat():
    """Create a new chat session"""
    try:
        response = requests.post(f"{API_BASE_URL}/create_chat")
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        st.error(f"Error creating chat: {str(e)}")
        return False

def get_all_chats():
    """Fetch all chats from the backend"""
    try:
        response = requests.get(f"{API_BASE_URL}/get_chats")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching chats: {str(e)}")
        return []

def get_chat_history(chat_id):
    """Fetch chat history for a specific chat"""
    try:
        response = requests.get(f"{API_BASE_URL}/get_chat/{chat_id}")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Error fetching chat history: {str(e)}")
        return []

def delete_chat(chat_id):
    """Delete a chat"""
    try:
        response = requests.delete(f"{API_BASE_URL}/delete_chat/{chat_id}")
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        st.error(f"Error deleting chat: {str(e)}")
        return False

def send_message(chat_id, query, rag_mode):
    """Send a message and get response"""
    try:
        endpoint = f"{API_BASE_URL}/{rag_mode}_rag/{chat_id}"
        params = {"query": query}
        response = requests.post(endpoint, params=params)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        return False

# Sidebar - Chat Management
with st.sidebar:
    st.title("RAG Chatbot")
    
    # RAG Mode Selection - disabled if current chat has messages
    st.subheader("RAG Mode")
    
    # Check if current chat has messages
    chat_has_messages = False
    if st.session_state.current_chat_id and st.session_state.chat_history:
        chat_has_messages = True
    
    # If current chat has messages, show its locked mode
    if chat_has_messages and st.session_state.current_chat_id in st.session_state.chat_rag_modes:
        locked_mode = st.session_state.chat_rag_modes[st.session_state.current_chat_id]
        st.info(f"🔒 This chat is locked to **{locked_mode.upper()}** mode")
        st.session_state.rag_mode = locked_mode
    else:
        # Allow selection for new chats or chats without messages
        rag_mode = st.radio(
            "Select data source:",
            ["web", "pdf"],
            index=0 if st.session_state.rag_mode == "web" else 1,
            help="Web: Search and scrape web pages\nPDF: Search and use PDF documents\n\n⚠️ Mode locks after first message"
        )
        st.session_state.rag_mode = rag_mode
    
    st.divider()
    
    # New Chat Button
    if st.button("➕ New Chat", use_container_width=True):
        if create_new_chat():
            st.success("New chat created!")
            st.session_state.chats_list = get_all_chats()
            time.sleep(0.5)
            st.rerun()
    
    st.divider()
    
    # Display Chats List
    st.subheader("Your Chats")
    
    if not st.session_state.chats_list:
        st.session_state.chats_list = get_all_chats()
    
    if st.session_state.chats_list:
        for chat in st.session_state.chats_list:
            chat_id = chat.get('chat_id')
            chat_name = chat.get('chat_name', 'New Chat')
            modified_at = chat.get('modified_at', '')
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                if st.button(
                    f"💬 {chat_name[:30]}...",
                    key=f"chat_{chat_id}",
                    use_container_width=True,
                    type="primary" if st.session_state.current_chat_id == chat_id else "secondary"
                ):
                    st.session_state.current_chat_id = chat_id
                    st.session_state.chat_history = get_chat_history(chat_id)
                    # Load the RAG mode for this chat if it exists
                    if chat_id in st.session_state.chat_rag_modes:
                        st.session_state.rag_mode = st.session_state.chat_rag_modes[chat_id]
                    st.rerun()
            
            with col2:
                if st.button("🗑️", key=f"delete_{chat_id}"):
                    if delete_chat(chat_id):
                        if st.session_state.current_chat_id == chat_id:
                            st.session_state.current_chat_id = None
                            st.session_state.chat_history = []
                        st.session_state.chats_list = get_all_chats()
                        time.sleep(0.5)
                        st.rerun()
    else:
        st.info("No chats yet. Create a new chat to get started!")

# Main Chat Interface
st.title("💬 Chat Interface")

if st.session_state.current_chat_id:
    # Display current chat name
    current_chat = next(
        (chat for chat in st.session_state.chats_list 
         if chat.get('chat_id') == st.session_state.current_chat_id),
        None
    )
    if current_chat:
        st.caption(f"Chat: {current_chat.get('chat_name', 'New Chat')} | Mode: {st.session_state.rag_mode.upper()}")
    
    # Chat History Display
    chat_container = st.container()
    with chat_container:
        if st.session_state.chat_history:
            for message in st.session_state.chat_history:
                role = message.get('role', 'user')
                content = message.get('content', '')
                
                if role == 'user':
                    with st.chat_message("user"):
                        st.write(content)
                else:
                    with st.chat_message("assistant"):
                        st.write(content)
        else:
            st.info("Start a conversation by typing a message below!")
    
    # Message Input
    st.divider()
    
    with st.form(key="message_form", clear_on_submit=True):
        user_input = st.text_area(
            "Your message:",
            placeholder=f"Ask a question... (using {st.session_state.rag_mode.upper()} RAG)",
            height=100,
            key="user_input"
        )
        submit_button = st.form_submit_button("Send 📤", use_container_width=True)
        
        if submit_button and user_input.strip():
            with st.spinner(f"Processing your request using {st.session_state.rag_mode.upper()} RAG..."):
                # Lock the RAG mode for this chat on first message
                if st.session_state.current_chat_id not in st.session_state.chat_rag_modes:
                    st.session_state.chat_rag_modes[st.session_state.current_chat_id] = st.session_state.rag_mode
                
                if send_message(st.session_state.current_chat_id, user_input, st.session_state.rag_mode):
                    # Refresh chat history after sending message
                    st.session_state.chat_history = get_chat_history(st.session_state.current_chat_id)
                    st.session_state.chats_list = get_all_chats()
                    st.rerun()
                else:
                    st.error("Failed to send message. Please try again.")
else:
    # No chat selected
    st.info("👈 Select a chat from the sidebar or create a new one to get started!")
    
    # Display welcome message
    st.markdown("""
    ## Welcome to RAG Chatbot! 🚀
    
    This chatbot uses Retrieval-Augmented Generation (RAG) to provide intelligent responses based on:
    
    - **Web RAG**: Searches and scrapes relevant web pages to answer your questions
    - **PDF RAG**: Searches and uses PDF documents to provide answers
    
    ### How to use:
    1. Select your preferred RAG mode (Web or PDF) in the sidebar
    2. Click "➕ New Chat" to create a new conversation
    3. Start asking questions!
    
    The chatbot will automatically:
    - Collect relevant data based on your query
    - Generate meaningful responses
    - Maintain conversation history
    - Create appropriate chat names
    """)
