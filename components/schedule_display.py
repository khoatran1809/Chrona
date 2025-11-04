
import streamlit as st
from .schedule_feedback import render_schedule_feedback
from .schedule_multiday import render_multi_day_schedule
from .schedule_single_day import render_single_day_schedule

def render_schedule_results(result):
    """Render optimized schedule results"""
    if "optimized_schedule" not in result:
        return

    st.subheader("📅 Optimized Schedule")

    # Handle both single-day and multi-day formats
    schedule_data = result["optimized_schedule"]
    
    # Check if this is multi-day format (array of day objects)
    if isinstance(schedule_data, list) and len(schedule_data) > 0 and isinstance(schedule_data[0], dict) and "day" in schedule_data[0]:
        # Multi-day format
        render_multi_day_schedule(schedule_data)
    else:
        # Single-day format (backward compatibility)
        render_single_day_schedule(schedule_data, day_index=None)

    # Add recommendations before chat
    if "daily_summary" in result and "recommendations" in result["daily_summary"]:
        st.markdown("---")
        st.subheader("💡 Recommendations")
        for rec in result["daily_summary"]["recommendations"]:
            st.info(f"• {rec}")
    
    # Add schedule feedback interface
    render_schedule_feedback()