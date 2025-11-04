import streamlit as st
import datetime
import re

def parse_duration(duration_str):
    """Parse duration string like '1h30m', '45m', '2h' into total minutes"""
    if not duration_str or not duration_str.strip():
        return None

    duration_str = duration_str.strip().lower()

    # Remove spaces
    duration_str = duration_str.replace(' ', '')

    # Pattern to match hours and minutes
    pattern = r'(?:(\d+)h)?(?:(\d+)m)?'
    match = re.match(pattern, duration_str)

    if not match:
        return None

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0

    # If no h or m specified, assume it's minutes
    if not match.group(1) and not match.group(2):
        # Try to parse as just a number (assume minutes)
        try:
            minutes = int(duration_str)
        except ValueError:
            return None

    total_minutes = hours * 60 + minutes

    # Validate range (15 minutes to 8 hours)
    if total_minutes < 15 or total_minutes > 480:
        return None

    return total_minutes

def format_duration_input(minutes):
    """Convert minutes back to duration string format for the input field"""
    if not minutes:
        return "1h"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if hours == 0:
        return f"{remaining_minutes}m"
    elif remaining_minutes == 0:
        return f"{hours}h"
    else:
        return f"{hours}h{remaining_minutes}m"

def render_task_form(form_counter):
    """Render task input form with validation"""
    with st.form(f"task_form_{form_counter}", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Task Name", placeholder="e.g., Complete project report")
            category = st.selectbox("Category", 
                                   ["Work", "Personal", "Health", "Learning", "Other"])

        with col2:
            priority = st.selectbox("Priority", ["high", "medium", "low"])
            duration_input = st.text_input("Duration", value="1h", placeholder="e.g., 30m, 1h, 2h30m", help="Format: 30m (minutes), 1h (hour), 2h30m (2 hours 30 minutes)")

        # Enhanced optional fields
        col3, col4 = st.columns(2)
        with col3:
            deadline = st.date_input("Deadline (optional)", value=None, min_value=datetime.date.today())
        with col4:
            preferred_time = st.selectbox("Preferred Time", 
                                        ["No preference", "Morning (6-12)", "Afternoon (12-18)", "Evening (18-22)"])

        notes = st.text_area("Notes (optional)", placeholder="Any additional details...")

        submitted = st.form_submit_button("➕ Add Task")

        if submitted:
            # Enhanced validation
            if not name or not name.strip():
                st.error("⚠️ Task name is required!")
                return None

            if len(name.strip()) > 100:
                st.error("⚠️ Task name must be less than 100 characters!")
                return None

            # Parse duration
            duration = parse_duration(duration_input)
            if duration is None:
                st.error("⚠️ Invalid duration format! Use formats like: 30m, 1h, 1h30m (15 minutes to 8 hours)")
                return None

            return {
                'id': f"task_{datetime.datetime.now().timestamp()}",
                'name': name.strip(),
                'category': category,
                'priority': priority,
                'duration': duration,
                'deadline': deadline.isoformat() if deadline else None,
                'preferred_time': preferred_time,
                'notes': notes.strip() if notes else "",
                'created_at': datetime.datetime.now().isoformat()
            }

    return None

def render_edit_task_form(task_index, task_data):
    """Render task edit form with pre-filled values"""
    st.markdown("### ✏️ Edit Task")
    
    # Parse deadline if it exists
    deadline_value = None
    if task_data.get('deadline'):
        try:
            deadline_value = datetime.datetime.fromisoformat(task_data['deadline']).date()
        except:
            deadline_value = None
    
    with st.form(f"edit_task_form_{task_index}", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Task Name", value=task_data.get('name', ''), placeholder="e.g., Complete project report")
            
            # Handle case-insensitive category matching for CSV imports
            category_options = ["Work", "Personal", "Health", "Learning", "Other"]
            current_category = task_data.get('category', 'Work')
            
            # Find matching category (case-insensitive)
            category_index = 0  # Default to "Work"
            for i, option in enumerate(category_options):
                if option.lower() == current_category.lower():
                    category_index = i
                    break
            
            category = st.selectbox("Category", category_options, index=category_index)

        with col2:
            priority_options = ["high", "medium", "low"]
            current_priority = task_data.get('priority', 'medium')
            
            # Handle case-insensitive priority matching
            priority_index = 1  # Default to "medium"
            for i, option in enumerate(priority_options):
                if option.lower() == current_priority.lower():
                    priority_index = i
                    break
            
            priority = st.selectbox("Priority", priority_options, index=priority_index)
            
            duration_input = st.text_input("Duration", 
                                         value=format_duration_input(task_data.get('duration', 60)), 
                                         placeholder="e.g., 30m, 1h, 2h30m", 
                                         help="Format: 30m (minutes), 1h (hour), 2h30m (2 hours 30 minutes)")

        # Enhanced optional fields
        col3, col4 = st.columns(2)
        with col3:
            deadline = st.date_input("Deadline (optional)", value=deadline_value, min_value=datetime.date.today())
        with col4:
            time_options = ["No preference", "Morning (6-12)", "Afternoon (12-18)", "Evening (18-22)"]
            time_index = 0
            if task_data.get('preferred_time') and task_data.get('preferred_time') in time_options:
                time_index = time_options.index(task_data.get('preferred_time'))
            preferred_time = st.selectbox("Preferred Time", time_options, index=time_index)

        notes = st.text_area("Notes (optional)", value=task_data.get('notes', ''), placeholder="Any additional details...")

        col_save, col_cancel = st.columns(2)
        
        with col_save:
            submitted = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
        
        with col_cancel:
            cancelled = st.form_submit_button("❌ Cancel", use_container_width=True)

        if cancelled:
            # Clear edit state
            if 'editing_task_index' in st.session_state:
                del st.session_state.editing_task_index
            if 'editing_task_data' in st.session_state:
                del st.session_state.editing_task_data
            if 'show_edit_form' in st.session_state:
                del st.session_state.show_edit_form
            st.toast("❌ Edit cancelled", icon="❌")
            st.rerun()

        if submitted:
            # Enhanced validation
            if not name or not name.strip():
                st.error("⚠️ Task name is required!")
                return None

            if len(name.strip()) > 100:
                st.error("⚠️ Task name must be less than 100 characters!")
                return None

            # Parse duration
            duration = parse_duration(duration_input)
            if duration is None:
                st.error("⚠️ Invalid duration format! Use formats like: 30m, 1h, 1h30m (15 minutes to 8 hours)")
                return None

            # Create updated task data
            updated_task = {
                'id': task_data.get('id', f"task_{datetime.datetime.now().timestamp()}"),
                'name': name.strip(),
                'category': category,
                'priority': priority,
                'duration': duration,
                'deadline': deadline.isoformat() if deadline else None,
                'preferred_time': preferred_time,
                'notes': notes.strip() if notes else "",
                'created_at': task_data.get('created_at', datetime.datetime.now().isoformat()),
                'modified_at': datetime.datetime.now().isoformat()
            }

            # Update the task in the optimizer
            if 'optimizer' in st.session_state and 0 <= task_index < len(st.session_state.optimizer.tasks):
                st.session_state.optimizer.tasks[task_index] = updated_task
                
                # Clear edit state
                if 'editing_task_index' in st.session_state:
                    del st.session_state.editing_task_index
                if 'editing_task_data' in st.session_state:
                    del st.session_state.editing_task_data
                if 'show_edit_form' in st.session_state:
                    del st.session_state.show_edit_form
                
                st.toast("💾 Task updated successfully!", icon="💾")
                st.rerun()

    return None