import streamlit as st
import datetime
import pandas as pd
from .schedule_themes import get_theme_color
from .schedule_charts import render_enhanced_chart

def render_single_day_schedule(tasks_data, day_index=None, day_theme=""):
    """Render a single day's schedule with enhanced interactivity"""
    
    # Create unique key suffix for multi-day support
    key_suffix = f"_day_{day_index}" if day_index is not None else ""
    
    # Create DataFrame for schedule
    schedule_df = pd.DataFrame(tasks_data)

    # Rename columns for display
    column_names = {
        'task_name': 'Task',
        'start_time': 'Start Time',
        'end_time': 'End Time',
        'priority': 'Priority',
        'notes': 'Notes'
    }

    display_df = schedule_df.rename(columns=column_names)
    
    # Enhanced schedule display with theme-based styling
    if day_theme:
        theme_color = get_theme_color(day_theme)
        st.markdown(f"""
        <div style="background: linear-gradient(90deg, {theme_color}20, transparent); 
                    padding: 10px; border-radius: 5px; margin: 10px 0;">
            <h4 style="color: {theme_color}; margin: 0;">📋 {day_theme} Schedule</h4>
        </div>
        """, unsafe_allow_html=True)
    
    # Add task filtering options
    col1, col2, col3 = st.columns(3)
    with col1:
        show_all_tasks = st.checkbox("Show All Tasks", value=True, key=f"show_all{key_suffix}")
    with col2:
        if not show_all_tasks:
            filter_priority = st.selectbox(
                "Filter by Priority:",
                options=["All"] + list(schedule_df['priority'].unique()),
                key=f"filter_priority{key_suffix}"
            )
        else:
            filter_priority = "All"
    with col3:
        if not show_all_tasks:
            filter_category = st.selectbox(
                "Filter by Category:",
                options=["All"] + list(schedule_df['category'].unique()),
                key=f"filter_category{key_suffix}"
            )
        else:
            filter_category = "All"
    
    # Apply filters
    filtered_df = display_df.copy()
    if not show_all_tasks:
        if filter_priority != "All":
            filtered_df = filtered_df[filtered_df['Priority'] == filter_priority]
        if filter_category != "All":
            filtered_df = filtered_df[filtered_df['category'] == filter_category]
    
    # Display filtered schedule
    st.dataframe(filtered_df, use_container_width=True)

    # Enhanced chart controls with real-time updates
    st.markdown("### 📊 Interactive Timeline")
    
    # Chart configuration options
    chart_col1, chart_col2, chart_col3 = st.columns(3)
    with chart_col1:
        show_chart = st.checkbox("Show Timeline Chart", value=True, 
                                key=f"chart_toggle{key_suffix}")
    with chart_col2:
        chart_style = st.selectbox(
            "Chart Style:",
            ["Timeline", "Bar Chart", "Compact"],
            key=f"chart_style{key_suffix}"
        )
    with chart_col3:
        show_priorities = st.checkbox("Color by Priority", value=True, 
                                     key=f"show_priorities{key_suffix}")
    
    # Real-time chart update based on selections
    if show_chart:
        render_enhanced_chart(schedule_df, day_index, chart_style, show_priorities, day_theme)
    
    # Enhanced download options
    st.markdown("### 📥 Export Options")
    download_col1, download_col2, download_col3 = st.columns(3)
    
    with download_col1:
        csv_data = schedule_df.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv_data,
            file_name=f"chrona_schedule_{datetime.date.today()}{key_suffix}.csv",
            mime="text/csv",
            key=f"download_csv{key_suffix}"
        )
    
    with download_col2:
        json_data = schedule_df.to_json(orient='records', indent=2)
        if json_data:
            st.download_button(
                label="📋 Download JSON",
                data=json_data,
                file_name=f"chrona_schedule_{datetime.date.today()}{key_suffix}.json",
                mime="application/json",
                key=f"download_json{key_suffix}"
            )
    
    with download_col3:
        # Text format with theme information
        text_data = f"CHRONA AI SCHEDULE - {day_theme}\n" + "="*50 + "\n\n"
        for idx, task in schedule_df.iterrows():
            text_data += f"{task['start_time']} - {task['end_time']}: {task['task_name']}\n"
            text_data += f"  Priority: {str(task.get('priority', 'medium')).title()}\n"
            text_data += f"  Category: {task.get('category', 'General')}\n"
            text_data += f"  Notes: {task.get('notes', 'No notes')}\n\n"
        
        if text_data:
            st.download_button(
                label="📝 Download TXT",
                data=text_data,
                file_name=f"chrona_schedule_{datetime.date.today()}{key_suffix}.txt",
                mime="text/plain",
                key=f"download_txt{key_suffix}"
            ) 