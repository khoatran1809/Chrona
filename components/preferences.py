
import streamlit as st

def render_preferences_sidebar():
    """Render user preferences sidebar with improved layout"""
    with st.sidebar:
        # User preferences section
        st.markdown("### 👤 Preferences")
        
        with st.container():
            st.markdown("**📅 Schedule Duration**")
            schedule_duration = st.selectbox(
                "Create schedule for",
                [
                    "1 day (Single day)",
                    "2 days (Weekend)", 
                    "3 days (Long weekend)",
                    "5 days (Workweek)",
                    "7 days (Full week)",
                    "14 days (Two weeks)"
                ],
                index=0,
                help="Choose how many days to schedule. Each day will be planned separately."
            )
            
            st.markdown("**⏰ Productivity Settings**")
            peak_hours = st.selectbox(
                "Most productive hours",
                ["Morning (6-12)", "Afternoon (12-18)", "Evening (18-22)"],
                help="When do you feel most productive?"
            )

            break_time = st.selectbox(
                "Preferred break duration",
                ["15 minutes", "30 minutes", "45 minutes", "60 minutes"],
                index=1,
                help="How long should breaks be between tasks?"
            )

        st.markdown("**🎯 Work Style**")
        work_type = st.selectbox(
            "Work priority style", 
            [
                "Important tasks first",
                "Urgent tasks first", 
                "Quick wins first",
                "Creative work first"
            ],
            help="How should tasks be prioritized?"
        )

        flexibility = st.slider(
            "Schedule flexibility", 
            1, 5, 3,
            help="1 = Strict schedule, 5 = Very flexible"
        )
        
        st.markdown("---")
        
        # Statistics section if tasks exist
        if 'optimizer' in st.session_state and st.session_state.optimizer.tasks:
            st.markdown("### 📊 Quick Stats")
            
            tasks = st.session_state.optimizer.tasks
            categories = {}
            priorities = {"high": 0, "medium": 0, "low": 0}
            
            for task in tasks:
                cat = task.get('category', 'Other')
                categories[cat] = categories.get(cat, 0) + 1
                priorities[task.get('priority', 'medium')] += 1
            
            st.markdown("**📂 By Category**")
            for cat, count in categories.items():
                st.write(f"• {cat}: {count}")
            
            st.markdown("**⚡ By Priority**")
            for priority, count in priorities.items():
                emoji = "🔴" if priority == "high" else "🟡" if priority == "medium" else "🟢"
                st.write(f"• {emoji} {priority.title()}: {count}")

        return {
            'schedule_duration': schedule_duration,
            'peak_hours': peak_hours,
            'break_time': break_time,
            'work_type': work_type,
            'flexibility': flexibility
        }
