import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from datetime import datetime
from utils.db_connector import get_database_connection
import dotenv
import os

dotenv.load_dotenv()
LOCALHOST_URI = os.getenv("LOCALHOST_URI")

st.set_page_config(
    page_title="Timeline View | Case Management System",
    page_icon="🔍",
    layout="wide"
)

st.cache_data(ttl=120)
def get_all_cases():
    """Fetch all cases from the database"""
    response = requests.get(f"{LOCALHOST_URI}/cases/all")
    return response.json()

@st.cache_data(ttl=120)
def get_selected_case_events(case_id):
    """Fetch all cases from the database"""
    try:
        response = requests.get(f"{LOCALHOST_URI}/cases/caseID/{case_id}")
        return response.json().get("event_ids", [])
    except Exception as e:
        st.error(f"Error loading case: {e}")
        return None

def get_event(event_id):
    """Fetch event details from the database"""
    try:
        response = requests.get(f"{LOCALHOST_URI}/events/{event_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error loading event: {e}")
        return None

def load_case_events(case_id):
    """Load all events for a specific case by querying the backend for each event_id"""
    
    try:    
        event_ids = get_selected_case_events(case_id)
        events = []
        for event_id in event_ids:
            event_data = get_event(event_id)
            if event_data:
                events.append(event_data)
            else:
                st.warning(f"Event {event_id} not found.")
                
        # Sort events by the 'occurred_at' field (ISO format: "YYYY-MM-DDTHH:MM:SSZ")
        events.sort(key=lambda x: datetime.strptime(x["occurred_at"], "%Y-%m-%dT%H:%M:%SZ"))
        return events
    except Exception as e:
        st.error(f"Error loading case events: {e}")
        return []

@st.cache_data(ttl=120)
def load_people():
    """Load all people from the backend"""
    try:
        url = f"{LOCALHOST_URI}/people/all"
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp.json()
        else:
            st.warning("Failed to load people.")
            return []
    except Exception as e:
        st.error(f"Error loading people: {e}")
        return []

