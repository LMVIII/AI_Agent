Sure. Here's a simple Python module that uses Google's API client and OAuth2 to create events on a user's Google Calendar.

For simplicity, we'll name this module `gcal.py`. Before you run the code, remember you have to obtain valid client_id, client_secret, and refresh_token from Google API Console, which involve enabling the Google Calendar API for your project and setting up OAuth2 credentials.

```python
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime
import pytz
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Shows basic usage of the Google Calendar API.
        Returns the Google Calendar API service.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(e)
        return None

def create_event(start_time_str, end_time_str, summary, description=None, location=None):
    service = get_calendar_service()

    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": summary,
            "description": description,
            "location": location,
            "start": {"dateTime": start_time_str, "timeZone": 'Asia/Kolkata'}, 
            "end": {"dateTime": end_time_str, "timeZone": 'Asia/Kolkata'},
        }
    ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

```

The `get_calendar_service` function uses OAuth2 to connect to the user's Google account, returning a service object that can be used to interact with the Google Calendar API.

The `create_event` function takes the start time, end time, event summary, description (optional), and location (optional) as parameters.

Please note that you need to modify according to your time zone in create_event function. Here I used 'Asia/Kolkata' as a timezone. 

To use this module to create an event, you would do something like:
```python
import gcal
gcal.create_event('2023-05-25T14:30:00', '2023-05-25T15:30:00', 'My Event', 'This is description', 'Zoom')
```

This will create an event on 25th May 2023 from 14:30 to 15:30 with the title 'My Event' and description 'This is description'. The location is 'Zoom'. The dateTime must be an ISO8601 timestamp.
