Creating a Python script to add events to Google Calendar involves several steps. We need to set up a project on Google Cloud Console, install Google Client libraries, and write a Python script.

First, you need to setup your OAuth2 credentials.

1. Go to the Google Cloud Console (https://console.developers.google.com/)
2. Create a new project
3. Enable Google Calendar API for that project
4. Create credentials for the API
5. When asked which API you are using, select "Google Calendar API v3"
6. When asked where you will be calling the API from, choose "Other UI (e.g., Windows, CLI tool)".
7. When asked what data you will be accessing, select "User data".
8. You should now see a dialog box saying that you need to setup the OAuth consent screen. Click "Setup consent screen"
9. Fill out the necessary fields on this page. You can use your local development environment as the Authorized domain.
10. Now create an OAuth 2.0 Client ID. Name it and then click "Create".
11. Download the JSON for your credentials.

Now let's start writing Python code to access the Google Calendar API.

1. Create a Python file (say, google_calendar.py)
2. Install the necessary libraries if you have not already (google-api-python-client, google-auth-httplib2, google-auth-oauthlib, google-auth, oauthlib) using pip command. 

```python
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib google-auth oauthlib
```

Here is the Python code:

```python
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# The scope URL for read/write access to a user's calendar
SCOPES = 'https://www.googleapis.com/auth/calendar'

CREDENTIALS_FILE = 'path_to_your_downloaded_json_file'


def add_event_to_calendar(summary, location, description, start_time, end_time):
    """Adds an event to the user's calendar"""
    # Use the client_secret.json file to authenticate and create an API client
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": start_time,
                "timeZone": 'America/Los_Angeles',
            },
            "end": {
                "dateTime": end_time,
                "timeZone": 'America/Los_Angeles',
            },
        }
    ).execute()

    return event_result['id']


if __name__ == '__main__':
    add_event_to_calendar('Meeting with Bob', 'Zoom', 'Discuss about project',
                          '2022-12-01T09:00:00', '2022-12-01T10:00:00')
```

This will add an event of a meeting with Bob on 1st Dec 2022 from 9am to 10am. Replace variables as per your requirement and make sure to provide the correct path to your downloaded JSON file. Note: the first time you run the script, it will open a new window in your default web browser asking you to authorize the app to access your Google Calendar data. Once you authorize it, it will store a token.pickle file containing the refresh token so that you won't have to re-authenticate every time.

Please note: Google's OAuth2 implementation may require the web server to obtain consent from the user to access their Google Calendar data. This might not work in a headless environment or where a web server and browser are not available.