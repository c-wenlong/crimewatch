import streamlit as st
import pandas as pd
from utils.db_connector import get_database_connection
import requests
import datetime
import dotenv
import os

dotenv.load_dotenv()
LOCALHOST_URI = os.getenv("LOCALHOST_URI")

st.set_page_config(
    page_title="Case Details | Case Management System",
    page_icon="🔍",
    layout="wide"
)

st.cache_data(ttl=120)
def get_all_cases():
    """Fetch all cases from the database"""
    response = requests.get(f"{LOCALHOST_URI}/cases/all")
    return response.json()

st.cache_data(ttl=40)
def get_selected_case(case_id):
    """Fetch all cases from the database"""
    try:
        response = requests.get(f"{LOCALHOST_URI}/cases/caseID/{case_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error loading case: {e}")
        return None
    
def update_case(id, data):
    """Update case details in the database"""
    response = requests.put(f"{LOCALHOST_URI}/cases/{id}", json=data)
    return response

def get_person(person_id):
    """Fetch person details from the database"""
    try:
        response = requests.get(f"{LOCALHOST_URI}/people/{person_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error loading person: {e}")
        return None

def get_evidence(evidence_id):
    """Fetch evidence details from the database"""
    try:
        response = requests.get(f"{LOCALHOST_URI}/evidence/{evidence_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error loading evidence: {e}")
        return None

def download_evidence(evidence_id):
    """Download evidence file from the database"""
    try:
        response = requests.get(f"{LOCALHOST_URI}/evidence/download/{evidence_id}")
        return response.content
    except Exception as e:
        st.error(f"Error downloading evidence: {e}")
        return None
    
def upload_evidence(uploaded_file, description):
    """Upload evidence file to the database"""
    try:
        if uploaded_file is None:
            st.error("No file selected")
            return None

        files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
        data = {"description": description}
        response = requests.post(f"{LOCALHOST_URI}/evidence/", files=files, data=data)

        if response.status_code == 201:
            return response.json()  # Successfully uploaded
        else:
            st.error(f"Error uploading evidence: {response.json().get('error', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Error uploading evidence: {e}")
        return None

def format_datetime(dt_str):
    dt_obj = datetime.datetime.strptime(dt_str, "%Y-%m-%dT%H:%M:%SZ")
    return dt_obj.strftime("%B %d, %Y at %I:%M %p")


