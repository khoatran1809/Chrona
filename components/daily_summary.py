import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def render_daily_summary(optimized_result):
    """
    Render the daily summary and time breakdown after optimization.
    
    Args:
        optimized_result: The optimization results containing daily_summary
    """
    result = optimized_result
    summary = result["daily_summary"]
    
    # Daily Summary in left column
    with st.container():
        st.subheader("📊 Daily Summary")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Work Time", summary.get("total_work_time", "N/A"))
            st.metric("Sleep Time", summary.get("sleep_time", "N/A"))
        
        with col_b:
            st.metric("Personal Time", summary.get("personal_time", "N/A"))
            st.metric("Meal Time", summary.get("meal_time", "N/A"))
        
        with col_c:
            st.metric("Exercise Time", summary.get("exercise_time", "N/A"))
            score = summary.get('productivity_score', 0)
            st.metric("Productivity Score", f"{score}/100")
    
    # Time breakdown chart in left column
    if all(key in summary for key in ["total_work_time", "personal_time", "sleep_time"]):
        with st.container():
            st.subheader("⏰ Time Breakdown")
            
            # Parse time strings to get hours
            def parse_time(time_str):
                if "hour" in time_str:
                    parts = time_str.split()
                    hours = float(parts[0])  # Use float to handle decimal hours like "7.5"
                    minutes = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
                    return hours + minutes/60
                return 0
            
            work_hours = parse_time(summary.get("total_work_time", "0 hours"))
            personal_hours = parse_time(summary.get("personal_time", "0 hours"))
            sleep_hours = parse_time(summary.get("sleep_time", "8 hours"))
            meal_hours = parse_time(summary.get("meal_time", "2 hours"))
            exercise_hours = parse_time(summary.get("exercise_time", "0.75 hours"))
            
            remaining_hours = 24 - (work_hours + personal_hours + sleep_hours + meal_hours + exercise_hours)
            
            time_data = {
                "Activity": ["Work", "Sleep", "Personal", "Meals", "Exercise", "Free Time"],
                "Hours": [work_hours, sleep_hours, personal_hours, meal_hours, exercise_hours, max(0, remaining_hours)]
            }
            
            time_df = pd.DataFrame(time_data)
            
            # Filter out activities with 0 hours to prevent 0.0% slices
            time_df = time_df[time_df['Hours'] > 0]
            
            # Create matplotlib pie chart with legend instead of direct labels
            plt.style.use('dark_background')
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
                    autotext.set_color('white')
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
                     facecolor='#1a1a1a',
                     edgecolor='white',
                     labelcolor='white')
            
            ax.set_title('Daily Time Distribution', fontsize=18, color='white', fontweight='bold', pad=30)
            
            # Equal aspect ratio ensures that pie is drawn as a circle
            ax.axis('equal')
            
            # Style the plot with better margins
            fig.patch.set_facecolor('#0F0F0F')
            plt.tight_layout(pad=2.0)
            
            # Display the chart
            st.pyplot(fig)
            
            # Clear the figure to free memory
            plt.close(fig)
    
    # Recommendations moved to schedule display area (above chat) 