Sure, here is a basic guide to create a Python module for scheduling events on Google Calendar. We will be using the Google Calendar API and OAuth2 for authentication.

Create a new project on Google Cloud, enable the Google Calendar API, and create OAuth2 credentials. Download the credentials.json file and put it in your working directory.

Here's an example of such a module:

```python
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_event(service, event):
    return service.events().insert(calendarId='primary', body=event).execute() 

def schedule_event(start_time_str, end_time_str, summary, description=None, location=None):
    creds = authenticate()
    service = build('calendar', 'v3', credentials=creds)
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S")
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Los_Angeles',
        }
    }
    create_event(service, event)
```

You can call `schedule_event` with the event details to schedule an event on Google Calendar. Make sure to pass the date-time string in the format "YYYY-MM-DDTHH:MM:SS”.

Please replace the 'credentials.json' and 'token.pickle' file path with your own file path. In the code above they are in the same directory.

A more detailed guide can be found in the Google Calendar API Python Quickstart guide: https://developers.google.com/calendar/quickstart/python