
import streamlit as st

def render_header():
    """Render main header with enhanced styling and status indicator"""
    st.markdown(
        """
        <div class="main-header">
            <h1>🌟 Chrona</h1>
            <p>AI-powered smart scheduling for optimal productivity</p>
            <div style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.8;">
                <span class="status-indicator status-online"></span>
                System Online & Ready
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_footer():
    """Render footer with enhanced styling and additional info"""
    st.markdown("""
    <div class="footer">
        <h3>🚀 Chrona</h3>
        <p>Powered by Streamlit & Google GenAI</p>
        <p>Smart scheduling for optimal productivity</p>
        <div style="margin: 1rem 0; opacity: 0.6;">
            <span style="margin: 0 1rem;">📊 Analytics</span>
            <span style="margin: 0 1rem;">🔒 Secure</span>
            <span style="margin: 0 1rem;">⚡ Fast</span>
        </div>
        <small>© 2025 - Built by LMKT Team for better time management</small>
    </div>
    """, unsafe_allow_html=True)
