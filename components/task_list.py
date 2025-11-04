
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def format_duration(minutes):
    """Format minutes into readable duration string"""
    if minutes < 60:
        return f"{minutes} minutes"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if remaining_minutes == 0:
        return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        return f"{hours} hour{'s' if hours > 1 else ''} {remaining_minutes} minute{'s' if remaining_minutes > 1 else ''}"

def render_task_summary(tasks):
    """Render daily summary and time breakdown based on current tasks"""
    if not tasks:
        return
    
    # Calculate task statistics
    total_duration = sum(task.get('duration', 0) for task in tasks)
    total_hours = total_duration / 60
    
    # Essential daily activities (default assumptions)
    sleep_hours = 8
    meal_hours = 2
    exercise_hours = 0.75
    
    # Calculate remaining time
    remaining_hours = 24 - (total_hours + sleep_hours + meal_hours + exercise_hours)
    
    # Create stable containers to prevent jumping
    with st.container():
        st.subheader("📊 Daily Summary")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Work Time", f"{int(total_hours)}h {int((total_hours % 1) * 60)}m")
            st.metric("Sleep Time", f"{sleep_hours}h")
        
        with col_b:
            st.metric("Personal Time", f"{remaining_hours:.1f}h")
            st.metric("Meal Time", f"{meal_hours}h")
        
        with col_c:
            st.metric("Exercise Time", f"{int(exercise_hours * 60)}m")
            # Calculate a basic productivity score based on task distribution
            productivity_score = min(100, int(len(tasks) * 15 + (total_hours * 10)))
            st.metric("Productivity Score", f"{productivity_score}/100")
    
    # Time breakdown chart
    if tasks:
        with st.container():
            st.subheader("⏰ Time Breakdown")
            
            # Prepare data for pie chart
            time_data = {
                "Activity": ["Work", "Sleep", "Personal", "Meals", "Exercise", "Free Time"],
                "Hours": [total_hours, sleep_hours, 2.0, meal_hours, exercise_hours, max(0, remaining_hours)]
            }
            
            time_df = pd.DataFrame(time_data)
            
            # Filter out activities with 0 hours to prevent 0.0% slices
            time_df = time_df[time_df['Hours'] > 0]
            
            # Create matplotlib pie chart with stable key
            chart_key = f"task_breakdown_{len(tasks)}_{int(total_duration)}"
            
            # Create matplotlib pie chart with better text positioning
            plt.style.use('default')  # Use default for better visibility
            fig, ax = plt.subplots(figsize=(10, 8))
            
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
            # Use only the colors we need based on filtered data
            filtered_colors = colors[:len(time_df)]
            
            # Create pie chart with legend instead of direct labels
            pie_result = ax.pie(time_df['Hours'].tolist(), 
                               colors=filtered_colors, 
                               autopct='%1.1f%%', 
                               startangle=90,
                               textprops={'fontsize': 12, 'fontweight': 'bold'},
                               pctdistance=0.75)
            
            # Handle variable return values from pie()
            if len(pie_result) == 3:
                wedges, texts, autotexts = pie_result
                # Enhance percentage text styling
                for autotext in autotexts:
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(12)
            else:
                wedges, texts = pie_result
                autotexts = []
            
            # Create legend instead of direct labels to prevent overlap
            ax.legend(wedges, time_df['Activity'].tolist(),
                     title="Activities",
                     title_fontsize=14,
                     fontsize=12,
                     loc="center left",
                     bbox_to_anchor=(1, 0, 0.5, 1),
                     frameon=True,
                     facecolor='white',
                     edgecolor='gray')
            
            ax.set_title('Daily Time Distribution', fontsize=18, fontweight='bold', pad=30)
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')
            
            # Adjust layout with better margins
            plt.tight_layout(pad=2.0)
            
            # Display the chart
            st.pyplot(fig)
            
            # Clear the figure to free memory
            plt.close(fig)
        
        # Add some recommendations based on current tasks
        st.subheader("💡 Quick Recommendations")
        
        recommendations = []
        if total_hours > 8:
            recommendations.append("Consider breaking down long work sessions with regular breaks")
        if len([t for t in tasks if t.get('priority') == 'high']) > 3:
            recommendations.append("You have many high-priority tasks - consider tackling them in the morning")
        if total_hours < 4:
            recommendations.append("You have light workload today - perfect for deep focus or learning")
        
        # Default recommendations
        if not recommendations:
            recommendations = [
                "Schedule high-priority tasks during your most productive hours",
                "Take regular breaks to maintain focus and productivity",
                "Keep some buffer time for unexpected tasks"
            ]
        
        for rec in recommendations:
            st.info(f"• {rec}")

