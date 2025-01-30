Sure, creating such a module would require a couple of steps and knowing certain key information such as your client_id, client_secret, and refresh_token from Google API.

Here is a basic example of a python module to create Google calendar events. We will use the Google Client Library to interact with the Google Calendar API.

First, install necessary libraries:
```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Python module to schedule events in Google Calendar:

```python
from __future__ import print_function
import datetime
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def create_google_calendar_event(event):
    """Shows basic usage of the Google Calendar API.
    Lists the next 10 events on the user's calendar."""
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

    service = build('calendar', 'v3', credentials=creds)

    event_result = service.events().insert(calendarId='primary', body=event).execute()

    print('Event created: %s' % (event_result.get('htmlLink')))

```

Please replace `'credentials.json'` with your downloaded JSON file of credentials from Google Cloud Console.

This is a very basic example, you should add error checking, exception handling, and modify it according to your needs. For production use, it is strongly recommended to follow Google's best practices for using OAuth 2.0.

After creating this module you can call `create_google_calendar_event` function from your code by passing it a dictionary event.

Example:
```python
event = {
  'summary': 'Sample Event',
  'location': 'Enter location',
  'description': 'Event Description
  'start': {
    'dateTime': '2022-01-09T09:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  },
  'end': {
    'dateTime': '2022-01-09T17:00:00-07:00',
    'timeZone': 'America/Los_Angeles',
  }
}

create_google_calendar_event(event)
```