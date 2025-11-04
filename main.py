
import streamlit as st
from config import setup_page_config, get_api_key
from schedule_optimizer import ScheduleOptimizer
from ui_components import (
    render_header, 
    render_preferences_sidebar, 
    render_footer,
    load_custom_styles
)
from components.dashboard import render_dashboard_overview
from components.task_builder import render_task_builder
from components.schedule_upload import render_schedule_upload
from components.analytics import render_analytics
from components.google_calendar import render_google_calendar_integration

def main():
    """
    Main application entry point with modular component structure.
    """
    # Setup page configuration and styling
    setup_page_config()
    
    # Load custom styles from components (ensures consistent styling)
    load_custom_styles()

    # Render main header
    render_header()

    # Initialize optimizer
    if 'optimizer' not in st.session_state:
        st.session_state.optimizer = ScheduleOptimizer()

    # Initialize API
    if 'api_initialized' not in st.session_state:
        api_key = get_api_key()
        if api_key and st.session_state.optimizer.initialize_genai(api_key):
            st.session_state.api_initialized = True
        else:
            st.session_state.api_initialized = False

    # Render sidebar preferences
    preferences = render_preferences_sidebar()

    # Render dashboard overview
    render_dashboard_overview(st.session_state.optimizer)

    # Simplified tab selection using widget state directly
    tab_options = ["📝 Task Builder", "📄 Schedule Upload", "📅 Google Calendar (WIP)", "📊 Analytics & Insights"]
    
    # Initialize tab index if not exists
    if 'tab_index' not in st.session_state:
        st.session_state.tab_index = 0
    
    # Main content with tab selection
    selected_tab = st.radio(
        "Select Mode:",
        tab_options,
        index=st.session_state.tab_index,
        horizontal=True,
        key="main_tab_selector"
    )
    
    # Update tab index based on selection
    if selected_tab != tab_options[st.session_state.tab_index]:
        st.session_state.tab_index = tab_options.index(selected_tab)
    
    # Set active tab for backwards compatibility
    if selected_tab == "📝 Task Builder":
        st.session_state.active_tab = "Task Builder"
    elif selected_tab == "📄 Schedule Upload":
        st.session_state.active_tab = "Schedule Upload"
    elif selected_tab == "📅 Google Calendar (WIP)":
        st.session_state.active_tab = "Google Calendar (WIP)"
    else:
        st.session_state.active_tab = "Analytics"
    
    # Add some spacing
    st.markdown("---")
    
    if selected_tab == "📝 Task Builder":
        # Task Builder tab functionality
        render_task_builder(st.session_state.optimizer, preferences)
    elif selected_tab == "📄 Schedule Upload":
        # Schedule Upload tab functionality
        render_schedule_upload(st.session_state.optimizer)
    elif selected_tab == "📅 Google Calendar (WIP)":
        # Google Calendar Integration tab functionality
        render_google_calendar_integration(st.session_state.optimizer)
    else:
        # Analytics & Insights tab functionality
        render_analytics(st.session_state.optimizer, preferences)

    # Add some spacing before footer
    st.markdown("---")
    
    # Render footer
    render_footer()

if __name__ == "__main__":
    main()
