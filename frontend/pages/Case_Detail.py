import streamlit as st
import pandas as pd
from utils.db_connector import get_database_connection
import requests

st.set_page_config(
    page_title="Case Details | Case Management System",
    page_icon="🔍",
    layout="wide"
)

def get_all_cases():
    """Fetch all cases from the database"""
    response = requests.get("http://localhost:5000/cases/all")
    return response.json()

def get_selected_case(case_id):
    """Fetch all cases from the database"""
    try:
        response = requests.get(f"http://localhost:5000/cases/caseID/{case_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error loading case: {e}")
        return None

def get_person(person_id):
    """Fetch person details from the database"""
    try:
        response = requests.get(f"http://localhost:5000/people/{person_id}")
        return response.json()
    except Exception as e:
        st.error(f"Error loading person: {e}")
        return None

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
    
    # Display case information
    st.header(case['title'])
    
    # Create columns for basic info
    st.info(f"**Status:** {case['status']}")
    col1, col2 = st.columns(2)
    with col1:
        # st.info(f"**Status:** {case['status']}")
        st.write(f"**Case ID:** {case['case_id']}")
        st.write(f"**Reported Date:** {case['reported_datetime']}")
    
    with col2:
        st.write(f"**Type:** {case['type_of_crime']}")
        st.write(f"**Reported Location:** {case['reported_location']}")
    
    # Display description
    st.subheader("Case Description")
    st.write(case['description'])
    
    # Display evidence if available
    if "evidence" in case and case["evidence"]:
        st.subheader("Evidence")
        evidence_df = pd.DataFrame(case["evidence"])
        st.dataframe(evidence_df)
    
    # Display suspects if available
    if "people_involved" in case and case["people_involved"]:
        st.subheader("People Involved")
        for i, person_id in enumerate(case["people_involved"]):
            person = get_person(person_id)
            with st.expander(f"Person {i+1}: {person.get('name', 'Unknown')} ({person.get('role_in_case', 'Role Unknown')})"):
                for key, value in person.items():
                    if key != "name" and key != "_id":
                        st.write(f"**{key.replace('_', ' ').title()}:** {value}")
    
    # Add case actions
    st.subheader("Case Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Update Case"):
            st.write("Update functionality to be implemented")
    with col2:
        if st.button("Add Evidence"):
            st.write("Add evidence functionality to be implemented")
    with col3:
        if st.button("Generate Report"):
            st.write("Report generation to be implemented")

if __name__ == "__main__":
    show_case_detail()