# Chrona - Smart Schedule Optimizer

📅 **Chrona** is an intelligent task scheduling application that leverages Google's Gemini AI to optimize your daily and multi-day schedules. Built with Streamlit, it provides a beautiful, user-friendly interface for managing tasks and generating optimized schedules based on your preferences and constraints.

## ✨ Features

- **🤖 AI-Powered Scheduling**: Uses Google's Gemini 2.5 Flash model to generate optimized, personalized task schedules
- **🌐 English–Vietnamese Interface**: Seamlessly toggle between languages with full UI and response adaptation
- **📊 Productivity Insights**: Visual timelines, metrics, and downloadable CSV exports for easy tracking and analysis
- **🔒 Secure API Handling**: Backend-managed API keys for safe deployment and clean user experience
- **🔧 Modular Localization**: Easy-to-extend translation system with JSON-based language packs
- **📅 Google Calendar Integration**: Export and sync your optimized schedules with Google Calendar (setup required)
- **📈 Analytics Dashboard**: Track your productivity with detailed insights and visualizations
- **🎨 Modern Dark UI**: Beautiful, responsive interface with customizable themes

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Google Generative AI API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/khoatran1809/Chrona.git
cd chrona
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**

Create a `.env` file in the project root:
```env
GOOGLE_GENAI_API_KEY=your_api_key_here
```

You can copy the example file:
```bash
cp .env.example .env
```

Then edit `.env` and add your API key.

5. **Run the application**
```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Usage

### Creating Tasks

1. Navigate to the **📝 Task Builder** tab
2. Fill in task details:
   - Task name
   - Priority (High/Medium/Low)
   - Estimated duration
   - Deadline (optional)
   - Additional notes or constraints
3. Click "Add Task" to add to your task list
4. Repeat for all tasks you want to schedule

### Optimizing Your Schedule

1. Once you've added your tasks, click **"Generate Optimized Schedule"**
2. The AI will analyze your tasks and preferences
3. View your optimized schedule with:
   - Visual timeline
   - Daily breakdown
   - Conflict detection
   - Adjustments suggestions

### Exporting and Syncing

- **Export to CSV**: Download your schedule as a CSV file
- **Google Calendar Sync**: Follow the [Google Calendar Setup Guide](GOOGLE_CALENDAR_SETUP.md) to enable calendar integration

## 🔧 Configuration

### Google Calendar Integration

To enable Google Calendar integration, see the detailed setup guide in [GOOGLE_CALENDAR_SETUP.md](GOOGLE_CALENDAR_SETUP.md).

**Note**: Google Calendar integration requires OAuth 2.0 credentials from Google Cloud Console. The feature is fully implemented but requires API verification for production use.

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_GENAI_API_KEY` | Your Google Generative AI API key | Yes |

## 📁 Project Structure

```
chrona/
├── components/          # UI components
│   ├── analytics/      # Analytics and insights components
│   └── google_calendar/ # Google Calendar integration
├── models/             # Data models
├── services/           # Business logic services
├── config.py           # Configuration and styling
├── main.py             # Main application entry point
├── schedule_optimizer.py # Schedule optimization engine
└── requirements.txt    # Python dependencies
```

## 🛠️ Development

### Adding New Features

The codebase is modular and organized:

- **Components**: UI components in `components/`
- **Services**: Business logic in `services/`
- **Models**: Data models in `models/`

### Running Tests

```bash
# Add tests here as the project grows
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Google Generative AI](https://ai.google.dev/)
- Uses [Google Calendar API](https://developers.google.com/calendar) for calendar integration

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the [Google Calendar Setup Guide](GOOGLE_CALENDAR_SETUP.md) for calendar-related issues
3. Open an issue on GitHub

## 🔒 Security

- **Never commit your `.env` file** - it contains sensitive API keys
- **Never share your `google_calendar_credentials.json`** - it contains OAuth credentials
- All sensitive files are already in `.gitignore`
- API keys should be managed through environment variables

## 🐛 Troubleshooting

### API Key Issues

- **Error**: "API key not configured in backend environment"
  - **Solution**: Make sure your `.env` file exists and contains `GOOGLE_GENAI_API_KEY=your_key`

### Google Calendar Issues

- **Error**: "Credentials file not found"
  - **Solution**: Follow the [Google Calendar Setup Guide](GOOGLE_CALENDAR_SETUP.md) to set up OAuth credentials

### Import Errors

- **Error**: Module not found
  - **Solution**: Make sure all dependencies are installed: `pip install -r requirements.txt`

---

Made with ❤️ for better time management

