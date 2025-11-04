import streamlit as st


def render_schedule_feedback():
    """Render the schedule chatbot interface for direct schedule modifications"""
    
    # Chat-style interface for schedule optimization
    st.markdown("---")
    st.subheader("💬 Chat with AI to improve your schedule")
    st.markdown("Tell me what you'd like to change about your schedule, and I'll adjust it for you!")
    
    # Chat interface
    col_chat, col_action = st.columns([3, 1])
    
    with col_chat:
        # Chat input
        user_request = st.text_area(
            "What would you like to change?",
            placeholder="e.g., 'Move my workout to 6 AM', 'Give me longer breaks between tasks', 'Schedule meetings in the afternoon', 'I want more time for lunch'...",
            height=100,
            key="schedule_chat_input"
        )
        
        # Show example requests
        with st.expander("💡 Example requests you can make"):
            st.markdown("""
            **Time adjustments:**
            - "Move my workout earlier to 6 AM"
            - "Schedule all meetings after 2 PM"
            - "Give me 30 minutes for lunch instead of 15"
            
            **Task organization:**
            - "Put my most important tasks in the morning"
            - "Add 10-minute breaks between all tasks"
            - "Group similar tasks together"
            
            **Personal preferences:**
            - "I'm more productive in the evening"
            - "I need time to walk my dog at 5 PM"
            - "Don't schedule anything during my lunch break"
            """)
    
    with col_action:
        st.markdown("**Actions:**")
        
        if st.button("🤖 Update Schedule", 
                   type="primary", 
                   use_container_width=True,
                   help="Tell AI to adjust your schedule based on your request"):
            
            if user_request.strip():
                # Store user request for schedule modification
                st.session_state.user_schedule_request = user_request.strip()
                st.session_state.schedule_chat_submitted = True
                st.session_state.auto_optimize_requested = True  # Flag to trigger automatic optimization
                
                st.success("✅ Got it! Modifying your current schedule...")
                st.info(f"🤖 **AI:** I'll adjust your schedule based on: '{user_request[:80]}{'...' if len(user_request) > 80 else ''}'")
                
                # Store backup of current result
                if hasattr(st.session_state, 'optimized_result'):
                    st.session_state.original_result = st.session_state.optimized_result.copy()
                
                # Trigger re-optimization with existing schedule
                st.rerun()
            else:
                st.warning("Please tell me what you'd like to change about your schedule.")
        
        # Show restore option if there's a backup
        if hasattr(st.session_state, 'original_result'):
            if st.button("↩️ Restore Original", 
                       use_container_width=True,
                       help="Go back to the original optimized schedule"):
                st.session_state.optimized_result = st.session_state.original_result.copy()
                if hasattr(st.session_state, 'user_schedule_request'):
                    del st.session_state.user_schedule_request
                if hasattr(st.session_state, 'schedule_chat_submitted'):
                    del st.session_state.schedule_chat_submitted
                if hasattr(st.session_state, 'auto_optimize_requested'):
                    del st.session_state.auto_optimize_requested
                st.success("✅ Original schedule restored!")
                st.rerun()
    
    # Show current request status if any
    if hasattr(st.session_state, 'user_schedule_request'):
        st.info(f"🤖 **AI is working on:** {st.session_state.user_schedule_request[:100]}{'...' if len(st.session_state.user_schedule_request) > 100 else ''}")


def get_feedback_status():
    """Get the current chat request status for display in other components"""
    if hasattr(st.session_state, 'user_schedule_request') and st.session_state.user_schedule_request:
        return {
            'has_feedback': True,
            'feedback_text': st.session_state.user_schedule_request,
            'is_submitted': st.session_state.get('schedule_chat_submitted', False)
        }
    return {
        'has_feedback': False,
        'feedback_text': '',
        'is_submitted': False
    }


def clear_feedback():
    """Clear all chat requests from session state"""
    if hasattr(st.session_state, 'user_schedule_request'):
        del st.session_state.user_schedule_request
    if hasattr(st.session_state, 'schedule_chat_submitted'):
        del st.session_state.schedule_chat_submitted
    if hasattr(st.session_state, 'auto_optimize_requested'):
        del st.session_state.auto_optimize_requested
    if hasattr(st.session_state, 'original_result'):
        del st.session_state.original_result 