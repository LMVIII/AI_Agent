Below is a basic implementation of a Python module for scheduling events in Google Calendar. It uses the Google Calendar API and OAuth2 for authorization. Please note that this is a simplified version and may not cover all use cases.

Before executing this script, you must set up OAuth credentials at the Google Cloud Console and download the credentials JSON file.

First, install the necessary libraries:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Python Script `calendar_event_scheduler.py`:

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import datetime
import pickle 

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def service_account_login():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('calendar', 'v3', credentials=creds)


def create_event(service, calendar_id='primary', summary='Appointment',
                 location='123 Main Street', description='Meeting with Client', 
                 start_time=datetime.datetime.now(), end_time=datetime.datetime.now()):

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
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

if __name__ == '__main__':
    google_calendar_service = service_account_login()
    create_event(google_calendar_service)
```

This will create a new event on the primary calendar of the authenticated user. Make sure to replace `'credentials.json'` with the path to your actual downloaded credentials file.

This script also does not handle OAuth2 error flow, refresh tokens, or service account authorization, which may be necessary depending on your requirements.

Please go through Google Calendar's official Python Quickstart guide to understand more about how to use the API: https://developers.google.com/calendar/quickstart/python

Finally, you should review Google's API use policies because excessive or inappropriate use may result in your usage being throttled or banned.