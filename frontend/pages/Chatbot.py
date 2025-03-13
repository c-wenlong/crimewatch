import streamlit as st
from utils import get_database_connection
import json
from datetime import datetime
import requests
import dotenv
import os

dotenv.load_dotenv()
LOCALHOST_URI = os.getenv("LOCALHOST_URI")

st.set_page_config(
    page_title="Case Assistant | Case Management System",
    page_icon="🔍",
    layout="wide"
)

def get_all_cases():
    """Fetch all cases from the database"""
    response = requests.get(f"{LOCALHOST_URI}/cases/all")
    return response.json()

def get_selected_case(case_id):
    """Fetch all cases from the database"""
    try:
        response = requests.get(f"{LOCALHOST_URI}/cases/caseID/{case_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error loading case: {e}")
        return None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_case_context(case_id):
    """Get relevant information about a case to provide context for the chatbot"""
    
    try:
        case = get_selected_case(case_id)
        if not case:
            return f"No information found for case {case_id}."
        
        # Extract key information
        context = {
            "case_id": case["case_id"],
            "title": case["title"],
            "type": case["type_of_crime"],
            "status": case["status"],
            "description": case["description"],
            "date_opened": case["reported_datetime"],
            "location": case["reported_location"],
        }
        
        return context
    except Exception as e:
        return f"Error retrieving case information: {e}"

def generate_response(prompt, case_context):
    payload = {"user_prompt": prompt, "case_context": case_context}
    try:
        response = requests.post(f"{LOCALHOST_URI}/chatgpt/", json=payload)
        print(response)
        if response.ok:
            return response.json().get("results")
        else:
            return "Error: Unable to get a response from the chatbot."
    except Exception as e:
        return f"Exception occurred: {e}"


def save_chat_history(case_id, messages):
    """Save chat history to the database"""
    db = get_database_connection()
    if not db:
        return False
    
    try:
        # Create a chat log entry
        chat_log = {
            "case_id": case_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "messages": messages
        }
        
        # Save to chat_logs collection
        db.chat_logs.insert_one(chat_log)
        return True
    except Exception as e:
        st.error(f"Error saving chat history: {e}")
        return False

def show_chatbot():
    st.title("💬 Case Assistant Chatbot")
    
    # Get case_id from session state or select
    case_id = st.session_state.get("selected_case")
    
    # Allow manual case selection
    all_cases = []
    
    try:
        all_cases = get_all_cases()
    except Exception as e:
        st.error(f"Error loading cases: {e}")
    
    case_options = {case["case_id"]: f"{case['case_id']} - {case['title']}" for case in all_cases}
    
    selected_case_id = st.selectbox(
        "Select a case:", 
        options=list(case_options.keys()),
        format_func=lambda x: case_options.get(x, x),
        index=list(case_options.keys()).index(case_id) if case_id and case_id in case_options else 0
    )
    
    # Update session state
    st.session_state.selected_case = selected_case_id
    
    # Get case context
    case_context = get_case_context(selected_case_id)
    
    # If context is a string, there was an error
    if isinstance(case_context, str):
        st.error(case_context)
        return
        
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about this case..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message in chat message container
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate a response
        response = generate_response(prompt, case_context)
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Save chat history (in actual implementation)
        save_chat_history(selected_case_id, st.session_state.messages)
    
    # Add option to clear chat
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    show_chatbot()