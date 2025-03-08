import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from utils.db_connector import get_database_connection

st.set_page_config(
    page_title="Timeline View | Case Management System",
    page_icon="🔍",
    layout="wide"
)

def load_case_events(case_id):
    """Load all events for a specific case"""
    db = get_database_connection()
    if not db:
        return None
    
    try:
        case = db.test_case.find_one({"case_id": case_id})
        if not case or "events" not in case:
            return []
        
        # Sort events by date
        events = case["events"]
        events.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d"))
        return events
    except Exception as e:
        st.error(f"Error loading case events: {e}")
        return []

def show_timeline():
    st.title("📅 Case Timeline View")
    
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
        "Select a case to view timeline:", 
        options=list(case_options.keys()),
        format_func=lambda x: case_options.get(x, x),
        index=list(case_options.keys()).index(case_id) if case_id and case_id in case_options else 0
    )
    
    # Update session state
    st.session_state.selected_case = selected_case_id
    
    # Load case events
    events = load_case_events(selected_case_id)
    
    if not events:
        st.info("No timeline events found for this case.")
        
        # Option to add events
        with st.expander("Add New Event"):
            event_date = st.date_input("Event Date")
            event_type = st.selectbox("Event Type", ["Interview", "Evidence Collection", "Arrest", "Witness Statement", "Other"])
            event_description = st.text_area("Event Description")
            if st.button("Add Event"):
                st.info("Event addition functionality to be implemented")
        return
    
    # Convert to DataFrame for visualization
    df_events = pd.DataFrame(events)
    
    # Create interactive timeline
    fig = px.timeline(
        df_events, 
        x_start="date", 
        y="type",
        color="type",
        hover_data=["description"],
        labels={"date": "Date", "type": "Event Type"},
        title=f"Timeline for Case {selected_case_id}"
    )
    
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)
    
    # Display events in a table
    st.subheader("Case Events")
    st.dataframe(df_events, use_container_width=True)
    
    # Add new event
    with st.expander("Add New Event"):
        event_date = st.date_input("Event Date")
        event_type = st.selectbox("Event Type", ["Interview", "Evidence Collection", "Arrest", "Witness Statement", "Other"])
        event_description = st.text_area("Event Description")
        if st.button("Add Event"):
            st.info("Event addition functionality to be implemented")

if __name__ == "__main__":
    show_timeline()