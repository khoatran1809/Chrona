import streamlit as st
from ui_components import render_task_list
from components.task_form import render_task_form, render_edit_task_form
from components.task_actions import render_task_actions
from components.daily_summary import render_daily_summary
from components.schedule_optimization import render_schedule_optimization

def render_task_builder(optimizer, preferences):
    """
    Render the Task Builder tab with all task management functionality.
    
    Args:
        optimizer: The ScheduleOptimizer instance
        preferences: User preferences from sidebar
    """
    # Main content layout
    col1, col2 = st.columns([1.2, 1], gap="large")

    # Left column: Task management
    with col1:
        # Special highlight for recently imported tasks
        if st.session_state.get('tasks_just_imported', False):
            st.markdown('<div id="task-builder-top"></div>', unsafe_allow_html=True)
            st.markdown("### 📝 Task Management")
            st.success("🎉 Tasks imported successfully! Your imported tasks are shown below.")
            
            # Add scroll behavior to jump to the top of Task Builder
            st.markdown("""
            <script>
            setTimeout(function() {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }, 100);
            </script>
            """, unsafe_allow_html=True)
            
            st.session_state.tasks_just_imported = False
        else:
            st.markdown('<div id="task-builder-top"></div>', unsafe_allow_html=True)
            st.markdown("### 📝 Task Management")

        # Check if we're in edit mode
        if st.session_state.get('show_edit_form', False) and st.session_state.get('editing_task_index') is not None:
            # Show edit form
            task_index = st.session_state.editing_task_index
            task_data = st.session_state.editing_task_data
            render_edit_task_form(task_index, task_data)
        else:
            # Show regular add task form
            form_expanded = not optimizer.tasks and not st.session_state.get('task_just_added', False)
            
            with st.expander("➕ Add New Task", expanded=form_expanded):
                task_data = render_task_form(len(optimizer.tasks))

                if task_data:
                    # Check for duplicate task names
                    existing_names = [task.get('name', '').lower() for task in optimizer.tasks]
                    if task_data['name'].lower() in existing_names:
                        st.warning("⚠️ A task with this name already exists!")
                    else:
                        optimizer.add_task(task_data)
                        st.session_state.task_just_added = True
                        # Use toast instead of success to prevent layout jump
                        st.toast("✅ Task added successfully!", icon="✅")
                        # Keep the current tab active
                        st.session_state.active_tab = "Task Builder"
                        # Add rerun to ensure smooth UI update
                        st.rerun()
        
        # Reset the flag after form rendering
        if st.session_state.get('task_just_added', False):
            st.session_state.task_just_added = False

        # Render task list
        render_task_list(optimizer.tasks)

        # Render task actions (clear, export, import)
        render_task_actions(optimizer)

        # Add Daily Summary and Time Breakdown to left column ONLY after optimization
        if hasattr(st.session_state, 'optimized_result') and "daily_summary" in st.session_state.optimized_result:
            render_daily_summary(st.session_state.optimized_result)

    # Right column: Schedule optimization
    with col2:
        render_schedule_optimization(optimizer, preferences) 