def show_case_detail():
    st.title("📋 Case Details")
    
    # If coming from dashboard, case may be in session state
    case_id = st.session_state.get("selected_case")
    
    # Also offer manual case selection
    all_cases = []

    try:
        all_cases = get_all_cases()
    except Exception as e:
        st.error(f"Error loading cases: {e}")
    
    case_options = {case["case_id"]: f"{case['case_id']} - {case['title']}" for case in all_cases}
    
    selected_case_id = st.selectbox(
        "Select a case to view:", 
        options=list(case_options.keys()),
        format_func=lambda x: case_options.get(x, x),
        index=list(case_options.keys()).index(case_id) if case_id in case_options else 0
    )
    
    # Update session state
    st.session_state.selected_case = selected_case_id
    
    # Get case details
    case = get_selected_case(selected_case_id)
    
    if not case:
        st.warning("No case selected or case not found.")
        return
    
    # Layout: Basic Info & Status
    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.header(f"{case['title']}")  # Main title of the case
        st.write(f"**Case ID:** {case['case_id']}")

    # Use st.metric to visually represent status or other numeric info
    with col_b:
        st.metric(label="Status", value=case.get("status", "Unknown"))

    # Another row of columns for quick metrics
    col_c, col_d, col_e = st.columns(3)
    st.markdown(
        """
    <style>
    [data-testid="stMetricValue"] {
        font-size: 25px;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )
    with col_c:
        st.metric(label="Type of Crime", value=case.get("type_of_crime", "N/A"))
    with col_d:
        raw_dt_str = case.get("reported_datetime", "")
        if raw_dt_str:
            displayed_datetime = format_datetime(raw_dt_str)
            st.metric(label="Reported Time", value=displayed_datetime)
        else:
            st.metric(label="Reported Time", value="N/A")
    with col_e:
        loc_str = case.get("reported_location", "Unknown Location")
        st.metric(label="Location", value=loc_str)

    # Use tabs for better organization of sections
    tab_overview, tab_people, tab_evidence, tab_actions = st.tabs(
        ["Overview", "People Involved", "Evidence", "Actions"]
    )
    
    # 1) Overview Tab
    with tab_overview:
        st.subheader("Case Description")
        st.write(case.get("description", "No description provided."))

        with tab_people:
            st.subheader("People Involved")
            
            # Add quick filters for people
            role_filter = st.multiselect("Filter by Role:", ["Victim", "Witness", "Suspect", "Person of Interest", "All"], default=["All"])
            
            people_involved = case.get("people_involved", [])
            if people_involved:
                for person_id in people_involved:
                    person = get_person(person_id)
                    if not person:
                        continue
                    
                    # Role-based styling
                    role = person.get('role_in_case', 'Unknown')
                    role_color = {
                        "Victim": "#e6f7ff", 
                        "Witness": "#d4edda", 
                        "Suspect": "#f8d7da",
                        "Person of Interest": "#fff3cd"
                    }.get(role, "#f0f2f6")
                    
                    # Use an expander for each person
                    with st.expander(f"{person.get('name', 'Unknown')} - {role}"):
                        cols = st.columns([1, 1])
                        with cols[0]:
                            st.markdown(f"""
                            <div style="background-color: {role_color}; padding: 10px; border-radius: 5px;">
                                <h4>{person.get('name', 'Unknown')}</h4>
                                <p><strong>Role:</strong> {role}</p>
                                <p><strong>Age:</strong> {person.get('age', 'N/A')}</p>
                                <p><strong>Gender:</strong> {person.get('gender', 'N/A')}</p>
                                <p><strong>Contact:</strong> {person.get('contact', 'N/A')}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with cols[1]:
                            addresses = person.get("known_addresses", [])
                            if addresses:
                                st.markdown("**Known Addresses:**")
                                for addr in addresses:
                                    st.markdown(f"- {addr}")
                            
                            # Show criminal history if available and for suspect/POI
                            if person.get('criminal_history') and role in ["Suspect", "Person of Interest"]:
                                st.markdown("**Prior Offenses:**")
                                for offense in person.get('prior_offenses', ['None']):
                                    st.markdown(f"- {offense}")
                        
                        # Notes section
                        st.markdown("**Notes:**")
                        st.markdown(person.get('notes', 'No notes available.'))
                        
            else:
                st.info("No people linked to this case.")
            
    # 3) Evidence Tab
    with tab_evidence:
        st.subheader("Evidence")
        evidence_list = case.get("evidence", [])
        if evidence_list:
            for evidence_id in evidence_list:
                evidence = get_evidence(evidence_id['$oid'])
                if not evidence:
                    continue
                
                # Use an expander for each evidence item
                with st.expander(f"{evidence.get('filename', 'Unknown')}"):
                    
                    # Add download link if file is available
                    if evidence.get('file'):
                        st.markdown(f"📄 **File:** {evidence.get('filename')}")
                        file_content = download_evidence(evidence_id['$oid'])
                        if file_content:
                            st.download_button(
                                key=f"download_{evidence_id['$oid']}",
                                label=f"Download {evidence.get('filename')}",
                                data=file_content,
                                file_name=evidence.get('filename'),
                                mime='application/octet-stream'
                            )
                            if evidence.get('filename').endswith('.pdf'):
                                # Directly display PDF without requiring button click
                                st.markdown(f"### Viewing: {evidence.get('filename')}")
                                import base64
                                base64_pdf = base64.b64encode(file_content).decode('utf-8')
                                pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1200" height="1000" type="application/pdf"></iframe>'
                                st.markdown(pdf_display, unsafe_allow_html=True)
        else:
            st.info("No evidence available for this case.")

    # 4) Actions Tab
    with tab_actions:
        st.subheader("Case Actions")
        
        # Always show the file uploader
        uploaded_file = st.file_uploader("Upload Evidence File", type=["txt", "docx", "pdf"])
        evidence_list = case.get("evidence", [])
        if uploaded_file:
            description = st.text_input("Evidence Description")
            if st.button("Submit Evidence"):
                evidence_response = upload_evidence(uploaded_file, description)
                if evidence_response:
                    # Create new evidence ObjectId entry
                    new_evidence = {"$oid": evidence_response['evidence_id']}
                    # Append to the evidence list
                    evidence_list.append(new_evidence)
                    print(evidence_list)
                    # Update the case with the new evidence list
                    update_response = update_case(str(case["_id"]['$oid']), {"evidence": evidence_list})
                    if update_response.status_code == 200:
                        st.success("File uploaded and case updated successfully!")
                        # Refresh the page to show new evidence
                        st.rerun()
                    else:
                        st.error("Error updating case with new evidence.")
            # else:
            #     st.error("Error uploading evidence.")

    # You could also add an expander or additional tabs for "History", "Events", or "Notes".
    st.divider()
    st.caption("End of case details.")

if __name__ == "__main__":
    show_case_detail()