"""
Google Calendar Export Module

This module handles exporting tasks to Google Calendar including:
- Task selection interface
- Export options configuration
- Calendar event creation
- Scheduling and time management
"""

import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta

from .auth import get_calendar_service

def render_export_section(optimizer):
    """Render task export to Google Calendar section"""
    st.markdown("### 📤 Export Tasks to Google Calendar")
    
    if not optimizer.tasks:
        st.info("📝 **No tasks to export.** Add tasks in the Task Builder first.")
        return
    
    # Task selection
    st.markdown("#### 📋 Select Tasks to Export")
    
    tasks_df = pd.DataFrame([
        {
            'Select': True,
            'Task': task.get('name', 'Unnamed'),
            'Duration': f"{task.get('duration', 0)} min",
            'Priority': task.get('priority', 'medium'),
            'Category': task.get('category', 'Other')
        }
        for task in optimizer.tasks
    ])
    
    edited_df = st.data_editor(
        tasks_df,
        column_config={
            "Select": st.column_config.CheckboxColumn(
                "Export",
                help="Select tasks to export to Google Calendar",
                default=True,
            )
        },
        disabled=["Task", "Duration", "Priority", "Category"],
        hide_index=True,
        use_container_width=True
    )
    
    # Export options
    st.markdown("#### ⚙️ Export Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        calendar_name = st.selectbox(
            "📅 Target Calendar",
            ["Primary Calendar", "Work Calendar", "Personal Calendar"],
            help="Select which Google Calendar to export tasks to"
        )
        
        start_date = st.date_input(
            "📅 Start Date",
            value=datetime.date.today(),
            help="When to start scheduling the exported tasks"
        )
    
    with col2:
        start_time = st.time_input(
            "⏰ Start Time",
            value=datetime.time(9, 0),
            help="What time to start the first task"
        )
        
        add_breaks = st.checkbox(
            "☕ Add breaks between tasks",
            value=True,
            help="Add 15-minute breaks between tasks"
        )
    
    # Export button
    selected_tasks = edited_df[edited_df['Select']]['Task'].tolist()
    
    if st.button("📤 Export Selected Tasks", type="primary", disabled=len(selected_tasks) == 0):
        export_tasks_to_calendar(selected_tasks, calendar_name, start_date, start_time, add_breaks)

def export_tasks_to_calendar(selected_tasks, calendar_name, start_date, start_time, add_breaks):
    """Export selected tasks to Google Calendar"""
    service = get_calendar_service()
    if not service:
        st.error("❌ Not connected to Google Calendar!")
        return
    
    with st.spinner(f"Exporting {len(selected_tasks)} tasks to {calendar_name}..."):
        try:
            # Convert start_date and start_time to datetime
            start_datetime = datetime.datetime.combine(start_date, start_time)
            current_time = start_datetime
            
            exported_count = 0
            for task_name in selected_tasks:
                # Find the task in optimizer.tasks
                task = next((t for t in st.session_state.optimizer.tasks if t.get('name') == task_name), None)
                if not task:
                    continue
                
                # Create event
                duration = task.get('duration', 60)
                event = {
                    'summary': task_name,
                    'description': task.get('notes', ''),
                    'start': {
                        'dateTime': current_time.isoformat(),
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': (current_time + timedelta(minutes=duration)).isoformat(),
                        'timeZone': 'UTC',
                    },
                }
                
                # Add task metadata to description
                metadata = []
                if task.get('priority'):
                    metadata.append(f"Priority: {task.get('priority').title()}")
                if task.get('category'):
                    metadata.append(f"Category: {task.get('category')}")
                if task.get('duration'):
                    metadata.append(f"Duration: {task.get('duration')} minutes")
                
                if metadata:
                    event['description'] = f"{task.get('notes', '')}\n\n" + "\n".join(metadata)
                
                # Insert event
                service.events().insert(calendarId='primary', body=event).execute()
                exported_count += 1
                
                # Update time for next task
                current_time += timedelta(minutes=duration)
                if add_breaks:
                    current_time += timedelta(minutes=15)  # Add 15-minute break
                    
            st.success(f"✅ Successfully exported {exported_count} tasks to {calendar_name}!")
            
            # Show summary
            st.markdown("#### 📋 Export Summary")
            st.info(f"""
            **Exported {exported_count} tasks:**
            - 📅 Start Date: {start_date.strftime('%B %d, %Y')}
            - ⏰ Start Time: {start_time.strftime('%I:%M %p')}
            - 📍 Calendar: {calendar_name}
            - ☕ Breaks: {'Yes' if add_breaks else 'No'}
            """)
            
        except Exception as e:
            st.error(f"❌ Export failed: {str(e)}")

def sync_tasks_to_calendar(optimizer):
    """Sync all tasks to Google Calendar"""
    service = get_calendar_service()
    if not service:
        st.error("❌ Not connected to Google Calendar!")
        return
    
    with st.spinner("Syncing tasks to Google Calendar..."):
        try:
            synced_count = 0
            for task in optimizer.tasks:
                # Create event
                event = {
                    'summary': task.get('name', 'Unnamed Task'),
                    'description': task.get('notes', ''),
                    'start': {
                        'dateTime': datetime.datetime.now().isoformat(),
                        'timeZone': 'UTC',
                    },
                    'end': {
                        'dateTime': (datetime.datetime.now() + timedelta(minutes=task.get('duration', 60))).isoformat(),
                        'timeZone': 'UTC',
                    },
                }
                
                # Add task metadata
                metadata = []
                if task.get('priority'):
                    metadata.append(f"Priority: {task.get('priority').title()}")
                if task.get('category'):
                    metadata.append(f"Category: {task.get('category')}")
                if task.get('duration'):
                    metadata.append(f"Duration: {task.get('duration')} minutes")
                
                if metadata:
                    event['description'] = f"{task.get('notes', '')}\n\n" + "\n".join(metadata)
                
                # Insert event
                service.events().insert(calendarId='primary', body=event).execute()
                synced_count += 1
                
            st.success(f"✅ Successfully synced {synced_count} tasks to Google Calendar!")
            
        except Exception as e:
            st.error(f"❌ Sync failed: {str(e)}")

def get_calendar_list():
    """Get list of available Google Calendars"""
    service = get_calendar_service()
    if not service:
        return ["Primary Calendar"]
    
    try:
        calendar_list = service.calendarList().list().execute()
        calendars = []
        
        for calendar in calendar_list.get('items', []):
            if calendar.get('primary'):
                calendars.append("Primary Calendar")
            else:
                calendars.append(calendar.get('summary', 'Unknown Calendar'))
                
        return calendars if calendars else ["Primary Calendar"]
        
    except Exception as e:
        st.error(f"❌ Failed to get calendar list: {str(e)}")
        return ["Primary Calendar"] 