To create Python module to schedule events in Google Calendar using OAuth2, we first need to install some necessary libraries using pip:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Then, you can create a Google Calendar API on Google Cloud Platform and download your credentials.json file.

Here is a basic Python module that you can use to schedule events:

```python
from __future__ import print_function
import datetime
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datefinder

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def scheduled_event(start_time_str, summary, duration=1, description=None, location=None):
    start_time = list(datefinder.find_dates(start_time_str))[0]
    end_time = start_time + datetime.timedelta(hours=duration)

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

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    result = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (result.get('htmlLink'))

# testing the function
# it schedules an event for tomorrow 9 AM PST
scheduled_event("tomorrow at 9 AM", "Test Event")
```
Make sure to replace 'credentials.json' with the path to your actual credentials file. This code will create an event for the primary calendar of the user who authorized the application. 'token.pickle' stores the user's access and refresh tokens after successful login.

Note that the code above assumes the target timezone is America/Los_Angeles. Please adjust those to fit your specific use case.