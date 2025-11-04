import streamlit as st
import json
import re

def render_schedule_upload(optimizer):
    """
    Render the Schedule Upload tab with file upload and AI analysis functionality.
    
    Args:
        optimizer: The ScheduleOptimizer instance
    """
    # Schedule Upload functionality
    st.markdown("### 📄 Upload Existing Schedule")
    st.markdown("Upload your existing schedule and let AI understand and optimize it!")
    
    col_upload, col_preview = st.columns([1, 1])
    
    with col_upload:
        st.markdown("#### 📤 Upload Schedule")
        
        # Upload method selection
        upload_method = st.radio(
            "Choose upload method:",
            ["📄 Upload Schedule File", "📝 Paste Schedule Text"],
            key="schedule_upload_method"
        )
        
        schedule_content = ""
        
        if upload_method == "📄 Upload Schedule File":
            uploaded_schedule = st.file_uploader(
                "Upload your schedule file",
                type=['txt', 'csv', 'json', 'md'],
                help="Supports text files, CSV, JSON, or Markdown formats",
                key="schedule_file_upload"
            )
            
            if uploaded_schedule is not None:
                try:
                    schedule_content = uploaded_schedule.read().decode('utf-8')
                    st.success(f"✅ File uploaded: {uploaded_schedule.name}")
                except Exception as e:
                    st.error(f"❌ Error reading file: {str(e)}")
                    
        elif upload_method == "📝 Paste Schedule Text":
            schedule_content = st.text_area(
                "Paste your existing schedule here:",
                height=250,
                placeholder="""Example formats:
                
9:00-10:00 Morning Meeting
10:00-11:00 Project Work
11:00-12:00 Email Review
...

Or:
Time,Activity,Duration
09:00,Morning Meeting,60
10:00,Project Work,60
...

Or any text format describing your schedule!""",
                key="schedule_text_paste"
            )
    
    with col_preview:
        st.markdown("#### 🔍 AI Analysis")
        
        if schedule_content.strip():
            # Show preview of uploaded content
            with st.expander("📋 Uploaded Content Preview", expanded=True):
                lines = schedule_content.split('\n')[:10]  # Show first 10 lines
                for line in lines:
                    if line.strip():
                        st.text(line)
                if len(schedule_content.split('\n')) > 10:
                    st.text(f"... and {len(schedule_content.split('\n')) - 10} more lines")
            
            # AI Analysis button
            if st.button("🤖 Analyze & Convert Schedule", type="primary", use_container_width=True):
                if st.session_state.get('api_initialized', False):
                    with st.spinner("🤖 AI is analyzing your schedule..."):
                        result = _analyze_schedule_with_ai(schedule_content, optimizer)
                        
                        if result.get('success', False):
                            st.success(f"✅ AI successfully analyzed your schedule!")
                            st.success(f"🎯 Found {len(result['tasks'])} tasks")
                            
                            # Store parsed tasks in session state for preview
                            st.session_state.parsed_schedule_tasks = result['tasks']
                        else:
                            st.error(f"❌ {result.get('error', 'Unknown error occurred')}")
                else:
                    st.error("🔴 API key required for AI analysis")
        else:
            st.info("📝 Upload or paste your schedule content to see AI analysis")
    
    # Show parsed tasks and import option
    if 'parsed_schedule_tasks' in st.session_state:
        st.markdown("---")
        st.markdown("### 🎯 Parsed Tasks")
        
        col_tasks, col_actions = st.columns([2, 1])
        
        with col_tasks:
            # Display parsed tasks in a nice format
            for i, task in enumerate(st.session_state.parsed_schedule_tasks[:8]):  # Show first 8
                priority_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(task.get('priority', 'medium'), "⚪")
                category_icon = {
                    "work": "💼", "personal": "👤", "health": "💪", 
                    "education": "📚", "social": "👥", "other": "📝"
                }.get(task.get('category', 'other'), "📝")
                
                st.markdown(f"""
                **{i+1}. {task.get('name', 'Unnamed Task')}**  
                {priority_icon} {task.get('priority', 'medium').title()} • {category_icon} {task.get('category', 'other').title()} • ⏰ {task.get('duration', 0)} min  
                *{task.get('notes', 'No notes')}*
                """)
            
            if len(st.session_state.parsed_schedule_tasks) > 8:
                st.info(f"... and {len(st.session_state.parsed_schedule_tasks) - 8} more tasks")
        
        with col_actions:
            st.markdown("#### 🚀 Import Tasks")
            
            if st.button("✅ Import All Tasks", type="primary", use_container_width=True):
                # Clear existing tasks first
                optimizer.tasks = []
                
                # Import all parsed tasks
                for task in st.session_state.parsed_schedule_tasks:
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
                    
                    # Validate and clean the task
                    clean_task = {
                        'name': task.get('name', 'Imported Task'),
                        'duration': max(15, int(task.get('duration', 60))),
                        'priority': normalized_priority,
                        'category': normalized_category,
                        'notes': task.get('notes', ''),
                        'deadline': task.get('deadline', None),
                        'preferred_time': task.get('preferred_time', 'No preference')
                    }
                    optimizer.add_task(clean_task)
                
                # Clear parsed tasks and switch to Task Builder
                del st.session_state.parsed_schedule_tasks
                st.success(f"✅ Imported {len(optimizer.tasks)} tasks!")
                st.info("🔄 Switching to Task Builder to view your imported tasks...")
                
                # Clear any existing optimization results
                if hasattr(st.session_state, 'optimized_result'):
                    del st.session_state.optimized_result
                
                # Switch to Task Builder tab and focus on Task Management
                st.session_state.tab_index = 0  # Task Builder is index 0
                st.session_state.active_tab = "Task Builder"
                st.session_state.tasks_just_imported = True
                
                st.rerun()
            
            if st.button("🗑️ Clear Analysis", use_container_width=True):
                del st.session_state.parsed_schedule_tasks
                # Keep the current tab active
                st.session_state.active_tab = "Schedule Upload"
                st.rerun()
            
            st.markdown("---")
            st.markdown("**💡 Tips:**")
            st.markdown("• Import tasks and switch to Task Builder")
            st.markdown("• Use AI optimization features")  
            st.markdown("• Chat to modify schedule")

