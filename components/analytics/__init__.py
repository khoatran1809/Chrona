"""
Analytics Module for Chrona Schedule Optimizer

This module provides comprehensive analytics and insights functionality,
broken down into specialized components for better organization and maintainability.

"""

import streamlit as st

from .data_manager import initialize_analytics_data, update_analytics_data
from .overview import render_overview_analytics
from .time_analysis import render_time_analysis
from .productivity_metrics import render_productivity_metrics
from .task_insights import render_task_insights

def render_analytics(optimizer, preferences):
    """
    Render the Analytics & Insights tab with comprehensive productivity metrics.
    
    Args:
        optimizer: The ScheduleOptimizer instance
        preferences: User preferences from sidebar
    """
    st.markdown("# 📊 Analytics & Insights")
    st.markdown("Track your productivity patterns, analyze your scheduling habits, and discover insights to optimize your time.")
    
    # Initialize analytics data if not exists
    if 'analytics_data' not in st.session_state:
        st.session_state.analytics_data = initialize_analytics_data()
    
    # Add current session data if optimization results exist
    if hasattr(st.session_state, 'optimized_result') and optimizer.tasks:
        update_analytics_data(st.session_state.optimized_result, optimizer.tasks)
    
    # Main analytics layout
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Overview", 
        "⏰ Time Analysis", 
        "🎯 Productivity Metrics", 
        "📋 Task Insights"
    ])
    
    with tab1:
        render_overview_analytics()
    
    with tab2:
        render_time_analysis(optimizer)
    
    with tab3:
        render_productivity_metrics()
    
    with tab4:
        render_task_insights(optimizer)

# Export the main render function for backward compatibility
__all__ = ['render_analytics'] 