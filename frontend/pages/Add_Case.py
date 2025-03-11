import streamlit as st
import requests
from datetime import datetime, time
import pytz
import dotenv
import os

dotenv.load_dotenv()
LOCALHOST_URI = os.getenv("LOCALHOST_URI")

def create_case(case_data):
    """Send a POST request to create a new case"""
    response = requests.post(f"{LOCALHOST_URI}/cases/", json=case_data)
    return response

def create_person(person_data):
    """Send a POST request to create a new person"""
    response = requests.post(f"{LOCALHOST_URI}/people/", json=person_data)
    return response

def get_all_people():
    """Fetch all people from the database"""
    response = requests.get(f"{LOCALHOST_URI}/people/all")
    return response.json()

def add_case():
    """Add a new case to the database"""
    st.header("Add New Case")
    st.write("Use the form below to add a new case.")

    # Fetch all Investigator for the Investigator ID dropdown
    people = get_all_people()
    investigator_options = {
        person["_id"]["$oid"]: f"{person['_id']['$oid']} - {person['name']}"
        for person in people
        if person.get("role_in_case") == "Investigator"  
    }

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
        
        investigator_id = st.selectbox(
            "Investigator ID",
            options=list(investigator_options.keys()),
            format_func=lambda x: investigator_options[x]
        )
        status = st.selectbox("Status", ["Active", "Solved", "Archived"])
        
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

            # Validation
            required_fields = {
                "Case ID": case_id,
                "Title": title,
                "Description": description,
                "Type of Crime": type_of_crime,
                "Reported Location": reported_location,
            }

            missing_fields = [field for field, value in required_fields.items() if not value]

            if missing_fields:
                for field in missing_fields:
                    st.error(f"{field} is required.")
                return

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
                "people_involved": [],
                "evidence": [],
                "event_ids": [],
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

def add_person():
    """Add a new person to the database"""
    st.header("Add New Person")
    st.write("Use the form below to add a new person.")

    with st.form("person_form"):
        # Input fields
        name = st.text_input("Name", placeholder="John Doe")
        age = st.number_input("Age", min_value=0, max_value=120, value=35)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        known_addresses = st.text_area("Known Addresses", placeholder="Stockholm, Sweden")
        role_in_case = st.text_input("Role in Case", placeholder="Witness", help="E.g., Witness, Suspect, Investigator, Victim, etc.")
        
        # Submit button
        submitted = st.form_submit_button("Add Person")

        # Process form submission
        if submitted:
            # Validation
            required_fields = {
                "Name": name,
                "Known Addresses": known_addresses,
                "Role in Case": role_in_case,
            }

            missing_fields = [field for field, value in required_fields.items() if not value]

            if missing_fields:
                for field in missing_fields:
                    st.error(f"{field} is required.")
                return

            # Convert inputs to appropriate formats
            person_data = {
                "name": name,
                "age": age,
                "gender": gender,
                "known_addresses": known_addresses,
                "role_in_case": role_in_case,
            }

            # Insert data into MongoDB
            try:
                response = create_person(person_data)
                if response.status_code == 201:
                    st.success("Person added successfully!")
                else:
                    st.error(f"Failed to add person. Server returned: {response.status_code}")
            except Exception as e:
                st.error(f"Error while adding person: {e}")

st.set_page_config(
    page_title="Add Case/People | Case Management System", 
    page_icon="📝", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📝 Case Management System")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Add New Case", "Add New Person"])

    if page == "Add New Case":
        add_case()
    elif page == "Add New Person":
        add_person()

# Run the app
if __name__ == "__main__":
    main()