import streamlit as st
import datetime
import numpy as np

def initialize_analytics_data():
    """Initialize analytics data structure"""
    return {
        'sessions': [],
        'task_completions': [],
        'time_tracking': [],
        'productivity_scores': [],
        'optimization_history': []
    }

def update_analytics_data(optimized_result, tasks):
    """Update analytics data with current session information"""
    if 'analytics_data' not in st.session_state:
        st.session_state.analytics_data = initialize_analytics_data()
    
    current_time = datetime.datetime.now()
    
    # Add session data
    session_data = {
        'timestamp': current_time,
        'total_tasks': len(tasks),
        'total_duration': sum(task.get('duration', 0) for task in tasks),
        'high_priority_tasks': len([t for t in tasks if t.get('priority') == 'high']),
        'productivity_score': optimized_result.get('daily_summary', {}).get('productivity_score', 0)
    }
    
    st.session_state.analytics_data['sessions'].append(session_data)
    
    # Keep only last 30 sessions to prevent memory issues
    if len(st.session_state.analytics_data['sessions']) > 30:
        st.session_state.analytics_data['sessions'] = st.session_state.analytics_data['sessions'][-30:]

def get_analytics_data():
    """Get current analytics data, initializing if necessary"""
    if 'analytics_data' not in st.session_state:
        st.session_state.analytics_data = initialize_analytics_data()
    return st.session_state.analytics_data

def clear_analytics_data():
    """Clear all analytics data"""
    st.session_state.analytics_data = initialize_analytics_data()

def calculate_key_metrics(sessions):
    """Calculate key metrics from session data"""
    if not sessions:
        return {
            'total_sessions': 0,
            'avg_productivity': 0,
            'total_tasks': 0,
            'total_time': 0
        }
    
    total_sessions = len(sessions)
    avg_productivity = np.mean([s.get('productivity_score', 0) for s in sessions])
    total_tasks = sum(s.get('total_tasks', 0) for s in sessions)
    total_time = sum(s.get('total_duration', 0) for s in sessions)
    
    return {
        'total_sessions': total_sessions,
        'avg_productivity': avg_productivity,
        'total_tasks': total_tasks,
        'total_time': total_time
    } 