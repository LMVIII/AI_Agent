Sure, here's an example of how you might set this up in Python:

```python
# file: gcal_scheduler.py
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def create_event(summary, location, description, start_time, end_time):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')
```

This very basic module gets an OAuth2 token, then uses it to authenticate with the Google Calendar API and create an event. A few important notes:

- You need to replace the 'credentials.json' with your own file, which should be obtained from your Google Cloud Console (https://console.cloud.google.com/).

- This event is created on the primary calendar of the user who authorizes the app. If you want to add events to a different calendar, you can replace 'primary' with the calendar ID.

- This example specifies reminders 24 hours before the event by email, and 10 minutes before the event by popup. 

- You can add more functionalities based on your requirements, this is very basic script which covers getting OAuth2 token and adding events to the calendar. 

- You should handle exceptions and errors, this script does not cover those.