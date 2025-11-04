import streamlit as st
from ui_components import render_schedule_results, get_feedback_status

def render_schedule_optimization(optimizer, preferences):
    """
    Render the schedule optimization section with buttons and logic.
    
    Args:
        optimizer: The ScheduleOptimizer instance
        preferences: User preferences from sidebar
    """
    st.markdown("### 🎯 Schedule Optimization")

    # API status indicator
    if st.session_state.get('api_initialized', False):
        st.success("🟢 AI Optimization Ready")
    else:
        st.error("🔴 API Key Required")

    # Optimization button and logic
    if optimizer.tasks and st.session_state.get('api_initialized', False):
        st.markdown("#### 🚀 Generate Schedule")
        
        # Get feedback status using utility function
        feedback_status = get_feedback_status()
        is_reoptimization = feedback_status['is_submitted']
        
        # Show different button text and logic for re-optimization
        if is_reoptimization:
            button_text = "🔄 Re-optimize with Feedback"
            button_help = "Apply your feedback to create an improved schedule"
            spinner_text = "🤖 Re-optimizing with your feedback..."
        else:
            button_text = "🎯 Optimize Schedule!"
            button_help = "Generate an AI-optimized schedule from your tasks"
            spinner_text = "🤖 AI is optimizing your schedule..."
        
        # Check if automatic optimization is requested (from chat)
        auto_optimize = st.session_state.get('auto_optimize_requested', False)
        
        if st.button(button_text, type="primary", use_container_width=True, help=button_help) or auto_optimize:
            # Clear any existing optimization data first to ensure fresh start
            if hasattr(st.session_state, 'optimized_result'):
                del st.session_state.optimized_result
            
            # Clear auto-optimization flag if it was triggered
            if auto_optimize:
                st.session_state.auto_optimize_requested = False
                spinner_text = "🤖 Processing your chat request and updating schedule..."
            
            with st.spinner(spinner_text):
                # Include user feedback if available
                optimization_preferences = preferences.copy()
                
                if feedback_status['has_feedback']:
                    # Add user feedback to preferences for the optimizer
                    optimization_preferences['user_schedule_request'] = feedback_status['feedback_text']
                    st.info(f"🔄 **Applying feedback:** {feedback_status['feedback_text'][:100]}{'...' if len(feedback_status['feedback_text']) > 100 else ''}")
                
                result = optimizer.optimize_schedule(optimization_preferences)

                if "error" in result:
                    st.error(f"❌ {result['error']}")
                else:
                    if auto_optimize:
                        st.success("✅ Schedule updated based on your chat request!")
                        # Clear feedback flags after successful chat optimization
                        st.session_state.schedule_chat_submitted = False
                    elif is_reoptimization:
                        st.success("✅ Schedule re-optimization complete with your feedback!")
                        # Clear feedback flags after successful re-optimization
                        st.session_state.feedback_submitted = False
                    else:
                        st.success("✅ Schedule optimization complete!")
                    
                    # Completely replace with new optimization results
                    st.session_state.optimized_result = result
                    # Trigger rerun to immediately show fresh Daily Summary in left column
                    st.rerun()
        
        # Show feedback status if active using utility function
        if feedback_status['has_feedback']:
            st.info("💬 **User feedback active** - Next optimization will consider your preferences")
    
    elif optimizer.tasks and not st.session_state.get('api_initialized', False):
        # Show re-optimization option even without API if there's existing result and feedback
        feedback_status = get_feedback_status()
        if hasattr(st.session_state, 'optimized_result') and feedback_status['has_feedback']:
            st.warning("🔧 API key required for re-optimization with feedback")
    
    # Display optimization results
    if hasattr(st.session_state, 'optimized_result'):
        render_schedule_results(st.session_state.optimized_result)
    elif not st.session_state.get('api_initialized', False):
        st.info("🔧 Configure your API key in the sidebar to enable AI optimization")
    elif not optimizer.tasks:
        st.info("👈 Add some tasks first to optimize your schedule") 