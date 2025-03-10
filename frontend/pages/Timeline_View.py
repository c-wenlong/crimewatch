import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
from utils.db_connector import get_database_connection

st.set_page_config(
    page_title="Timeline View | Case Management System",
    page_icon="🔍",
    layout="wide"
)

def load_case_events(case_id):
    """Load all events for a specific case by querying the backend for each event_id"""
    db = get_database_connection()
    if not db:
        return None
    
    try:
        case = db.cases.find_one({"case_id": case_id})
        if not case or "event_ids" not in case:
            return []
        
        event_ids = case["event_ids"]
        events = []
        for event_id in event_ids:
            url = f"http://127.0.0.1:5000/events/{event_id}"
            resp = requests.get(url)
            if resp.status_code == 200:
                # Assuming the returned event follows the API docs: it contains fields like 'title', 'description', 'datetime', etc.
                event_data = resp.json()
                events.append(event_data)
            else:
                st.warning(f"Event {event_id} not found.")
                
        # Sort events by the 'occurred_at' field (ISO format: "YYYY-MM-DDTHH:MM:SSZ")
        events.sort(key=lambda x: datetime.strptime(x["occurred_at"], "%Y-%m-%dT%H:%M:%SZ"))
        return events
    except Exception as e:
        st.error(f"Error loading case events: {e}")
        return []

def show_timeline():
    st.title("📅 Case Timeline View")
    
    # Get case_id from session state or select
    case_id = st.session_state.get("selected_case")
    
    # Allow manual case selection
    db = get_database_connection()
    all_cases = []
    if db:
        try:
            all_cases = list(db.test_case.find({}, {"case_id": 1, "title": 1}))
        except Exception as e:
            st.error(f"Error loading cases: {e}")
    
    if not all_cases:
        st.error("No cases available.")
        return
    
    case_options = {case["case_id"]: f"{case['case_id']} - {case['title']}" for case in all_cases}
    
    # Set default index
    keys_list = list(case_options.keys())
    default_index = keys_list.index(case_id) if case_id in keys_list else 0
    
    selected_case_id = st.selectbox(
        "Select a case to view timeline:", 
        options=keys_list,
        format_func=lambda x: case_options.get(x, x),
        index=default_index
    )
    
    # Update session state
    st.session_state.selected_case = selected_case_id
    
    # Load case events by querying the events endpoint for each event id
    events = load_case_events(selected_case_id)
    
    if not events:
        st.info("No timeline events found for this case.")
        with st.expander("Add New Event"):
            event_date = st.date_input("Event Date")
            event_type = st.selectbox("Event Type", ["Interview", "Evidence Collection", "Arrest", "Witness Statement", "Other"])
            event_description = st.text_area("Event Description")
            if st.button("Add Event"):
                st.info("Event addition functionality to be implemented")
        return
    
    # Convert to DataFrame for visualization.
    # We'll use the 'datetime' field for the timeline and rename 'title' to 'event'
    df_events = pd.DataFrame(events)

    # Convert the 'occurred_at' column from ISO string to datetime
    df_events["occurred_at"] = pd.to_datetime(df_events["occurred_at"], format="%Y-%m-%dT%H:%M:%SZ")

    # Create a new column 'x_end' that is the same for all events—the last occurred_at time
    max_occurred_at = df_events["occurred_at"].max()

    # Create a new column 'x_start'
    min_occurred_at = df_events["occurred_at"].min()

    # Create a small duration for each event (e.g., 1 minute) so that each event has a visible length.
    df_events["event_start"] = df_events["occurred_at"]
    df_events["event_end"] = df_events["occurred_at"] + pd.Timedelta(minutes=1)

    # Create an interactive timeline where each event is represented as a bar of 1 minute duration.
    fig = px.timeline(
        df_events, 
        x_start="event_start", 
        x_end="event_end", 
        hover_data=["description"],
        labels={"event_start": "Date", "event_type": "Event Type"},
        title=f"Timeline for Case {selected_case_id}",
        y="event_type",
        color="event_type"
    )

    # Optionally, update the x-axis range to span from the earliest to the latest event.
    fig.update_layout(yaxis_range=[min_occurred_at, max_occurred_at], width=10)
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