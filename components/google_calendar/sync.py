"""
Google Calendar Sync Module

This module handles sync status and management including:
- Sync status tracking
- Sync history management
- Manual sync controls
- Sync error handling
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

from .auth import get_calendar_service
from .export import sync_tasks_to_calendar
from .import_calendar import import_calendar_events

def render_sync_status():
    """Render sync status and history"""
    st.markdown("### 🔄 Sync Status & History")
    
    # Initialize sync data if not exists
    if 'sync_data' not in st.session_state:
        st.session_state.sync_data = initialize_sync_data()
    
    # Sync status overview
    sync_data = st.session_state.sync_data
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        last_sync = get_last_sync_time()
        st.metric("Last Sync", last_sync, "✅" if last_sync != "Never" else "❌")
    with col2:
        total_synced = get_total_synced_tasks()
        st.metric("Tasks Synced", total_synced, f"+{sync_data.get('recent_synced', 0)}")
    with col3:
        total_imported = get_total_imported_events()
        st.metric("Events Imported", total_imported, f"+{sync_data.get('recent_imported', 0)}")
    with col4:
        error_count = get_sync_error_count()
        st.metric("Sync Errors", error_count, "✅" if error_count == 0 else "⚠️")
    
    # Sync history
    st.markdown("#### 📊 Recent Sync Activity")
    
    sync_history = get_sync_history()
    if sync_history is not None and not sync_history.empty:
        st.dataframe(sync_history, use_container_width=True)
    else:
        st.info("📋 No sync history available yet.")
    
    # Manual sync controls
    st.markdown("#### 🔧 Manual Sync Controls")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Force Full Sync"):
            perform_full_sync()
    
    with col2:
        if st.button("🗑️ Clear Sync History"):
            clear_sync_history()
            st.success("🗑️ Sync history cleared!")
            st.rerun()

def initialize_sync_data():
    """Initialize sync data structure"""
    return {
        'history': [],
        'last_sync': None,
        'total_synced': 0,
        'total_imported': 0,
        'recent_synced': 0,
        'recent_imported': 0,
        'error_count': 0
    }

def get_last_sync_time():
    """Get the last sync time formatted for display"""
    if 'sync_data' not in st.session_state:
        return "Never"
    
    last_sync = st.session_state.sync_data.get('last_sync')
    if not last_sync:
        return "Never"
    
    now = datetime.now()
    diff = now - last_sync
    
    if diff.days > 0:
        return f"{diff.days} days ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hours ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minutes ago"
    else:
        return "Just now"

def get_total_synced_tasks():
    """Get total number of synced tasks"""
    if 'sync_data' not in st.session_state:
        return 0
    return st.session_state.sync_data.get('total_synced', 0)

def get_total_imported_events():
    """Get total number of imported events"""
    if 'sync_data' not in st.session_state:
        return 0
    return st.session_state.sync_data.get('total_imported', 0)

def get_sync_error_count():
    """Get current sync error count"""
    if 'sync_data' not in st.session_state:
        return 0
    return st.session_state.sync_data.get('error_count', 0)

def get_sync_history():
    """Get sync history as DataFrame"""
    if 'sync_data' not in st.session_state:
        return None
    
    history = st.session_state.sync_data.get('history', [])
    if not history:
        return None
    
    return pd.DataFrame(history)

def add_sync_record(action, status, details, count=0):
    """Add a sync record to history"""
    if 'sync_data' not in st.session_state:
        st.session_state.sync_data = initialize_sync_data()
    
    record = {
        'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Action': action,
        'Status': status,
        'Details': details,
        'Count': count
    }
    
    st.session_state.sync_data['history'].append(record)
    st.session_state.sync_data['last_sync'] = datetime.now()
    
    # Keep only last 50 records
    if len(st.session_state.sync_data['history']) > 50:
        st.session_state.sync_data['history'] = st.session_state.sync_data['history'][-50:]
    
    # Update counters
    if action == "Export Tasks" and status == "✅ Success":
        st.session_state.sync_data['total_synced'] += count
        st.session_state.sync_data['recent_synced'] = count
    elif action == "Import Events" and status == "✅ Success":
        st.session_state.sync_data['total_imported'] += count
        st.session_state.sync_data['recent_imported'] = count
    
    if "Failed" in status or "Error" in status:
        st.session_state.sync_data['error_count'] += 1
    else:
        st.session_state.sync_data['error_count'] = 0  # Reset on success

def perform_full_sync():
    """Perform a full sync operation"""
    service = get_calendar_service()
    if not service:
        st.error("❌ Not connected to Google Calendar!")
        add_sync_record("Full Sync", "❌ Failed", "Not connected to Google Calendar")
        return
    
    with st.spinner("🔄 Performing full sync with Google Calendar..."):
        try:
            # Get current tasks and events
            if 'optimizer' in st.session_state and st.session_state.optimizer.tasks:
                # Export tasks
                sync_tasks_to_calendar(st.session_state.optimizer)
                task_count = len(st.session_state.optimizer.tasks)
                add_sync_record("Full Sync - Export", "✅ Success", f"Exported {task_count} tasks", task_count)
            
            # Import events
            now = datetime.utcnow().isoformat() + 'Z'
            end_time = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
            
            events_result = service.events().list(
                calendarId='primary',
                timeMin=now,
                timeMax=end_time,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            add_sync_record("Full Sync - Import", "✅ Success", f"Imported {len(events)} events", len(events))
            
            st.success(f"✅ Full sync completed! Synced {task_count if 'task_count' in locals() else 0} tasks and imported {len(events)} events.")
            
        except Exception as e:
            error_msg = f"Full sync failed: {str(e)}"
            st.error(f"❌ {error_msg}")
            add_sync_record("Full Sync", "❌ Failed", error_msg)

def clear_sync_history():
    """Clear sync history"""
    if 'sync_data' in st.session_state:
        st.session_state.sync_data['history'] = []
        st.session_state.sync_data['error_count'] = 0

def get_sync_statistics():
    """Get sync statistics for display"""
    if 'sync_data' not in st.session_state:
        return {
            'total_syncs': 0,
            'successful_syncs': 0,
            'failed_syncs': 0,
            'success_rate': 0
        }
    
    history = st.session_state.sync_data.get('history', [])
    total_syncs = len(history)
    successful_syncs = len([h for h in history if '✅' in h.get('Status', '')])
    failed_syncs = total_syncs - successful_syncs
    success_rate = (successful_syncs / total_syncs * 100) if total_syncs > 0 else 0
    
    return {
        'total_syncs': total_syncs,
        'successful_syncs': successful_syncs,
        'failed_syncs': failed_syncs,
        'success_rate': success_rate
    }

def render_sync_statistics():
    """Render sync statistics"""
    stats = get_sync_statistics()
    
    st.markdown("#### 📈 Sync Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Syncs", stats['total_syncs'])
    with col2:
        st.metric("Successful", stats['successful_syncs'])
    with col3:
        st.metric("Failed", stats['failed_syncs'])
    with col4:
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")

def auto_sync_check():
    """Check if auto-sync should be performed"""
    if not st.session_state.get('calendar_authenticated', False):
        return False
    
    # Check auto-sync settings
    auto_sync_enabled = st.session_state.get('auto_sync_enabled', False)
    if not auto_sync_enabled:
        return False
    
    # Check last sync time
    last_sync = st.session_state.get('sync_data', {}).get('last_sync')
    if not last_sync:
        return True
    
    # Check sync interval
    sync_interval = st.session_state.get('sync_interval', 'Every hour')
    now = datetime.now()
    
    if sync_interval == "Real-time":
        return True
    elif sync_interval == "Every 15 minutes":
        return (now - last_sync).total_seconds() > 900  # 15 minutes
    elif sync_interval == "Every hour":
        return (now - last_sync).total_seconds() > 3600  # 1 hour
    elif sync_interval == "Daily":
        return (now - last_sync).total_seconds() > 86400  # 24 hours
    
    return False

def schedule_auto_sync():
    """Schedule automatic sync if conditions are met"""
    if auto_sync_check():
        perform_full_sync() 