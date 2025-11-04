import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import datetime
from datetime import timedelta

from .data_manager import get_analytics_data, calculate_key_metrics

def render_overview_analytics():
    """Render overview analytics dashboard"""
    st.markdown("### 📊 Productivity Overview")
    
    # Get analytics data
    analytics_data = get_analytics_data()
    sessions = analytics_data.get('sessions', [])
    
    if not sessions:
        _render_empty_state()
        return
    
    # Calculate and display key metrics
    metrics = calculate_key_metrics(sessions)
    _render_key_metrics(metrics)
    
    # Productivity trend chart
    if len(sessions) > 1:
        _render_productivity_trend(sessions)
    
    # Recent insights
    _render_recent_insights(sessions)

def _render_empty_state():
    """Render empty state when no data is available"""
    st.info("📈 **Start optimizing schedules to see analytics!**\n\nCreate tasks and optimize schedules to begin tracking your productivity patterns.")
    
    # Show demo/preview of what analytics will look like
    st.markdown("### 🔮 Preview: What You'll See")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sessions", "12", "↗️ +3")
    with col2:
        st.metric("Avg Productivity", "85/100", "↗️ +5")
    with col3:
        st.metric("Tasks Completed", "156", "↗️ +23")
    with col4:
        st.metric("Time Optimized", "32 hrs", "↗️ +8 hrs")
    
    # Demo chart
    demo_dates = [datetime.datetime.now() - timedelta(days=x) for x in range(7, 0, -1)]
    demo_scores = [78, 82, 85, 79, 88, 91, 85]
    
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(mdates.date2num(demo_dates), demo_scores, marker='o', linewidth=2, markersize=6, color='#4CAF50')
    ax.set_title('Weekly Productivity Trend (Demo)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Productivity Score')
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def _render_key_metrics(metrics):
    """Render key metrics display"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sessions", metrics['total_sessions'])
    with col2:
        st.metric("Avg Productivity", f"{metrics['avg_productivity']:.0f}/100")
    with col3:
        st.metric("Tasks Planned", metrics['total_tasks'])
    with col4:
        total_time = metrics['total_time']
        st.metric("Time Planned", f"{total_time//60:.0f}h {total_time%60:.0f}m")

def _render_productivity_trend(sessions):
    """Render productivity trend chart"""
    st.markdown("### 📈 Productivity Trend")
    
    dates = [s['timestamp'] for s in sessions]
    scores = [s.get('productivity_score', 0) for s in sessions]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(dates, scores, marker='o', linewidth=2, markersize=6, color='#2196F3')
    ax.set_title('Productivity Score Over Time', fontsize=16, fontweight='bold')
    ax.set_ylabel('Productivity Score')
    ax.set_xlabel('Date')
    ax.grid(True, alpha=0.3)
    
    # Format x-axis
    if len(dates) > 7:
        ax.xaxis.set_major_locator(mdates.WeekdayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    plt.xticks(rotation=45)
    
    # Add trend line
    if len(sessions) > 2:
        z = np.polyfit(range(len(scores)), scores, 1)
        p = np.poly1d(z)
        ax.plot(dates, p(range(len(scores))), "--", alpha=0.7, color='red', label='Trend')
        ax.legend()
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def _render_recent_insights(sessions):
    """Render recent insights section"""
    st.markdown("### 💡 Recent Insights")
    
    if len(sessions) >= 3:
        recent_scores = [s.get('productivity_score', 0) for s in sessions[-3:]]
        trend = "improving" if recent_scores[-1] > recent_scores[0] else "declining"
        
        insights = [
            f"📈 Your productivity trend is **{trend}** over the last 3 sessions",
            f"🎯 You typically plan **{np.mean([s.get('total_tasks', 0) for s in sessions]):.1f} tasks** per session",
            f"⏰ Average planning time: **{np.mean([s.get('total_duration', 0) for s in sessions])//60:.0f}h {np.mean([s.get('total_duration', 0) for s in sessions])%60:.0f}m**"
        ]
        
        for insight in insights:
            st.info(insight)
    else:
        st.info("🔍 Create more optimized schedules to see personalized insights!") 