import streamlit as st
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
from .schedule_themes import get_theme_color

def render_enhanced_chart(schedule_df, day_index, chart_style, show_priorities, day_theme):
    """Render enhanced chart with dynamic updates"""
    
    # Check task count limit
    if len(schedule_df) > 25:
        st.error(f"🚫 Too many tasks ({len(schedule_df)}) for chart display. Maximum allowed: 25")
        st.info("💡 Use filtering options above to reduce the number of tasks")
        return
    
    try:
        # Force close any existing figures
        plt.close('all')
        
        # Clean the time data
        schedule_df_clean = schedule_df.copy()
        
        if schedule_df_clean.empty:
            st.warning("No schedule data available for chart.")
            return
        
        # Fix time formats
        for idx, row in schedule_df_clean.iterrows():
            start_time = str(row['start_time'])
            end_time = str(row['end_time'])
            
            if start_time == '24:00':
                schedule_df_clean.loc[idx, 'start_time'] = '00:00'
            if end_time == '24:00':
                schedule_df_clean.loc[idx, 'end_time'] = '00:00'
        
        # Convert to datetime
        today = datetime.date.today()
        schedule_df_clean['start_datetime'] = schedule_df_clean['start_time'].apply(
            lambda x: datetime.datetime.combine(today, datetime.datetime.strptime(x, '%H:%M').time())
        )
        schedule_df_clean['end_datetime'] = schedule_df_clean['end_time'].apply(
            lambda x: datetime.datetime.combine(today, datetime.datetime.strptime(x, '%H:%M').time())
        )
        
        # Sort by start time
        schedule_df_clean = schedule_df_clean.sort_values('start_datetime')
        
        # Set up matplotlib with theme colors
        plt.style.use('dark_background')
        
        # Priority color mapping
        if show_priorities:
            priority_colors = {
                "high": "#FF3030",
                "medium": "#FFA500",
                "low": "#32CD32",
                "essential": "#1E90FF",
                "critical": "#8A2BE2"
            }
        else:
            # Use theme color
            theme_color = get_theme_color(day_theme)
            priority_colors = {
                "high": theme_color,
                "medium": theme_color,
                "low": theme_color,
                "essential": theme_color,
                "critical": theme_color
            }
        
        # Create chart based on style
        if chart_style == "Bar Chart":
            render_bar_chart(schedule_df_clean, priority_colors, day_theme)
        elif chart_style == "Compact":
            render_compact_chart(schedule_df_clean, priority_colors, day_theme)
        else:  # Timeline
            render_timeline_chart(schedule_df_clean, priority_colors, day_theme)
        
    except Exception as e:
        plt.close('all')
        st.error(f"Chart error: {str(e)}")
        st.info("📊 Chart temporarily unavailable - use the table view above")

