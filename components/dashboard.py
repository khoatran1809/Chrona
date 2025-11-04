import streamlit as st

def render_dashboard_overview(optimizer):
    """
    Render the dashboard overview section with task statistics and metrics.
    
    Args:
        optimizer: The ScheduleOptimizer instance containing tasks
    """
    st.markdown("### 📊 Dashboard Overview")
    
    # Enhanced stats section with progress indicators
    if optimizer.tasks:
        col1, col2, col3, col4 = st.columns(4)
        
        total_tasks = len(optimizer.tasks)
        total_duration = sum(task.get('duration', 0) for task in optimizer.tasks)
        high_priority = len([t for t in optimizer.tasks if t.get('priority') == 'high'])
        pending_deadlines = len([t for t in optimizer.tasks if t.get('deadline')])
        
        # Calculate completion rate (assuming tasks without deadlines are in progress)
        completion_rate = min(100, (total_tasks * 15)) if total_tasks > 0 else 0
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📋</h3>
                <h2>{total_tasks}</h2>
                <p>Total Tasks</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(100, total_tasks * 10)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⏱️</h3>
                <h2>{total_duration//60}h {total_duration%60}m</h2>
                <p>Total Time</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {min(100, (total_duration / 480) * 100)}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            priority_percentage = (high_priority / total_tasks * 100) if total_tasks > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>🚨</h3>
                <h2>{high_priority}</h2>
                <p>High Priority</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {priority_percentage}%; background: linear-gradient(90deg, #ff4444, #ff6b6b);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            deadline_percentage = (pending_deadlines / total_tasks * 100) if total_tasks > 0 else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>📅</h3>
                <h2>{pending_deadlines}</h2>
                <p>With Deadlines</p>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {deadline_percentage}%; background: linear-gradient(90deg, #ffa726, #ff9800);"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---") 