"""
Google Calendar Authentication Module

This module handles Google Calendar API authentication including:
- OAuth 2.0 authentication flow
- Credential management and storage
- Token refresh handling
- Service initialization
"""

import streamlit as st
import os

# Google Calendar API imports
try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from google.oauth2 import service_account
    GOOGLE_CALENDAR_AVAILABLE = True
except ImportError:
    GOOGLE_CALENDAR_AVAILABLE = False

def check_google_calendar_api():
    """Check if Google Calendar API dependencies are available"""
    return GOOGLE_CALENDAR_AVAILABLE

def authenticate_google_calendar():
    """Authenticate with Google Calendar API"""
    if not GOOGLE_CALENDAR_AVAILABLE:
        return False
    
    try:
        # Define scopes
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        
        # Load credentials
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = Flow.from_client_secrets_file(
                    'google_calendar_credentials.json', SCOPES)
                flow.redirect_uri = 'http://localhost:8501'
                
                # Generate authorization URL
                auth_url, _ = flow.authorization_url(prompt='consent')
                st.markdown(f"[🔗 Click here to authorize Google Calendar access]({auth_url})")
                
                # Get authorization code from user
                auth_code = st.text_input("Enter the authorization code:")
                if auth_code:
                    try:
                        flow.fetch_token(code=auth_code)
                        creds = flow.credentials
                        
                        # Save credentials for next run
                        with open('token.json', 'w') as token:
                            token.write(creds.to_json())
                        
                        st.session_state.calendar_service = build('calendar', 'v3', credentials=creds)
                        return True
                    except Exception as e:
                        st.error(f"Authentication failed: {str(e)}")
                        return False
                else:
                    return False
        
        # Create service
        st.session_state.calendar_service = build('calendar', 'v3', credentials=creds)
        return True
        
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False

def get_calendar_service():
    """Get authenticated Google Calendar service"""
    if 'calendar_service' not in st.session_state:
        return None
    return st.session_state.calendar_service

def is_authenticated():
    """Check if user is authenticated with Google Calendar"""
    return st.session_state.get('calendar_authenticated', False)

def disconnect_calendar():
    """Disconnect from Google Calendar"""
    if 'calendar_service' in st.session_state:
        del st.session_state.calendar_service
    if 'calendar_authenticated' in st.session_state:
        del st.session_state.calendar_authenticated
    
    # Remove token file
    if os.path.exists('token.json'):
        os.remove('token.json')

def render_authentication_section():
    """Render Google Calendar authentication section"""
    st.markdown("### 🔐 Google Calendar Authentication")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.info("🔑 **Connect your Google Calendar account to sync your optimized schedules.**")
        
        # Check if credentials file exists
        if not os.path.exists('google_calendar_credentials.json'):
            st.warning("⚠️ **Google Calendar credentials not found.** Please follow the setup guide to configure OAuth credentials.")
            with st.expander("📖 Setup Instructions"):
                render_setup_instructions()
            return
        
        # Real authentication process
        if st.button("🔗 Connect Google Calendar", type="primary"):
            with st.spinner("Connecting to Google Calendar..."):
                success = authenticate_google_calendar()
                if success:
                    st.session_state.calendar_authenticated = True
                    st.success("✅ Successfully connected to Google Calendar!")
                    st.rerun()
                else:
                    st.error("❌ Failed to connect to Google Calendar. Please check your credentials.")
    
    with col2:
        st.markdown("#### 🛡️ Privacy & Security")
        st.markdown("""
        - Secure OAuth 2.0 authentication
        - Read/write calendar permissions
        - Data stays in your Google account
        - Revoke access anytime
        """)

def render_setup_instructions():
    """Render setup instructions for Google Calendar API"""
    st.warning("🔧 **Google Calendar API Setup Required**")
    
    st.markdown("""
    ### 📋 Setup Instructions
    
    To use Google Calendar integration, you need to:
    
    1. **Install Google Calendar API dependencies:**
    ```bash
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```
    
    2. **Set up Google Cloud Project:**
    - Go to [Google Cloud Console](https://console.cloud.google.com/)
    - Create a new project or select existing one
    - Enable Google Calendar API
    - Create credentials (OAuth 2.0 client ID)
    - Download the credentials JSON file
    
    3. **Configure credentials:**
    - Save the credentials file as `google_calendar_credentials.json` in your project root
    - The file should contain your OAuth 2.0 client configuration
    
    4. **Restart the application** after completing the setup
    """)
    
    with st.expander("🔍 **Show Example Credentials Structure**"):
        st.code("""
        {
            "web": {
                "client_id": "your-client-id.googleusercontent.com",
                "project_id": "your-project-id",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": "your-client-secret",
                "redirect_uris": ["http://localhost:8501"]
            }
        }
        """, language="json") 