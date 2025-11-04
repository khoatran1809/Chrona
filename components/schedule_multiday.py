import streamlit as st
import datetime
import pandas as pd
from .schedule_themes import get_theme_emoji
from .schedule_single_day import render_single_day_schedule

def render_multi_day_schedule(schedule_data):
    """Render multi-day schedule with enhanced day-specific charts"""
    
    # Initialize session state for active day if not exists
    if 'active_day_index' not in st.session_state:
        st.session_state.active_day_index = 0
    
    # Create tabs for each day
    if len(schedule_data) > 1:
        day_names = [day_data["day_name"] for day_data in schedule_data]
        
        # Display day themes if available
        if "theme" in schedule_data[0]:
            st.markdown("### 🎯 Daily Themes Overview")
            theme_cols = st.columns(min(len(schedule_data), 4))  # Max 4 columns
            
            for i, day_data in enumerate(schedule_data):
                col_idx = i % 4
                with theme_cols[col_idx]:
                    theme_emoji = get_theme_emoji(day_data.get("theme", ""))
                    st.markdown(f"""
                    **{theme_emoji} {day_data['day_name']}**  
                    *{day_data.get('theme', 'Standard')}*  
                    📋 {day_data.get('focus', 'Mixed tasks')}  
                    ⚡ {day_data.get('energy_pattern', 'Steady')}
                    """)
        
        # Create interactive day selection
        st.markdown("### 📊 Daily Schedule Details")
        selected_day = st.selectbox(
            "Select Day to View:",
            options=range(len(schedule_data)),
            format_func=lambda x: f"{schedule_data[x]['day_name']} - {schedule_data[x].get('theme', 'Standard')}",
            index=st.session_state.active_day_index,
            key="day_selector"
        )
        
        # Update active day index
        st.session_state.active_day_index = selected_day
        
        # Show selected day's schedule
        day_data = schedule_data[selected_day]
        st.markdown(f"#### {get_theme_emoji(day_data.get('theme', ''))} {day_data['day_name']} - {day_data.get('theme', 'Standard')}")
        
        # Add day-specific insights
        if "focus" in day_data:
            st.info(f"🎯 **Focus**: {day_data['focus']} | ⚡ **Energy**: {day_data.get('energy_pattern', 'Steady')}")
        
        # Render the selected day with enhanced features
        render_single_day_schedule(day_data["tasks"], day_index=selected_day, day_theme=day_data.get("theme", ""))
        
        # Add day comparison features for multi-day schedules
        if len(schedule_data) > 2:
            render_day_comparison(schedule_data, selected_day)
    else:
        # Single day in multi-day format
        day_data = schedule_data[0]
        st.markdown(f"### {get_theme_emoji(day_data.get('theme', ''))} {day_data['day_name']} - {day_data.get('theme', 'Standard')}")
        render_single_day_schedule(day_data["tasks"], day_index=0, day_theme=day_data.get("theme", ""))

def render_day_comparison(schedule_data, selected_day):
    """Render day comparison features"""
    st.markdown("### 📈 Day Comparison")
    
    # Calculate metrics for each day
    day_metrics = []
    for day_data in schedule_data:
        tasks = day_data["tasks"]
        work_tasks = [t for t in tasks if t.get("category", "").lower() in ["work", "learning"]]
        personal_tasks = [t for t in tasks if t.get("category", "").lower() in ["personal", "health"]]
        
        # Calculate durations
        work_duration = sum([
            (datetime.datetime.strptime(t["end_time"], "%H:%M") - 
             datetime.datetime.strptime(t["start_time"], "%H:%M")).total_seconds() / 3600 
            for t in work_tasks
        ])
        
        personal_duration = sum([
            (datetime.datetime.strptime(t["end_time"], "%H:%M") - 
             datetime.datetime.strptime(t["start_time"], "%H:%M")).total_seconds() / 3600 
            for t in personal_tasks
        ])
        
        day_metrics.append({
            "day": day_data["day_name"],
            "theme": day_data.get("theme", "Standard"),
            "work_hours": round(work_duration, 1),
            "personal_hours": round(personal_duration, 1),
            "total_tasks": len(tasks),
            "work_tasks": len(work_tasks),
            "personal_tasks": len(personal_tasks)
        })
    
    # Display comparison
    comparison_df = pd.DataFrame(day_metrics)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**⏰ Time Distribution**")
        st.dataframe(comparison_df[["day", "theme", "work_hours", "personal_hours"]], 
                    use_container_width=True)
    
    with col2:
        st.markdown("**📋 Task Distribution**")
        st.dataframe(comparison_df[["day", "total_tasks", "work_tasks", "personal_tasks"]], 
                    use_container_width=True) 