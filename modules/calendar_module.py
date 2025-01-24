Sure, to interact with Google Calendar API, we use `google-auth`, `google-auth-httplib2`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client`, `oauthlib` packages. If they are not installed, use pip to install them:

```bash
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client oauthlib
```

Now, using these libraries, let's create a python module named `calendar_module.py`:

```python
from __future__ import print_function
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
import datetime

class CalendarModule:

    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, creds_path):
        creds = None

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', CalendarModule.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, CalendarModule.SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=creds)

    def add_event_to_calendar(self, event):
        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')

if __name__ == '__main__':
    creds_path = 'path_to_your_credentials_file.json'

    event_data = {
        'summary': 'Test Event',
        'start': {
            'dateTime': datetime.datetime.now().isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': (datetime.datetime.now() + datetime.timedelta(hours=1)).isoformat(),
            'timeZone': 'America/Los_Angeles',
        },
    }

    cal = CalendarModule(creds_path)
    cal.add_event_to_calendar(event_data)
```

Make sure to replace `'path_to_your_credentials_file.json'` with the path to your actual `credentials.json` file. You can create your `credentials.json` file from your Google Cloud Console.

This script will open a new window in your default web browser and ask for the permission to access your Google Account. This only happens for the first time you run the script, or whenever the `token.json` file is missing or invalid.

The `add_event_to_calendar` method adds events to the primary calendar. The event is passed as a dictionary in the method. You can change or add any other details to the event as you wish. This is a very basic module and can be improved by handling exceptions, having functions to delete and update events, or interacting with non-primary calendars.