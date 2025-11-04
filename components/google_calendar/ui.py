"""
Google Calendar UI Module

This module handles the main UI rendering components including:
- Main dashboard interface
- Tab navigation
- Action buttons
- Status displays
"""

import streamlit as st
from .auth import is_authenticated, render_authentication_section, render_setup_instructions, check_google_calendar_api
from .export import render_export_section, sync_tasks_to_calendar
from .import_calendar import render_import_section, import_calendar_events
from .sync import render_sync_status
from .settings import render_calendar_settings

def render_google_calendar_integration(optimizer):
    """
    Render the Google Calendar Integration tab.
    
    Args:
        optimizer: The ScheduleOptimizer instance
    """
    st.markdown("# 📅 Google Calendar Integration")
    st.markdown("Connect your schedule optimizer with Google Calendar to sync tasks and events seamlessly.")
    
    # Check if Google Calendar API is available
    if not check_google_calendar_api():
        render_setup_instructions()
        return
    
    # Initialize calendar state
    if 'calendar_authenticated' not in st.session_state:
        st.session_state.calendar_authenticated = False
    
    # Main layout
    if not is_authenticated():
        render_authentication_section()
    else:
        render_calendar_dashboard(optimizer)

def render_calendar_dashboard(optimizer):
    """Render the main calendar dashboard when authenticated"""
    st.success("✅ Connected to Google Calendar")
    
    # Action buttons
    render_action_buttons(optimizer)
    
    st.markdown("---")
    
    # Main dashboard tabs
    render_dashboard_tabs(optimizer)

def render_action_buttons(optimizer):
    """Render the main action buttons"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Sync Tasks to Calendar"):
            sync_tasks_to_calendar(optimizer)
    
    with col2:
        if st.button("📥 Import Calendar Events"):
            import_calendar_events(optimizer)
    
    with col3:
        if st.button("🔓 Disconnect"):
            from .auth import disconnect_calendar
            disconnect_calendar()
            st.session_state.calendar_authenticated = False
            st.rerun()

def render_dashboard_tabs(optimizer):
    """Render the main dashboard tabs"""
    tab1, tab2, tab3, tab4 = st.tabs([
        "📤 Export to Calendar",
        "📥 Import from Calendar", 
        "🔄 Sync Status",
        "⚙️ Settings"
    ])
    
    with tab1:
        render_export_section(optimizer)
    
    with tab2:
        render_import_section(optimizer)
    
    with tab3:
        render_sync_status()
    
    with tab4:
        render_calendar_settings()

def render_connection_status():
    """Render connection status indicator"""
    if is_authenticated():
        st.success("🔗 Connected to Google Calendar")
    else:
        st.error("❌ Not connected to Google Calendar")

def render_quick_stats(optimizer):
    """Render quick statistics"""
    if not is_authenticated():
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        task_count = len(optimizer.tasks) if optimizer.tasks else 0
        st.metric("📝 Tasks Ready", task_count)
    
    with col2:
        sync_count = st.session_state.get('sync_data', {}).get('total_synced', 0)
        st.metric("🔄 Tasks Synced", sync_count)
    
    with col3:
        import_count = st.session_state.get('sync_data', {}).get('total_imported', 0)
        st.metric("📥 Events Imported", import_count)

def render_help_section():
    """Render help and documentation section"""
    with st.expander("❓ Help & Documentation"):
        st.markdown("""
        ### 🚀 Getting Started
        
        1. **Connect your Google Calendar** by clicking the connect button
        2. **Export tasks** to your calendar using the Export tab
        3. **Import events** from your calendar using the Import tab
        4. **Configure settings** in the Settings tab
        
        ### 📤 Exporting Tasks
        
        - Select which tasks to export
        - Choose your target calendar
        - Set start date and time
        - Add breaks between tasks
        
        ### 📥 Importing Events
        
        - Select date range to import
        - Choose source calendar
        - Convert events to tasks
        - Preview before importing
        
        ### 🔄 Sync Status
        
        - View sync history
        - Monitor sync errors
        - Perform manual sync
        - Clear sync history
        
        ### ⚙️ Settings
        
        - Configure auto-sync
        - Set sync intervals
        - Customize event appearance
        - Manage account connection
        """)

def render_troubleshooting():
    """Render troubleshooting section"""
    with st.expander("🔧 Troubleshooting"):
        st.markdown("""
        ### Common Issues
        
        **❌ "Not connected to Google Calendar"**
        - Make sure you've completed the OAuth flow
        - Check that your credentials file is valid
        - Try refreshing the token in Settings
        
        **❌ "Export failed"**
        - Verify you have calendar write permissions
        - Check that the target calendar exists
        - Ensure tasks have valid names and durations
        
        **❌ "Import failed"**
        - Verify you have calendar read permissions
        - Check the date range is valid
        - Ensure the source calendar exists
        
        **❌ "Sync errors"**
        - Check your internet connection
        - Verify API quotas haven't been exceeded
        - Try disconnecting and reconnecting
        
        ### Getting Help
        
        If you continue to have issues:
        1. Check the sync status for error details
        2. Try clearing sync history
        3. Disconnect and reconnect your account
        4. Verify your Google Cloud project settings
        """)

def render_feature_overview():
    """Render feature overview section"""
    with st.expander("✨ Feature Overview"):
        st.markdown("""
        ### 📋 What You Can Do
        
        **📤 Export Tasks to Calendar**
        - ✅ Select specific tasks to export
        - ✅ Schedule tasks with proper timing
        - ✅ Add breaks between tasks
        - ✅ Choose target calendar
        - ✅ Include task notes and metadata
        
        **📥 Import Events from Calendar**
        - ✅ Import events from any date range
        - ✅ Convert events to optimizer tasks
        - ✅ Preview events before import
        - ✅ Choose source calendar
        
        **🔄 Sync Management**
        - ✅ Real-time sync status
        - ✅ Sync history tracking
        - ✅ Manual sync controls
        - ✅ Error monitoring
        - ✅ Auto-sync options
        
        **⚙️ Customization**
        - ✅ Event colors and privacy
        - ✅ Sync intervals
        - ✅ Notification preferences
        - ✅ Default calendars
        - ✅ Conflict resolution
        """)

def render_footer_info():
    """Render footer information"""
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_help_section()
    
    with col2:
        render_troubleshooting()
    
    with col3:
        render_feature_overview()
    
    # Connection status at bottom
    render_connection_status() 