def _analyze_schedule_with_ai(schedule_content, optimizer):
    """
    Analyze schedule content using AI to extract tasks.
    
    Args:
        schedule_content: The uploaded schedule content
        optimizer: The ScheduleOptimizer instance
        
    Returns:
        dict: Result containing success status and tasks or error message
    """
    # Generate AI prompt to parse the schedule
    analysis_prompt = f"""
    You are Chrona AI, an expert schedule analyzer. Your task is to parse the uploaded schedule and convert it to our standard task format.

    UPLOADED SCHEDULE CONTENT:
    {schedule_content}

    CONVERSION RULES:
    1. Extract each activity/task from the schedule
    2. Determine duration (in minutes) for each task
    3. Assign appropriate priority (high/medium/low) based on context
    4. Categorize tasks (work/personal/health/education/social/other)
    5. Extract any time preferences or constraints
    6. Add relevant notes based on context

    OUTPUT FORMAT:
    Return ONLY valid JSON array with tasks in this exact format:
    [
        {{
            "name": "Task name",
            "duration": 60,
            "priority": "medium",
            "category": "work",
            "notes": "Any relevant details",
            "preferred_time": "Morning" or specific time if mentioned,
            "deadline": null or "YYYY-MM-DD" if deadline mentioned
        }}
    ]

    ANALYSIS GUIDELINES:
    - Meetings/calls → high priority, work category
    - Exercise/gym → medium priority, health category  
    - Personal time → low priority, personal category
    - Study/learning → high priority, education category
    - Meals → medium priority, personal category
    - Creative work → high priority, work category
    - Administrative tasks → low priority, work category

    Parse ALL identifiable tasks from the schedule content above.
    """
    
    try:
        # Use the existing AI client to analyze the schedule
        if optimizer.client is None:
            return {"success": False, "error": "AI client not properly initialized"}
            
        response = optimizer.client.models.generate_content(
            model='gemini-2.0-flash-exp', 
            contents=analysis_prompt
        )
        
        response_text = response.text if response.text else ""
        
        # Extract JSON from response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        
        if json_match:
            json_str = json_match.group()
            parsed_tasks = json.loads(json_str)
            
            if isinstance(parsed_tasks, list) and len(parsed_tasks) > 0:
                return {"success": True, "tasks": parsed_tasks}
            else:
                return {"success": False, "error": "No valid tasks found in schedule"}
        else:
            return {"success": False, "error": "AI could not parse the schedule format"}
            
    except Exception as e:
        return {"success": False, "error": f"Error analyzing schedule: {str(e)}"} 