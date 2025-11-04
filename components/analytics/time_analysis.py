import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def render_time_analysis(optimizer):
    """Render time analysis charts and insights"""
    st.markdown("### ⏰ Time Distribution Analysis")
    
    if not optimizer.tasks:
        st.info("📝 **Add tasks to see time analysis!**\n\nOnce you add tasks to the Task Builder, you'll see detailed breakdowns of how you're spending your time.")
        return
    
    # Analyze current tasks
    tasks = optimizer.tasks
    
    # Category distribution
    _render_category_analysis(tasks)
    
    # Priority distribution
    _render_priority_analysis(tasks)

def _render_category_analysis(tasks):
    """Render category time distribution analysis"""
    st.markdown("#### 📊 Time by Category")
    
    category_time = {}
    for task in tasks:
        category = task.get('category', 'Other')
        duration = task.get('duration', 0)
        category_time[category] = category_time.get(category, 0) + duration
    
    if not category_time:
        return
    
    # Create pie chart
    fig, ax = plt.subplots(figsize=(10, 8))
    
    categories = list(category_time.keys())
    durations = list(category_time.values())
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', '#99CCFF']
    
    pie_result = ax.pie(durations, labels=categories, autopct='%1.1f%%', 
                       colors=colors[:len(categories)], startangle=90)
    ax.set_title('Time Distribution by Category', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Category breakdown table
    category_df = pd.DataFrame([
        {
            'Category': cat, 
            'Time (minutes)': time, 
            'Time (hours)': f"{time//60}h {time%60}m",
            'Percentage': f"{(time/sum(durations)*100):.1f}%"
        }
        for cat, time in category_time.items()
    ])
    
    st.dataframe(category_df, use_container_width=True)

def _render_priority_analysis(tasks):
    """Render priority time distribution analysis"""
    st.markdown("#### 🎯 Time by Priority")
    
    priority_time = {}
    for task in tasks:
        priority = task.get('priority', 'medium')
        duration = task.get('duration', 0)
        priority_time[priority] = priority_time.get(priority, 0) + duration
    
    if not priority_time:
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        _render_priority_chart(priority_time)
    
    with col2:
        _render_priority_insights(priority_time)

def _render_priority_chart(priority_time):
    """Render priority distribution bar chart"""
    fig, ax = plt.subplots(figsize=(8, 6))
    
    priorities = list(priority_time.keys())
    durations = list(priority_time.values())
    colors = {'high': '#FF4444', 'medium': '#FFA500', 'low': '#44AA44'}
    bar_colors = [colors.get(p, '#888888') for p in priorities]
    
    bars = ax.bar(priorities, durations, color=bar_colors, alpha=0.8)
    ax.set_title('Time Distribution by Priority', fontweight='bold')
    ax.set_ylabel('Time (minutes)')
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
               f'{int(height)}m', ha='center', va='bottom')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def _render_priority_insights(priority_time):
    """Render priority insights and recommendations"""
    st.markdown("**Priority Insights:**")
    
    total_time = sum(priority_time.values())
    high_pct = (priority_time.get('high', 0) / total_time * 100) if total_time > 0 else 0
    
    if high_pct > 50:
        st.warning("⚠️ Over 50% of your time is on high-priority tasks. Consider balancing with medium-priority items.")
    elif high_pct < 20:
        st.info("💡 Less than 20% of your time is on high-priority tasks. Consider focusing more on important items.")
    else:
        st.success("✅ Good balance of high and medium priority tasks!")
    
    for priority, time in priority_time.items():
        pct = (time / total_time * 100) if total_time > 0 else 0
        st.metric(f"{priority.title()} Priority", f"{pct:.1f}%", f"{time//60}h {time%60}m") 