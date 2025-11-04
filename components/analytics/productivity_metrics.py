import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from .data_manager import get_analytics_data

def render_productivity_metrics():
    """Render productivity metrics and patterns"""
    st.markdown("### 🎯 Productivity Patterns")
    
    analytics_data = get_analytics_data()
    sessions = analytics_data.get('sessions', [])
    
    if not sessions:
        st.info("📊 **Track productivity over time!**\n\nOptimize schedules regularly to see productivity patterns and improvement trends.")
        return
    
    # Productivity distribution
    if len(sessions) > 1:
        _render_productivity_distribution(sessions)
    
    # Session patterns
    if len(sessions) >= 5:
        _render_session_patterns(sessions)

def _render_productivity_distribution(sessions):
    """Render productivity score distribution analysis"""
    st.markdown("#### 📈 Productivity Score Distribution")
    
    scores = [s.get('productivity_score', 0) for s in sessions]
    
    col1, col2 = st.columns(2)
    
    with col1:
        _render_productivity_histogram(scores)
    
    with col2:
        _render_productivity_statistics(scores)

def _render_productivity_histogram(scores):
    """Render productivity score histogram"""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.hist(scores, bins=10, alpha=0.7, color='#4CAF50', edgecolor='black')
    ax.set_title('Productivity Score Distribution', fontweight='bold')
    ax.set_xlabel('Productivity Score')
    ax.set_ylabel('Frequency')
    ax.axvline(float(np.mean(scores)), color='red', linestyle='--', label=f'Average: {np.mean(scores):.1f}')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def _render_productivity_statistics(scores):
    """Render productivity statistics"""
    st.markdown("**Statistics:**")
    st.metric("Average Score", f"{np.mean(scores):.1f}")
    st.metric("Best Score", f"{np.max(scores):.1f}")
    st.metric("Improvement", f"+{np.max(scores) - np.min(scores):.1f}")
    
    if np.std(scores) < 10:
        st.success("🎯 Consistent productivity levels!")
    else:
        st.info("📊 Variable productivity - look for patterns to optimize")

def _render_session_patterns(sessions):
    """Render session patterns analysis"""
    st.markdown("#### 📅 Session Patterns")
    
    # Tasks per session trend
    task_counts = [s.get('total_tasks', 0) for s in sessions]
    session_numbers = list(range(1, len(sessions) + 1))
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Tasks per session
    ax1.plot(session_numbers, task_counts, marker='o', color='#2196F3')
    ax1.set_title('Tasks per Session Over Time', fontweight='bold')
    ax1.set_ylabel('Number of Tasks')
    ax1.grid(True, alpha=0.3)
    
    # Time per session
    time_per_session = [s.get('total_duration', 0) for s in sessions]
    ax2.plot(session_numbers, time_per_session, marker='s', color='#FF9800')
    ax2.set_title('Total Time per Session Over Time', fontweight='bold')
    ax2.set_xlabel('Session Number')
    ax2.set_ylabel('Total Duration (minutes)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig) 