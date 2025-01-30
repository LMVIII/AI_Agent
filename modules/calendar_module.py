Sure, below you can find an example of a Python module for scheduling events in Google Calendar using OAuth2. Please replace `'credentials.json'` with your actual credentials json file provided by your Google Cloud Console.

```python
# You need to install google-auth, google-auth-oauthlib, google-auth-httplib2 and google-api-python-client libraries
# You can install using pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import datetime
import json
import os.path
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarEventScheduler:

    def __init__(self):
        """
        Shows basic usage of the Google Calendar API.
        Lists the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            with open('token.json', 'r') as token:
                creds = json.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
                
        self.service = build('calendar', 'v3', credentials=creds)


    def add_event(self, calendar_id, event):
        """
        Adds an event to the specified calendar_id.
        :param calendar_id: str, ID of the calendar where the event will be added.
        :param event: dict, The event to add to the calendar.
        :return: event object if successful, None otherwise.
        """
        try:
            event = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        except Exception as e:
            print(f'An error occurred: {e}')
            return None
        return event
```
You can use this library like this:
```python
gcal = GoogleCalendarEventScheduler()
event = {
  'summary': 'Google I/O 2015',
  'location': '800 Howard St., San Francisco, CA 94103',
  'description': 'A chance to hear more about Google\'s developer products.',
  'start': {
    'dateTime': '2015-05-28T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2015-05-28T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
}    
ev = gcal.add_event('primary', event)
```