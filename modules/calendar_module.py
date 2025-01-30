Let's create a Python module that is able to schedule events in Google Calendar using OAuth2. The module goes as follows:

File: gcal_event_manager.py

```python
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
            'dateTime': start_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event['htmlLink']}")

def delete_event(event_id):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print(f"Event deleted: {event_id}")

def get_event(event_id):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    return event
```

This module provides functionality for creating, getting and deleting events in your primary Google Calendar. 

Be sure to replace 'America/Los_Angeles' with your actual timezone, and also note that 'start_time' and 'end_time' must be datetime objects.

To correctly use OAuth2 you first need to activate the Google Calendar API for your Google account and download the `credentials.json` file. Then, run any function from this file: the script will open a new page in your browser asking for permissions. After giving them, the script will store these access permissions locally in a `token.json` file. 

Usage examples:

```python
import datetime
from gcal_event_manager import create_event, get_event, delete_event

# Create Event
start_time = datetime.datetime(2022, 5, 20, 10, 0, 0)
end_time = datetime.datetime(2022, 5, 20, 11, 0, 0)
create_event("Meeting with Bob", "Zoom", "Discuss project X", start_time, end_time)

# Get Event
event_id = "abcdefghijkl"
print(get_event(event_id))

# Delete Event
delete_event(event_id)
```
Remember: Do not publish your 'credentials.json' and 'token.json' files in public repositories for security issues.