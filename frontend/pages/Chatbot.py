import streamlit as st
from utils.db_connector import get_database_connection
import json
from datetime import datetime

st.set_page_config(
    page_title="Case Assistant | Case Management System",
    page_icon="🔍",
    layout="wide"
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def get_case_context(case_id):
    """Get relevant information about a case to provide context for the chatbot"""
    db = get_database_connection()
    if not db:
        return "Database connection failed."
    
    try:
        case = db.test_case.find_one({"case_id": case_id})
        if not case:
            return f"No information found for case {case_id}."
        
        # Extract key information
        context = {
            "case_id": case["case_id"],
            "title": case["title"],
            "type": case["type"],
            "status": case["status"],
            "description": case["description"],
            "date_opened": case["date_opened"],
            "location": case["location"],
            "lead_detective": case["lead_detective"]
        }
        
        return context
    except Exception as e:
        return f"Error retrieving case information: {e}"

def generate_response(prompt, case_context):
    """
    This is a placeholder for an actual AI response generator
    In a real implementation, you would connect to an LLM API
    """
    
    # Simple keyword-based response for demonstration
    if "status" in prompt.lower():
        return f"The current status of case {case_context['case_id']} is '{case_context['status']}'."
    
    elif "location" in prompt.lower():
        return f"This case occurred in {case_context['location']}."
    
    elif "detective" in prompt.lower() or "lead" in prompt.lower():
        return f"The lead detective for this case is {case_context['lead_detective']}."
    
    elif "description" in prompt.lower() or "about" in prompt.lower() or "summary" in prompt.lower():
        return f"Case summary: {case_context['description']}"
    
    else:
        return (
            f"I'm the Case Assistant for case {case_context['case_id']} - {case_context['title']}. "
            f"This is a {case_context['type']} case opened on {case_context['date_opened']}. "
            f"You can ask me about case status, location, lead detective, or for a summary."
        )

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
    db = get_database_connection()
    if db:
        try:
            all_cases = list(db.test_case.find({}, {"case_id": 1, "title": 1}))
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