# Google Calendar Integration Setup Guide

## Prerequisites

1. **Google Account**: You need a Google account with access to Google Calendar
2. **Google Cloud Project**: You need a Google Cloud project with Calendar API enabled

## Step-by-Step Setup

### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Note down your project ID

### Step 2: Enable Google Calendar API

1. In the Google Cloud Console, go to "APIs & Services" > "Library"
2. Search for "Google Calendar API"
3. Click on it and click "Enable"

### Step 3: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth 2.0 Client ID"
3. Choose "Web application" as the application type
4. Add authorized redirect URIs:
   - `http://localhost:8501`
   - `http://localhost:8501/`
5. Click "Create"
6. Download the credentials JSON file

### Step 4: Configure Your Project

1. Rename the downloaded file to `google_calendar_credentials.json`
2. Place it in your project root directory (same folder as `main.py`)
3. Make sure the file structure looks like this:

```json
{
  "web": {
    "client_id": "your-client-id.googleusercontent.com",
    "project_id": "your-project-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "your-client-secret",
    "redirect_uris": ["http://localhost:8501"]
  }
}
```

### Step 5: Install Dependencies

Make sure you have the required packages installed:

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 6: Run the Application

1. Start your Streamlit app: `streamlit run main.py`
2. Go to the "📅 Google Calendar" tab
3. Click "🔗 Connect Google Calendar"
4. Follow the authentication flow

## Authentication Flow

1. Click the authorization link that appears
2. Sign in to your Google account
3. Grant permissions to access your calendar
4. Copy the authorization code
5. Paste it into the app and press Enter

## Using the Integration

Once authenticated, you can:

- **Export Tasks**: Select tasks to export to your Google Calendar
- **Import Events**: Import existing calendar events
- **Sync**: Keep your schedule and calendar in sync
- **Manage**: Configure sync settings and preferences

## 🔧 Troubleshooting

### Common Issues

1. **"Credentials file not found"**
   - Make sure `google_calendar_credentials.json` is in the project root
   - Check that the file has the correct JSON structure

2. **"Authentication failed"**
   - Verify your redirect URI is exactly `http://localhost:8501`
   - Make sure your OAuth client is configured for "Web application"

3. **"Access denied"**
   - Check that Google Calendar API is enabled in your project
   - Verify your OAuth consent screen is configured

4. **"Invalid credentials"**
   - Regenerate your OAuth credentials
   - Make sure you're using the correct client ID and secret

### Getting Help

If you encounter issues:
1. Check the error messages in the app
2. Verify your Google Cloud project configuration
3. Ensure all APIs are enabled
4. Try regenerating your credentials

## Security Notes

- Never share your `google_calendar_credentials.json` file
- Don't commit credentials to version control
- Add `google_calendar_credentials.json` and `token.json` to your `.gitignore`
- Regularly review and revoke access if needed

## Supported Features

- ✅ OAuth 2.0 authentication
- ✅ Export tasks to Google Calendar
- ✅ Import events from Google Calendar
- ✅ Real-time sync
- ✅ Multiple calendar support
- ✅ Conflict detection
- ✅ Time zone handling

## Next Steps

After successful setup:
1. Create some tasks in the Task Builder
2. Export them to your Google Calendar
3. Check your calendar to see the synced events
4. Configure sync preferences in the Settings tab 