def show_timeline():
    st.title("📅 Case Timeline View")
    
    # Get case_id from session state or select
    case_id = st.session_state.get("selected_case")
    
    # Allow manual case selection
    all_cases = []

    try:
        all_cases = get_all_cases()
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
            event_time = st.time_input("Event time")
            event_type = st.selectbox("Event Type", ["Interview", "Evidence Collection", "Arrest", "Witness Statement", "Other"])
            event_description = st.text_area("Event Description")
            event_location = st.text_input("Event Location")
            people = load_people()
            person_options = {person["_id"]["$oid"]: f"{person['name']}" for person in people}
            person_id = st.selectbox("Person ID", options=list(person_options.keys()) + [None], format_func=lambda x: person_options.get(x, x))
            reported_by = st.text_input("Reported By")

            if st.button("Add Event"):
                occurred_at = datetime.combine(event_date, event_time).strftime("%Y-%m-%dT%H:%M:%SZ")
                new_event = {
                    "case_id": selected_case_id,
                    "description": event_description,
                    "event_type": event_type,
                    "occurred_at": occurred_at,
                    "location": event_location,
                    "person_id": person_id,
                    "reported_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "reported_by": reported_by
                }
                response = requests.post(f"{LOCALHOST_URI}/events/", json=new_event)
                if response.status_code == 201:
                    new_event_data = response.json()
                    new_event_id = new_event_data.get("event_id")
                    if not new_event_id:
                        st.error("Event created but no event_id was returned!")
                    else:
                        case_id = requests.get(f"{LOCALHOST_URI}/cases/caseID/{selected_case_id}").json().get("_id")['$oid']
                        update_case_url = f"{LOCALHOST_URI}/cases/{case_id}"
                        update_payload = {
                            "$push": { "event_ids": new_event_id }
                        }
                        print(update_case_url, update_payload)
                        update_response = requests.put(update_case_url, json=update_payload)
                        if update_response.status_code == 200:
                            st.success("Event added and case updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"Event added but failed to update case: {update_response.text}")
                else:
                    st.error("Failed to add event.")
        return
    
    # Convert to DataFrame for visualization.
    # We'll use the 'datetime' field for the timeline and rename 'title' to 'event'
    df_events = pd.DataFrame(events)

    # Convert the 'occurred_at' column from ISO string to datetime
    df_events["occurred_at"] = pd.to_datetime(df_events["occurred_at"])

    df_events["reported_at"] = pd.to_datetime(df_events["reported_at"])

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

    # Load people data for name mapping
    people_data = load_people()
    people_dict = {person["_id"]["$oid"]: person["name"] for person in people_data}

    # Format datetime and replace person_id with name
    df_events["occurred_at"] = df_events["occurred_at"].dt.strftime("%d-%b-%y %H:%M")
    df_events["reported_at"] = df_events["reported_at"].dt.strftime("%d-%b-%y %H:%M")
    df_events["person_name"] = df_events["person_id"].map(people_dict)

    # Drop unnecessary columns
    df_events_display = df_events.drop(columns=["_id", "case_id", "event_start", "event_end", "person_id"], errors="ignore")

    df_events_display = df_events_display.loc[:, ['event_type', 'person_name', 'description', 'location', 'occurred_at', 'reported_at', 'reported_by']]

    # Display updated dataframe
    st.dataframe(df_events_display, use_container_width=True)

    internal_case_id = df_events["case_id"].iloc[0]

    with st.expander("Add New Event"):
        event_date = st.date_input("Event Date")
        event_time = st.time_input("Event time")
        st.write("Occurrence event time is set for", event_time)
        # event_time = st.time_input("Event Time", value=None)
        event_type = st.selectbox("Event Type", ["Interview", "Evidence Collection", "Arrest", "Witness Statement", "Other"])
        event_description = st.text_area("Event Description")
        event_location = st.text_input("Event Location")
        people = load_people()
        person_options = {person["_id"]["$oid"]: f"{person['name']}" for person in people}
        person_id = st.selectbox("Person ID", options=list(person_options.keys()) + ["None"], format_func=lambda x: person_options.get(x, x))
        # person_id = st.text_input("Person ID")
        reported_by = st.text_input("Reported By")
        if st.button("Add Event"):
            occurred_at = datetime.combine(event_date, event_time).strftime("%Y-%m-%dT%H:%M:%SZ")
            new_event = {
                "case_id": internal_case_id,
                "description": event_description,
                "event_type": event_type,
                "occurred_at": occurred_at,
                "location": event_location,
                "person_id": person_id,
                "reported_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                "reported_by": reported_by
            }
            response = requests.post(f"{LOCALHOST_URI}/events/", json=new_event)
            if response.status_code == 201:
                # Get the newly created event's _id
                new_event_data = response.json()
                new_event_id = new_event_data.get("event_id")
                
                if not new_event_id:
                    st.error("Event created but no event_id was returned!")
                else:
                    # Send an update request to add the event id to the case's event_ids array.
                    # Here we remove the extra "update" key and send the "$push" operator directly.
                    case_id = requests.get(f"{LOCALHOST_URI}/cases/caseID/{internal_case_id}").json().get("_id")['$oid']
                    update_case_url = f"{LOCALHOST_URI}/cases/{case_id}"
                    update_payload = {
                        "$push": { "event_ids": new_event_id }
                    }
                    update_response = requests.put(update_case_url, json=update_payload)
                    print("Update case response code:", update_response.status_code)
                    print("Update case response text:", update_response.text)
                    
                    if update_response.status_code == 200:
                        st.success("Event added and case updated successfully!")
                        st.rerun()
                    else:
                        st.error(f"Event added but failed to update case: {update_response.text}")
            else:
                st.error("Failed to add event.")


if __name__ == "__main__":
    show_timeline()