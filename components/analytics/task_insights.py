import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

from .data_manager import clear_analytics_data

def render_task_insights(optimizer):
    """Render task-specific insights and analysis"""
    st.markdown("### 📋 Task Analysis & Recommendations")
    
    if not optimizer.tasks:
        st.info("📝 **Add tasks to see insights!**\n\nOnce you have tasks, you'll see patterns in your task creation habits and get recommendations for better productivity.")
        return
    
    tasks = optimizer.tasks
    
    # Task patterns
    col1, col2 = st.columns(2)
    
    with col1:
        _render_task_patterns(tasks)
    
    with col2:
        _render_recommendations(tasks)
    
    # Task details and export
    _render_task_details(tasks)

def _render_task_patterns(tasks):
    """Render task patterns analysis"""
    st.markdown("#### 📊 Task Patterns")
    
    # Duration analysis
    durations = [task.get('duration', 0) for task in tasks]
    avg_duration = np.mean(durations)
    
    st.metric("Average Task Duration", f"{avg_duration:.0f} minutes")
    st.metric("Shortest Task", f"{min(durations)} minutes")
    st.metric("Longest Task", f"{max(durations)} minutes")
    
    # Duration distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(durations, bins=8, alpha=0.7, color='#9C27B0', edgecolor='black')
    ax.set_title('Task Duration Distribution', fontweight='bold')
    ax.set_xlabel('Duration (minutes)')
    ax.set_ylabel('Number of Tasks')
    ax.axvline(float(avg_duration), color='red', linestyle='--', label=f'Average: {avg_duration:.0f}m')
    ax.legend()
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def _render_recommendations(tasks):
    """Render smart recommendations based on task patterns"""
    st.markdown("#### 💡 Smart Recommendations")
    
    # Generate recommendations based on task patterns
    recommendations = _generate_recommendations(tasks)
    
    for rec in recommendations:
        st.info(rec)
    
    # Task completion suggestions
    st.markdown("#### 🎯 Optimization Tips")
    
    tips = [
        "🌅 Schedule high-priority tasks during your peak energy hours",
        "⏰ Add buffer time between tasks for transitions",
        "📅 Group similar tasks together for better focus",
        "🔄 Review and adjust your schedule based on actual completion times"
    ]
    
    for tip in tips:
        st.success(tip)

def _generate_recommendations(tasks):
    """Generate smart recommendations based on task analysis"""
    recommendations = []
    
    # Calculate metrics for recommendations
    durations = [task.get('duration', 0) for task in tasks]
    avg_duration = np.mean(durations)
    
    # Long task recommendation
    if avg_duration > 120:
        recommendations.append("🔧 Consider breaking tasks longer than 2 hours into smaller chunks")
    
    # Priority balance recommendation
    high_priority_count = len([t for t in tasks if t.get('priority') == 'high'])
    if high_priority_count > len(tasks) * 0.6:
        recommendations.append("⚖️ Too many high-priority tasks - consider redistributing priorities")
    
    # Category diversity recommendation
    category_counts = {}
    for task in tasks:
        cat = task.get('category', 'Other')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    if len(category_counts) == 1:
        recommendations.append("🌈 Consider diversifying task categories for better work-life balance")
    
    # Short task batching recommendation
    short_tasks = len([t for t in tasks if t.get('duration', 0) < 30])
    if short_tasks > len(tasks) * 0.4:
        recommendations.append("⚡ Many short tasks detected - consider batching similar quick tasks")
    
    # Default recommendation if no issues found
    if not recommendations:
        recommendations.append("✅ Your task structure looks well-balanced!")
    
    return recommendations

def _render_task_details(tasks):
    """Render task details table and export options"""
    st.markdown("#### 📈 Current Tasks Overview")
    
    if not tasks:
        return
    
    # Create task details dataframe
    task_df = pd.DataFrame([
        {
            'Task': task.get('name', 'Unnamed'),
            'Category': task.get('category', 'Other'),
            'Priority': task.get('priority', 'medium'),
            'Duration': f"{task.get('duration', 0)} min",
            'Notes': task.get('notes', '')[:50] + ('...' if len(task.get('notes', '')) > 50 else '')
        }
        for task in tasks
    ])
    
    st.dataframe(task_df, use_container_width=True)
    
    # Export and management options
    _render_export_options(task_df)

def _render_export_options(task_df):
    """Render export and data management options"""
    st.markdown("#### 📥 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export CSV
        csv_data = task_df.to_csv(index=False)
        st.download_button(
            label="📊 Download Task Data (CSV)",
            data=csv_data,
            file_name=f"chrona_tasks_{datetime.date.today()}.csv",
            mime="text/csv"
        )
    
    with col2:
        # Clear analytics history
        if st.button("🗑️ Clear Analytics History"):
            clear_analytics_data()
            st.success("Analytics history cleared!")
            st.rerun() 