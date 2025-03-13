import streamlit as st
import requests
from datetime import datetime, time
import pytz
import dotenv
import os
import json

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

def add_case_with_people():
    """Add a new case with required people to the database"""
    st.header("Add New Case")
    st.write("Use the form below to add a new case with related people.")

    # Fetch all Investigators for the dropdown
    people = get_all_people()
    investigator_options = {
        person["_id"]["$oid"]: f"{person['_id']['$oid']} - {person['name']}"
        for person in people
        if person.get("role_in_case") == "Investigator"  
    }
    
    # Initialize session state for people if it doesn't exist
    if 'people_to_add' not in st.session_state:
        st.session_state.people_to_add = []
    
    # Case form
    st.subheader("Case Details")
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
    
    # People section
    st.markdown("---")
    st.subheader("People Involved (Required)")
    st.info("At least one person must be added to create a case.")
    
    # Display people that will be added with the case
    if st.session_state.people_to_add:
        st.write("People to be added with this case:")
        for idx, person in enumerate(st.session_state.people_to_add):
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"{idx+1}. {person['name']} - {person['role_in_case']}")
            with col3:
                if st.button(f"Remove", key=f"remove_{idx}"):
                    st.session_state.people_to_add.pop(idx)
                    st.rerun()
    
    # Section to add a new person
    st.subheader("Add New Person")
    
    # Create columns for person input fields
    col1, col2 = st.columns(2)
    
    with col1:
        new_person_name = st.text_input("Name", key="new_name", placeholder="John Doe")
        new_person_age = st.number_input("Age", key="new_age", min_value=0, max_value=120, value=35)
        new_person_gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="new_gender")
    
    with col2:
        new_person_addresses = st.text_input("Known Addresses", key="new_addresses", placeholder="Stockholm, Sweden")
        new_person_role = st.selectbox("Role in Case", ["Witness", "Suspect", "Victim", "Investigator", "Other"], key="new_role")
    
    if st.button("Add Person to Case"):
        if new_person_name and new_person_addresses and new_person_role:
            # Add person to session state
            st.session_state.people_to_add.append({
                "name": new_person_name,
                "age": new_person_age,
                "gender": new_person_gender,
                "known_addresses": new_person_addresses,
                "role_in_case": new_person_role,
                "temp_id": len(st.session_state.people_to_add)  # Assign a temporary ID
            })
            st.success(f"Added {new_person_name} as {new_person_role} to the case.")
            st.rerun()  # Refresh to show updated list
        else:
            st.error("Name, Known Addresses, and Role in Case are required.")
    
    # Submit case button (outside of forms)
    st.markdown("---")
    if st.button("Submit Case", disabled=len(st.session_state.people_to_add) == 0):
        # Validation for case
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
            
        # Combine date and time into single datetime object
        reported_time = time(reported_time_hour, reported_time_minute, reported_time_second)
        reported_datetime = datetime.combine(reported_date, reported_time)

        # Convert the reported datetime to UTC (assume based in Stockholm)
        reported_datetime_local = pytz.timezone("Europe/Stockholm").localize(reported_datetime)
        reported_datetime_utc = reported_datetime_local.astimezone(pytz.utc)

        # Format the datetime
        formatted_datetime = reported_datetime_utc.strftime("%Y-%m-%dT%H:%M:%S") + "Z"

        # First create all the people
        people_involved_ids = []
        
        with st.spinner("Creating people records..."):
            for person_data in st.session_state.people_to_add:
                # Remove the temporary ID before sending
                person_to_create = {k: v for k, v in person_data.items() if k != 'temp_id'}

                try:
                    response = create_person(person_to_create)
                    if response.status_code == 201:
                        print("Response text:", response.text)
                        # Extract the created person's ID
                        person_id = json.loads(response.text).get("person_id", {})
                        if person_id:
                            people_involved_ids.append(person_id)
                            st.success(f"Created person: {person_data['name']}")
                        else:
                            st.warning(f"Created {person_data['name']} but couldn't get ID. Check database.")
                    else:
                        st.error(f"Failed to add person {person_data['name']}. Server returned: {response.status_code}")
                except Exception as e:
                    st.error(f"Error while adding person {person_data['name']}: {e}")

        # Now create the case with the people IDs
        case_data = {
            "case_id": case_id,
            "title": title,
            "description": description,
            "type_of_crime": type_of_crime,
            "reported_location": reported_location,
            "reported_datetime": formatted_datetime,
            "investigator_id": investigator_id,
            "status": status,
            "people_involved": people_involved_ids,
            "evidence": [],
            "event_ids": [],
        }

        with st.spinner("Creating case..."):
            try:
                response = create_case(case_data)
                if response.status_code == 201:
                    st.success(f"Case {case_id} added successfully with {len(people_involved_ids)} people!")
                    # Clear the people list after successful submission
                    st.session_state.people_to_add = []
                    # Clear form fields by rerunning
                    st.rerun()
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
    page_title="Case Management System", 
    page_icon="📝", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("📝 Case Management System")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Add New Case", "Add New Person"])

    if page == "Add New Case":
        add_case_with_people()
    elif page == "Add New Person":
        add_person()

# Run the app
if __name__ == "__main__":
    main()