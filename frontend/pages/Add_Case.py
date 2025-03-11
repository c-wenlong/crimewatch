import streamlit as st
import requests
from datetime import datetime, time
import pytz

def create_case(case_data):
    """Send a POST request to create a new case"""
    response = requests.post("http://localhost:5000/cases/", json=case_data)
    return response

st.set_page_config(
    page_title="Add New Case", 
    page_icon="📝", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📝 Add New Case")
    st.write("Use the form below to add a new case.")

    with st.form("case_form"):
        # Input fields
        case_id = st.text_input("Case ID", placeholder="CRM-YYYY-001")
        title = st.text_input("Title", placeholder="Vandalism at City Hall")
        description = st.text_area("Description", placeholder="Graffiti and property damage reported at Stockholm City Hall.")
        type_of_crime = st.text_input("Type of Crime", placeholder="Vandalism")
        reported_location = st.text_input("Reported Location", placeholder="Stockholm City Hall")
        
        # Separate date and time inputs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            reported_date = st.date_input("Reported Date")
        with col2:
            reported_time_hour = st.number_input("Reported Hour", min_value=0, max_value=23, value=12)
        with col3:
            reported_time_minute = st.number_input("Reported Minute", min_value=0, max_value=59, value=0)
        with col4:
            reported_time_second = st.number_input("Reported Second", min_value=0, max_value=59, value=0)
        
        investigator_id = st.text_input("Investigator ID")
        status = st.selectbox("Status", ["Active", "Solved", "Archived"])
        
        st.write("### Additional Information")
        people_involved = st.text_area("People Involved (comma-separated)")
        evidence = st.text_area("Evidence (comma-separated)", placeholder="Graffiti paint cans, CCTV footage from City Hall")
        event_ids = st.text_area("Event IDs (comma-separated)")
        
        # Submit button
        submitted = st.form_submit_button("Add Case")

        # Process form submission
        if submitted:
            # Combine date and time into single datetime object
            reported_time = time(reported_time_hour, reported_time_minute, reported_time_second)
            reported_datetime = datetime.combine(reported_date, reported_time)

            # Convert the reported datetime to UTC (assume based in Stockholm)
            reported_datetime_local = pytz.timezone("Europe/Stockholm").localize(reported_datetime)
            reported_datetime_utc = reported_datetime_local.astimezone(pytz.utc)

            # Format the datetime
            formatted_datetime = reported_datetime_utc.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

            # Convert inputs to appropriate formats
            case_data = {
                "case_id": case_id,
                "title": title,
                "description": description,
                "type_of_crime": type_of_crime,
                "reported_location": reported_location,
                "reported_datetime": formatted_datetime, # formatted
                "investigator_id": investigator_id,
                "status": status,
                "people_involved": [x.strip() for x in people_involved.split(",")] if people_involved else [],
                "evidence": [x.strip() for x in evidence.split(",")] if evidence else [],
                "event_ids": [x.strip() for x in event_ids.split(",")] if event_ids else [],
            }

            # Insert data into MongoDB
            try:
                response = create_case(case_data)
                if response.status_code == 201:
                    st.success("Case added successfully!")                    
                else:
                    st.error(f"Failed to add case. Server returned: {response.status_code}")
            except Exception as e:
                st.error(f"Error while adding case: {e}")

# Run the app
if __name__ == "__main__":
    main()