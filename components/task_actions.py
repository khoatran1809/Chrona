import streamlit as st
import datetime
import json
from components.task_import import render_import_modal

def render_task_actions(optimizer):
    """
    Render the task actions section with clear, export, and import buttons.
    
    Args:
        optimizer: The ScheduleOptimizer instance
    """
    st.markdown("#### 🛠️ Task Actions")
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        # Clear All button - only enabled when there are tasks
        if optimizer.tasks:
            if st.button("🗑️ Clear All", help="Remove all tasks", use_container_width=True):
                if st.session_state.get('confirm_clear', False):
                    # Clear all tasks and reset to original state
                    optimizer.tasks = []
                    st.session_state.confirm_clear = False
                    # Clear optimization results to reset to original state
                    if hasattr(st.session_state, 'optimized_result'):
                        del st.session_state.optimized_result
                    # Use toast instead of success to prevent layout jump
                    st.toast("🗑️ All cleared! Reset to original state", icon="🗑️")
                    # Keep the current tab active
                    st.session_state.tab_index = 0  # Task Builder is index 0
                    st.session_state.active_tab = "Task Builder"
                    st.rerun()
                else:
                    st.session_state.confirm_clear = True
                    st.warning("Click again to confirm")
        else:
            st.button("🗑️ Clear All", help="No tasks to clear", use_container_width=True, disabled=True)
            
    with col_b:
        # Export tasks as JSON - only enabled when there are tasks
        if optimizer.tasks:
            if st.button("📤 Export", use_container_width=True):
                tasks_json = json.dumps(optimizer.tasks, indent=2)
                st.download_button(
                    label="Download JSON",
                    data=tasks_json,
                    file_name=f"tasks_{datetime.date.today()}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.button("📤 Export", help="No tasks to export", use_container_width=True, disabled=True)
        
    with col_c:
        # Import tasks from JSON
        if st.button("📥 Import", use_container_width=True, help="Import tasks from JSON file or paste JSON content"):
            st.session_state.show_import_modal = True
        
        # Import modal/expander
        if st.session_state.get('show_import_modal', False):
            with st.expander("📥 Import Tasks", expanded=True):
                render_import_modal(optimizer) 