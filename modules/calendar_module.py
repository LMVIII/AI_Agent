Sure, I can provide you an example of how to create a Python module used for scheduling events in Google Calendar using OAuth 2. However, this is just an example and the actual Google's APIs require you to create OAuth 2.0 Client ID which won't be provided in the code. Please refer to API documentation for more details.

Creating a new Google Calendar event involves multiple steps:
1. Set up the Google Calendar API
2. Download and set up the client configuration
3. Create a Python script

Below is an example Python module. Replace 'credentials.json' with the path to your downloaded client configuration, and fill in your own details in 'EVENT': 

```python
import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file 'token.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def schedule_event():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API

    # 'Z' indicates UTC time
    start_time = datetime.datetime(2021, 11, 1, 7, 30, 0)
    end_time = start_time + datetime.timedelta(hours=1)
    timezone = 'America/Los_Angeles'

    event = {
        'summary': 'Python developer meeting',
        'location': 'Your Location',
        'description': 'Discuss about upcoming software project',
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
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
    print(f'Event created: {event["htmlLink"]}')

if __name__ == '__main__':
    schedule_event()
```

This Python script will prompt you for permission to access your Google Calendar and save an 'token.json' file for subsequent uses. 

Make sure to replace the start_time, end_time, and timezone with your desired date, time, and timezones respectively. Variables 'summary', 'location', and 'description' should also be customized according to your event's details.

For more information and tutorials, see Python Quickstart on Google Calendar API Python docs: https://developers.google.com/calendar/quickstart/python

Remember that you need a 'credentials.json' file downloaded from Google Cloud Console -> APIs & Services -> Credentials. You have to create a project, then create credentials for OAuth Client ID. After that, you should be able to download the 'credentials.json' file.