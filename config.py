
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
def setup_page_config():
    st.set_page_config(
        page_title="Chrona - Smart Schedule Optimizer",
        page_icon="📅",
        layout="wide",
        initial_sidebar_state="expanded"
    )

# Custom CSS
def load_custom_css():
    st.markdown("""
    <style>
        .stApp {
            background-color: #000000;
        }
        .main-header {
            text-align: center;
            padding: 2rem 0;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 10px;
            margin-bottom: 2rem;
        }
        .task-card {
            background: #1a1a1a;
            color: white;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            margin: 0.5rem 0;
        }
        .priority-high {
            border-left-color: #dc3545;
        }
        .priority-medium {
            border-left-color: #ffc107;
        }
        .priority-low {
            border-left-color: #28a745;
        }
        .metric-card {
            background: #1a1a1a;
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            text-align: center;
        }
        .stSidebar {
            background-color: #1a1a1a;
        }
        .stSelectbox > div > div {
            background-color: #2a2a2a;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #2a2a2a;
            color: white;
        }
        .stTextArea > div > div > textarea {
            background-color: #2a2a2a;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

def get_api_key():
    """Get API key from environment (backend configured)"""
    # API key should be configured in the backend environment
    api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    
    if not api_key:
        st.error("⚠️ API key not configured in backend environment")
        return None
    
    return api_key
