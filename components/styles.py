

import streamlit as st

def load_custom_styles():
    """Load custom CSS styles for the application"""
    st.markdown("""
    <style>
        /* Base styling with improved gradient */
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        /* Typography improvements */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        /* Enhanced header styling with glassmorphism effect */
        .main-header {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(102, 126, 234, 0.2);
            color: #ffffff;
            text-align: center;
            padding: 3rem 2rem;
            margin-bottom: 2rem;
            border-radius: 20px;
            box-shadow: 
                0 8px 32px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .main-header h1 {
            font-size: 3.5rem;
            margin-bottom: 0.5rem;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
            background: linear-gradient(45deg, #667eea, #764ba2, #f093fb);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradientText 4s ease infinite;
        }

        @keyframes gradientText {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }

        .main-header p {
            font-size: 1.3rem;
            color: rgba(255, 255, 255, 0.9);
            margin: 0;
            font-weight: 300;
        }

        /* Enhanced task cards with hover effects */
        .task-card {
            background: linear-gradient(135deg, rgba(42, 42, 42, 0.8) 0%, rgba(30, 30, 30, 0.8) 100%);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            margin-bottom: 1rem;
            border-radius: 16px;
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.3),
                0 1px 0 rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .task-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 2px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }

        .task-card:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 
                0 8px 32px rgba(102, 126, 234, 0.2),
                0 4px 20px rgba(0, 0, 0, 0.4);
            border-color: rgba(102, 126, 234, 0.3);
        }

        .task-card:hover::before {
            transform: scaleX(1);
        }

        .task-card h4 {
            color: #ffffff;
            margin-bottom: 0.75rem;
            font-size: 1.2rem;
            font-weight: 600;
        }

        .task-card p {
            color: #cccccc;
            margin-bottom: 0.5rem;
            line-height: 1.5;
        }

        .task-card strong {
            color: #ffffff;
        }

        /* Enhanced priority indicators with glow effects */
        .priority-high {
            border-left: 5px solid #ff4444;
            background: linear-gradient(135deg, rgba(255, 68, 68, 0.1) 0%, rgba(30, 20, 20, 0.8) 100%);
            box-shadow: 0 0 20px rgba(255, 68, 68, 0.1);
        }

        .priority-medium {
            border-left: 5px solid #ffb84d;
            background: linear-gradient(135deg, rgba(255, 184, 77, 0.1) 0%, rgba(30, 25, 20, 0.8) 100%);
            box-shadow: 0 0 20px rgba(255, 184, 77, 0.1);
        }

        .priority-low {
            border-left: 5px solid #4caf50;
            background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(20, 30, 20, 0.8) 100%);
            box-shadow: 0 0 20px rgba(76, 175, 80, 0.1);
        }

        /* Enhanced metric cards with animations */
        .metric-card {
            background: linear-gradient(135deg, rgba(45, 45, 45, 0.8) 0%, rgba(26, 26, 26, 0.8) 100%);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 16px;
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            color: #ffffff;
            text-align: center;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
            position: relative;
        }

        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 
                0 8px 32px rgba(102, 126, 234, 0.15),
                0 4px 20px rgba(0, 0, 0, 0.4);
        }

        .metric-card h3 {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .metric-card h2 {
            color: #667eea;
            margin: 0.5rem 0;
            font-weight: 700;
        }

        /* Enhanced sidebar with improved styling */
        .stSidebar {
            background: linear-gradient(180deg, rgba(26, 26, 26, 0.95) 0%, rgba(13, 13, 13, 0.95) 100%);
            backdrop-filter: blur(20px);
            border-right: 1px solid rgba(102, 126, 234, 0.2);
        }

        .stSidebar > div {
            background: transparent;
        }

        /* Enhanced form elements with better UX */
        .stSelectbox > div > div,
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stNumberInput > div > div > input {
            background: linear-gradient(135deg, rgba(42, 42, 42, 0.8) 0%, rgba(30, 30, 30, 0.8) 100%);
            backdrop-filter: blur(10px);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            transition: all 0.3s ease;
        }

        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within,
        .stNumberInput > div > div:focus-within {
            border-color: #667eea;
            box-shadow: 
                0 0 0 2px rgba(102, 126, 234, 0.2),
                0 4px 12px rgba(102, 126, 234, 0.1);
            transform: translateY(-1px);
        }

        /* Enhanced buttons with improved interactions */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 
                0 4px 15px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
            transition: left 0.5s;
        }

        .stButton > button:hover {
            transform: translateY(-2px) scale(1.05);
            box-shadow: 
                0 8px 25px rgba(102, 126, 234, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }

        .stButton > button:hover::before {
            left: 100%;
        }

        .stButton > button:active {
            transform: translateY(0) scale(1.02);
        }

        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            box-shadow: 
                0 4px 15px rgba(40, 167, 69, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        .stButton > button[kind="primary"]:hover {
            box-shadow: 
                0 8px 25px rgba(40, 167, 69, 0.4),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }

        /* Enhanced dataframe styling */
        .stDataFrame {
            background: rgba(42, 42, 42, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Enhanced expander styling */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, rgba(42, 42, 42, 0.8) 0%, rgba(30, 30, 30, 0.8) 100%);
            backdrop-filter: blur(10px);
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            transition: all 0.3s ease;
        }

        .streamlit-expanderHeader:hover {
            border-color: rgba(102, 126, 234, 0.3);
            transform: translateY(-1px);
        }

        .streamlit-expanderContent {
            background: rgba(26, 26, 26, 0.8);
            backdrop-filter: blur(10px);
            border-radius: 0 0 12px 12px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-top: none;
        }

        /* Enhanced footer styling */
        .footer {
            background: linear-gradient(135deg, rgba(26, 26, 26, 0.8) 0%, rgba(13, 13, 13, 0.8) 100%);
            backdrop-filter: blur(20px);
            padding: 3rem 2rem;
            margin-top: 3rem;
            border-radius: 20px;
            border: 1px solid rgba(102, 126, 234, 0.2);
            text-align: center;
            color: #888;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }

        .footer h3 {
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        /* Loading and status indicators */
        .stSpinner {
            border-color: #667eea !important;
        }

        /* Enhanced message styling with animations */
        .stSuccess {
            background: linear-gradient(135deg, rgba(40, 167, 69, 0.15) 0%, rgba(32, 201, 151, 0.15) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(40, 167, 69, 0.3);
            border-radius: 12px;
            animation: slideIn 0.3s ease;
        }

        .stError {
            background: linear-gradient(135deg, rgba(220, 53, 69, 0.15) 0%, rgba(255, 68, 68, 0.15) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(220, 53, 69, 0.3);
            border-radius: 12px;
            animation: slideIn 0.3s ease;
        }

        .stWarning {
            background: linear-gradient(135deg, rgba(255, 193, 7, 0.15) 0%, rgba(255, 184, 77, 0.15) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 193, 7, 0.3);
            border-radius: 12px;
            animation: slideIn 0.3s ease;
        }

        .stInfo {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(102, 126, 234, 0.3);
            border-radius: 12px;
            animation: slideIn 0.3s ease;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Mobile responsiveness with enhanced touch targets */
        @media (max-width: 768px) {
            .main-header {
                padding: 2rem 1rem;
            }
            
            .main-header h1 {
                font-size: 2.5rem;
            }
            
            .main-header p {
                font-size: 1.1rem;
            }
            
            .task-card {
                padding: 1rem;
                margin: 0.5rem 0;
                font-size: 14px;
            }
            
            .metric-card {
                padding: 1.5rem 1rem;
                margin: 0.25rem 0;
            }
            
            .stDataFrame {
                font-size: 12px;
            }
            
            .main .block-container {
                padding-left: 1rem;
                padding-right: 1rem;
            }

            /* Enhanced touch targets for mobile */
            .stButton > button {
                min-height: 48px;
                padding: 1rem 1.5rem;
                font-size: 16px;
            }
            
            .stSelectbox > div > div,
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                min-height: 48px;
                font-size: 16px;
            }
        }

        /* Improved accessibility */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }

        /* Focus indicators for keyboard navigation */
        .stButton > button:focus,
        .stSelectbox > div > div:focus-within,
        .stTextInput > div > div:focus-within,
        .stTextArea > div > div:focus-within {
            outline: 2px solid #667eea;
            outline-offset: 2px;
        }

        /* Enhanced scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(26, 26, 26, 0.5);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea, #764ba2);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a6fd8, #6b439a);
        }

        /* Enhanced container spacing */
        .element-container {
            margin-bottom: 1rem;
        }

        /* Status indicators with pulse animation */
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 0.5rem;
        }

        .status-online {
            background: #4caf50;
            animation: pulse 2s infinite;
        }

        .status-offline {
            background: #f44336;
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
        }

        /* Enhanced card grid layout */
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        /* Progress indicators */
        .progress-bar {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            height: 8px;
            overflow: hidden;
            margin: 0.5rem 0;
        }

        .progress-fill {
            background: linear-gradient(90deg, #667eea, #764ba2);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
    </style>
    """, unsafe_allow_html=True)