def render_bar_chart(schedule_df_clean, priority_colors, day_theme):
    """Render horizontal bar chart"""
    schedule_df_clean['duration_hours'] = (
        schedule_df_clean['end_datetime'] - schedule_df_clean['start_datetime']
    ).dt.total_seconds() / 3600
    
    fig, ax = plt.subplots(figsize=(12, max(6, len(schedule_df_clean) * 0.5)), dpi=80)
    
    y_positions = range(len(schedule_df_clean))
    colors = [priority_colors.get(str(priority), '#777777') for priority in schedule_df_clean['priority']]
    
    bars = ax.barh(y_positions, schedule_df_clean['duration_hours'], 
                  color=colors, alpha=0.8, edgecolor='white', linewidth=1.5)
    
    # Labels
    ax.set_yticks(y_positions)
    ax.set_yticklabels([f"{row['task_name']}\n{row['start_time']}-{row['end_time']}" 
                       for idx, row in schedule_df_clean.iterrows()], 
                      fontsize=10, color='white')
    ax.set_xlabel('Duration (Hours)', fontsize=14, color='white', fontweight='bold')
    ax.set_title(f'Daily Schedule - {day_theme}', fontsize=18, color='white', fontweight='bold', pad=20)
    ax.invert_yaxis()
    
    # Styling
    ax.tick_params(colors='white', labelsize=11)
    ax.grid(True, alpha=0.3, color='white')
    ax.set_facecolor('#0F0F0F')
    fig.patch.set_facecolor('#000000')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def render_compact_chart(schedule_df_clean, priority_colors, day_theme):
    """Render compact timeline chart"""
    fig, ax = plt.subplots(figsize=(14, 4), dpi=80)
    
    # Create timeline
    for i, (idx, row) in enumerate(schedule_df_clean.iterrows()):
        start_time = row['start_datetime']
        end_time = row['end_datetime']
        color = priority_colors.get(str(row['priority']), '#777777')
        
        # Create compact bar
        ax.barh(0, (end_time - start_time).total_seconds() / 3600, 
               left=start_time.hour + start_time.minute/60, 
               height=0.5, color=color, alpha=0.8, edgecolor='white')
        
        # Add task name
        mid_time = start_time.hour + start_time.minute/60 + (end_time - start_time).total_seconds() / 7200
        ax.text(mid_time, 0.6, row['task_name'], 
               rotation=45, ha='left', va='bottom', fontsize=8, color='white')
    
    # Styling
    ax.set_xlim(0, 24)
    ax.set_ylim(-0.5, 1.5)
    ax.set_xlabel('Time of Day', fontsize=14, color='white', fontweight='bold')
    ax.set_title(f'Daily Timeline - {day_theme}', fontsize=16, color='white', fontweight='bold')
    ax.set_yticks([])
    ax.set_xticks(range(0, 25, 2))
    ax.set_xticklabels([f"{h:02d}:00" for h in range(0, 25, 2)])
    
    ax.tick_params(colors='white', labelsize=11)
    ax.grid(True, alpha=0.3, color='white')
    ax.set_facecolor('#0F0F0F')
    fig.patch.set_facecolor('#000000')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

def render_timeline_chart(schedule_df_clean, priority_colors, day_theme):
    """Render full timeline chart"""
    fig, ax = plt.subplots(figsize=(12, max(8, len(schedule_df_clean) * 0.5)), dpi=80)
    
    y_positions = range(len(schedule_df_clean))
    
    for i, (idx, row) in enumerate(schedule_df_clean.iterrows()):
        start_time = row['start_datetime']
        end_time = row['end_datetime']
        color = priority_colors.get(str(row['priority']), '#777777')
        
        # Create timeline bar
        duration = end_time - start_time
        start_num = float(mdates.date2num(start_time))
        duration_num = float(mdates.date2num(end_time) - start_num)
        
        bar = Rectangle((start_num, i - 0.4), duration_num, 0.8,
                       facecolor=color, alpha=0.8, edgecolor='white', linewidth=2)
        ax.add_patch(bar)
        
        # Add task label
        text_x = float(start_num + duration_num/2)
        ax.text(text_x, i, f"{row['task_name']}\n{row['start_time']}-{row['end_time']}", 
               ha='center', va='center', fontsize=10, color='white', fontweight='bold')
    
    # Format time axis
    start_min = float(mdates.date2num(schedule_df_clean['start_datetime'].min() - pd.Timedelta(hours=1)))
    end_max = float(mdates.date2num(schedule_df_clean['end_datetime'].max() + pd.Timedelta(hours=1)))
    ax.set_xlim(start_min, end_max)
    ax.set_ylim(-0.5, len(schedule_df_clean) - 0.5)
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    
    # Labels
    ax.set_xlabel('Time of Day', fontsize=16, color='white', fontweight='bold')
    ax.set_ylabel('Scheduled Tasks', fontsize=16, color='white', fontweight='bold')
    ax.set_title(f'Daily Timeline - {day_theme}', fontsize=20, color='white', fontweight='bold', pad=30)
    
    ax.set_yticks(y_positions)
    ax.set_yticklabels([row['task_name'] for idx, row in schedule_df_clean.iterrows()], 
                      fontsize=12, color='white')
    
    # Styling
    ax.tick_params(colors='white', labelsize=11)
    ax.grid(True, alpha=0.3, color='white')
    ax.set_facecolor('#0F0F0F')
    fig.patch.set_facecolor('#000000')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig) 