import streamlit as st
import json

def render_import_modal(optimizer):
    """
    Render the import modal for JSON tasks.
    
    Args:
        optimizer: The ScheduleOptimizer instance
    """
    st.markdown("**Choose import method:**")
    
    # Tab-like interface using radio buttons
    import_method = st.radio(
        "Import method:",
        ["Upload JSON File", "Paste JSON Content"],
        key="import_method"
    )
    
    imported_tasks = []
    
    if import_method == "Upload JSON File":
        uploaded_file = st.file_uploader(
            "Choose a JSON file",
            type=['json'],
            key="json_file_upload"
        )
        
        if uploaded_file is not None:
            try:
                # Read the file content
                content = uploaded_file.read().decode('utf-8')
                imported_tasks = json.loads(content)
                
                if isinstance(imported_tasks, list):
                    st.success(f"✅ Found {len(imported_tasks)} tasks in file")
                    
                    # Preview tasks
                    with st.expander("📋 Preview tasks", expanded=True):
                        for i, task in enumerate(imported_tasks[:5]):  # Show first 5
                            st.write(f"**{i+1}.** {task.get('name', 'Unnamed')} - {task.get('duration', 0)} min - {task.get('priority', 'medium')}")
                        if len(imported_tasks) > 5:
                            st.write(f"... and {len(imported_tasks) - 5} more tasks")
                else:
                    st.error("❌ JSON file should contain an array of tasks")
                    imported_tasks = []
                    
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON format: {str(e)}")
                imported_tasks = []
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
                imported_tasks = []
    
    elif import_method == "Paste JSON Content":
        json_content = st.text_area(
            "Paste your JSON content here:",
            height=200,
            placeholder='[{"name": "Task 1", "duration": 60, "priority": "high", "category": "work", "notes": "Important task"}]',
            key="json_paste_content"
        )
        
        if json_content.strip():
            try:
                imported_tasks = json.loads(json_content)
                
                if isinstance(imported_tasks, list):
                    st.success(f"✅ Found {len(imported_tasks)} tasks in JSON")
                    
                    # Preview tasks
                    with st.expander("📋 Preview tasks", expanded=True):
                        for i, task in enumerate(imported_tasks[:5]):  # Show first 5
                            st.write(f"**{i+1}.** {task.get('name', 'Unnamed')} - {task.get('duration', 0)} min - {task.get('priority', 'medium')}")
                        if len(imported_tasks) > 5:
                            st.write(f"... and {len(imported_tasks) - 5} more tasks")
                else:
                    st.error("❌ JSON should contain an array of tasks")
                    imported_tasks = []
                    
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON format: {str(e)}")
                imported_tasks = []
            except Exception as e:
                st.error(f"❌ Error parsing JSON: {str(e)}")
                imported_tasks = []
    
    # Action buttons
    if imported_tasks:
        col_import, col_cancel = st.columns(2)
        
        with col_import:
            if st.button("✅ Import Tasks", type="primary", use_container_width=True):
                # Validate and clean imported tasks
                valid_tasks = []
                for task in imported_tasks:
                    # Ensure required fields
                    if isinstance(task, dict) and task.get('name'):
                        # Normalize category (case-insensitive matching)
                        raw_category = task.get('category', 'work')
                        category_options = ["Work", "Personal", "Health", "Learning", "Other"]
                        normalized_category = "Work"  # Default
                        for option in category_options:
                            if option.lower() == raw_category.lower():
                                normalized_category = option
                                break
                        
                        # Normalize priority (case-insensitive matching)
                        raw_priority = task.get('priority', 'medium')
                        priority_options = ["high", "medium", "low"]
                        normalized_priority = "medium"  # Default
                        for option in priority_options:
                            if option.lower() == raw_priority.lower():
                                normalized_priority = option
                                break
                        
                        clean_task = {
                            'name': task.get('name', 'Imported Task'),
                            'duration': max(15, int(task.get('duration', 60))),  # Minimum 15 minutes
                            'priority': normalized_priority,
                            'category': normalized_category,
                            'notes': task.get('notes', ''),
                            'deadline': task.get('deadline', None),
                            'preferred_time': task.get('preferred_time', 'No preference')
                        }
                        valid_tasks.append(clean_task)
                
                if valid_tasks:
                    # Add tasks to optimizer
                    for task in valid_tasks:
                        optimizer.add_task(task)
                    
                    st.session_state.show_import_modal = False
                    st.toast(f"✅ Successfully imported {len(valid_tasks)} tasks!", icon="✅")
                    # Keep the current tab active
                    st.session_state.tab_index = 0  # Task Builder is index 0
                    st.session_state.active_tab = "Task Builder"
                    st.rerun()
                else:
                    st.error("❌ No valid tasks found to import")
        
        with col_cancel:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.show_import_modal = False
                # Keep the current tab active
                st.session_state.tab_index = 0  # Task Builder is index 0
                st.session_state.active_tab = "Task Builder"
                st.rerun()
    else:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.show_import_modal = False
            # Keep the current tab active
            st.session_state.tab_index = 0  # Task Builder is index 0
            st.session_state.active_tab = "Task Builder"
            st.rerun() 