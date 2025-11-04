def get_theme_emoji(theme):
    """Get emoji for daily theme"""
    theme_emojis = {
        "Strategic": "🎯",
        "Deep Focus": "🧠",
        "Deep Work": "🧠",
        "Communication": "💬",
        "Creative": "🎨",
        "Implementation": "⚙️",
        "Personal": "👥",
        "Reflection": "🤔",
        "Innovation": "💡",
        "Analysis": "📊",
        "Collaboration": "🤝",
        "Results": "🎯",
        "Learning": "📚",
        "Adventure": "🚀",
        "Integration": "🔗",
        "Balanced": "⚖️"
    }
    
    for key, emoji in theme_emojis.items():
        if key.lower() in theme.lower():
            return emoji
    return "📅"

def get_theme_color(theme):
    """Get color for daily theme"""
    theme_colors = {
        "Strategic": "#4F46E5",
        "Deep Focus": "#7C3AED",
        "Deep Work": "#7C3AED",
        "Communication": "#10B981",
        "Creative": "#F59E0B",
        "Implementation": "#EF4444",
        "Personal": "#06B6D4",
        "Reflection": "#8B5CF6",
        "Innovation": "#F97316",
        "Analysis": "#3B82F6",
        "Collaboration": "#14B8A6",
        "Results": "#DC2626",
        "Learning": "#059669",
        "Adventure": "#D97706",
        "Integration": "#7C2D12",
        "Balanced": "#6B7280"
    }
    
    for key, color in theme_colors.items():
        if key.lower() in theme.lower():
            return color
    return "#6B7280" 