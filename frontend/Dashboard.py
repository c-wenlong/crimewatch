import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from utils.db_connector import get_database_connection

st.set_page_config(
    page_title="Case Management System", 
    page_icon="🔍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

def load_cases():
    """Load all cases from database"""
    db = get_database_connection()
    if not db:
        st.warning("Unable to connect to database. Showing sample data.")
        # Return sample data or empty DataFrame
        return pd.DataFrame()
    
    try:
        cases_cursor = db.test_case.find({})
        cases = list(cases_cursor)
        return pd.DataFrame(cases)
    except Exception as e:
        st.error(f"Error loading cases: {e}")
        return pd.DataFrame()

def show_dashboard():
    st.title("📊 Case Dashboard")
    st.write("Welcome to the Criminal Case Management System. Select a case to view details.")
    
    # Load case data
    df = load_cases()
    
    if df.empty:
        st.warning("No cases found in the database.")
        return
    
    # Filter columns for dashboard view
    df_dashboard = df[['case_id', 'title', 'type', 'status', 'date_opened', 'location']]
    
    # Build grid options with AgGrid
    gb = GridOptionsBuilder.from_dataframe(df_dashboard)
    gb.configure_selection("single", use_checkbox=False)
    gb.configure_grid_options(domLayout='normal')
    gb.configure_column("case_id", headerName="Case ID")
    gb.configure_column("title", headerName="Case Title")
    gb.configure_column("type", headerName="Type")
    gb.configure_column("status", header_name="Status", cellStyle={"styleConditions": [
        {"condition": "params.value == 'Active'", "style": {"color": "red"}},
        {"condition": "params.value == 'Solved'", "style": {"color": "green"}},
        {"condition": "params.value == 'Archived'", "style": {"color": "gray"}},
    ]})
    gb.configure_column("date_opened", headerName="Date Opened")
    gb.configure_column("location", headerName="Location")
    
    grid_options = gb.build()
    
    # Display filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_status = st.multiselect("Filter by Status:", options=df_dashboard["status"].unique())
    with col2:
        filter_type = st.multiselect("Filter by Type:", options=df_dashboard["type"].unique())
    with col3:
        search_query = st.text_input("Search by Title:")
    
    # Apply filters
    filtered_df = df_dashboard
    if filter_status:
        filtered_df = filtered_df[filtered_df["status"].isin(filter_status)]
    if filter_type:
        filtered_df = filtered_df[filtered_df["type"].isin(filter_type)]
    if search_query:
        filtered_df = filtered_df[filtered_df["title"].str.contains(search_query, case=False)]
    
    # Render AgGrid table
    grid_response = AgGrid(
        filtered_df,
        gridOptions=grid_options,
        enable_enterprise_modules=False,
        update_mode="MODEL_CHANGED",
        height=250,
        fit_columns_on_grid_load=True,
        theme="streamlit",
    )
    
    selected_rows = grid_response.get("selected_rows")
    if selected_rows is not None and len(selected_rows) > 0:
        st.session_state.selected_case = selected_rows["case_id"][0]
        st.success(f"Case '{selected_rows['title'][0]}' selected. Navigate to Case Details page to view more information.")

def main():
    st.sidebar.title("Navigation")
    st.sidebar.info("""
    Use the pages in the sidebar to navigate between different views:
    - Dashboard (Home)
    - Case Details
    - Chatbot
    - Timeline View
    """)
    
    # Display metrics
    db = get_database_connection()
    if db:
        try:
            total_cases = db.test_case.count_documents({})
            open_cases = db.test_case.count_documents({"status": "Active"})
            closed_cases = db.test_case.count_documents({"status": "Solved"})
            archived_cases = db.test_case.count_documents({"status": "Archived"})
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Cases", total_cases)
            col2.metric("Active Cases", open_cases)
            col3.metric("Solved Cases", closed_cases)
            col4.metric("Archived Cases", archived_cases)
        except Exception as e:
            st.error(f"Error calculating metrics: {e}")
    
    show_dashboard()

if __name__ == "__main__":
    main()