import streamlit as st
import pandas as pd
from utils.db_connector import get_database_connection

st.set_page_config(
    page_title="Case Details | Case Management System",
    page_icon="🔍",
    layout="wide"
)

def get_case_details(case_id):
    """Fetch case details from the database"""
    db = get_database_connection()
    if not db:
        st.error("Database connection failed")
        return None
    
    try:
        case = db.test_case.find_one({"case_id": case_id})
        return case
    except Exception as e:
        st.error(f"Error retrieving case details: {e}")
        return None

def show_case_detail():
    st.title("📋 Case Details")
    
    # If coming from dashboard, case may be in session state
    case_id = st.session_state.get("selected_case")
    
    # Also offer manual case selection
    all_cases = []
    db = get_database_connection()
    if db:
        try:
            all_cases = list(db.test_case.find({}, {"case_id": 1, "title": 1}))
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
    case = get_case_details(selected_case_id)
    
    if not case:
        st.warning("No case selected or case not found.")
        return
    
    # Display case information
    st.header(case['title'])
    
    # Create columns for basic info
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**Status:** {case['status']}")
        st.write(f"**Case ID:** {case['case_id']}")
        st.write(f"**Date Opened:** {case['date_opened']}")
        st.write(f"**Lead Detective:** {case['lead_detective']}")
    
    with col2:
        st.write(f"**Type:** {case['type']}")
        st.write(f"**Location:** {case['location']}")
        if "date_closed" in case and case["date_closed"]:
            st.write(f"**Date Closed:** {case['date_closed']}")
    
    # Display description
    st.subheader("Case Description")
    st.write(case['description'])
    
    # Display evidence if available
    if "evidence" in case and case["evidence"]:
        st.subheader("Evidence")
        evidence_df = pd.DataFrame(case["evidence"])
        st.dataframe(evidence_df)
    
    # Display suspects if available
    if "suspects" in case and case["suspects"]:
        st.subheader("Suspects")
        for i, suspect in enumerate(case["suspects"]):
            with st.expander(f"Suspect {i+1}: {suspect.get('name', 'Unknown')}"):
                for key, value in suspect.items():
                    if key != "name":
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