def render_task_list(tasks):
    """Render list of tasks with editing capabilities"""
    if not tasks:
        st.info("No tasks added yet. Add some tasks to get started!")
        return

    # Special highlight for recently imported tasks
    if st.session_state.get('tasks_just_imported', False):
        st.markdown("### 📋 Current Tasks ✨")
        st.info("👆 These are your imported tasks! You can edit or delete them using the buttons on the right.")
    else:
        st.subheader("📋 Current Tasks")

    # Task statistics
    if tasks:
        total_duration = sum(task.get('duration', 0) for task in tasks)
        high_priority = len([t for t in tasks if t.get('priority') == 'high'])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", len(tasks))
        with col2:
            st.metric("Total Duration", f"{total_duration//60}h {total_duration%60}m")
        with col3:
            st.metric("High Priority", high_priority)

    # Task list with actions
    for i, task in enumerate(tasks):
        try:
            priority_class = f"priority-{task.get('priority', 'medium')}"

            with st.container():
                col1, col2 = st.columns([3.5, 1])

                with col1:
                    # Build the HTML content properly
                    html_content = f"""
                    <div class="task-card {priority_class}">
                        <h4>🎯 {task.get('name', 'Unnamed Task')}</h4>
                        <p><strong>📂 Category:</strong> {task.get('category', 'Unknown')}</p>
                        <p><strong>⚡ Priority:</strong> {task.get('priority', 'medium').title()}</p>
                        <p><strong>⏰ Duration:</strong> {format_duration(task.get('duration', 0))}</p>"""

                    if task.get('deadline'):
                        html_content += f"<p><strong>📅 Deadline:</strong> {task.get('deadline', 'No deadline')}</p>"

                    if task.get('preferred_time') and task.get('preferred_time') != 'No preference':
                        html_content += f"<p><strong>🕐 Preferred Time:</strong> {task.get('preferred_time')}</p>"

                    if task.get('notes') and task.get('notes').strip():
                        html_content += f"<p><strong>📝 Notes:</strong> {task.get('notes')}</p>"

                    html_content += "</div>"

                    st.markdown(html_content, unsafe_allow_html=True)

                with col2:
                    # Action buttons in a vertical layout
                    col_edit, col_delete = st.columns(2)
                    
                    with col_edit:
                        if st.button("✏️", key=f"edit_{i}", help="Edit task", use_container_width=True):
                            # Set task to edit in session state
                            st.session_state.editing_task_index = i
                            st.session_state.editing_task_data = task.copy()
                            st.session_state.show_edit_form = True
                            st.toast("✏️ Edit mode activated", icon="✏️")
                            st.rerun()
                    
                    with col_delete:
                        if st.button("🗑️", key=f"delete_{i}", help="Delete task", use_container_width=True):
                            if 'optimizer' in st.session_state:
                                st.session_state.optimizer.tasks.pop(i)
                                # Use toast for better UX and rerun for smooth update
                                st.toast("🗑️ Task deleted", icon="🗑️")
                                st.rerun()

        except Exception as e:
            st.error(f"Error displaying task {i}: {str(e)}")
    
    # Remove this automatic call - will be placed elsewhere
    # render_task_summary(tasks)
