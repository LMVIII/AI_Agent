To use the Google Calendar API, you must first setup your project on Google Cloud Console, enable the Calendar API, and create credentials to use OAuth2. 

Here is a Python module named 'scheduler'. Save the credential JSON file in the same directory as this script and rename it to 'credentials.json'.

```python
import os
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']


def authenticate_and_build_service():
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
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service


def create_event(service, calendar_id, start_time_str, end_time_str, summary, description=None, location=None):
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S")
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
    }
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f'Event created: {event["htmlLink"]}')

```

You can use this module as follows:

```python
from scheduler import authenticate_and_build_service, create_event

service = authenticate_and_build_service()
calendar_id = 'primary'  
start_time_str = '2022-09-15T09:00:00'  
end_time_str = '2022-09-15T10:00:00' 
summary = 'Meeting with John' 
create_event(service, calendar_id, start_time_str, end_time_str, summary)
```

This will create an event on 15th of September 2022 from 09:00 to 10:00. This code assumes that the user's time zone is 'America/New_York'. It uses OAuth2 to authenticate the user and build the Google Calendar API service.

Remember to fill in the actual 'calendar_id', 'start_time_str', 'end_time_str', and 'summary' values as per the real data. The 'calendar_id' for the primary calendar is 'primary', and for other calendars, it is the email associated with that particular calendar.