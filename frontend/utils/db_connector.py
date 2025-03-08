import streamlit as st
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@st.cache_resource
def get_database_connection():
    """
    Create a cached connection to MongoDB
    """
    try:
        connection_string = os.getenv("MONGO_URI")
        if not connection_string:
            st.error("MongoDB connection string not found in environment variables")
            return None
            
        client = MongoClient(connection_string)
        return client.crimewatch
    except Exception as e:
        st.error(f"Failed to connect to database: {e}")
        return None