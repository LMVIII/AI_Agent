First of all, I will assume that you've created a project in the Google API Console, enabled the Google Calendar API, and obtained OAuth 2.0 client ID credentials. 

I'll write a Python script using the Google Client Library, which allows interaction with Google APIs. 

This script will authenticate a session via OAuth 2.0 and will contain a function to create a new event in your calendar. Note that you'll need to replace 'your_client_id.json' in line 7 with your downloaded OAuth 2.0 client ID .json file. 

Here's your Python script:

```python
from __future__ import print_function
import datetime
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import googleapiclient.discovery

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_account():
    """Shows basic usage of the Google Calendar API
    Lists the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'your_client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, start_time_str, end_time_str, summary, description, location):
    event = {
      'summary': summary,
      'location': location,
      'description': description,
      'start': {
        'dateTime': start_time_str,
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': end_time_str,
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

This is just a simple script. You'll need to call `authenticate_google_account` to authenticate your session. Then, you can use the returned `service` object with the `create_event` function to create a new event on your Google Calendar.

Please note that the date-time strings accepted by `create_event` should be in the following format: 'yyyy-mm-ddThh:mm:ss'. The 'T' and colons are optional.