To schedule events in Google Calendar, we'd require Google's Calendar API. Below is a sample Python script that will create a new event on Google Calendar:

Note that for it to work, you'd need to set up OAuth2 authentication and download a 'credentials.json' file from the Google Developer Console.

1. You have to create an Google Developer Console project, setup OAuth2 authentication and download 'credentials.json' file.

2. Enable the Google Calendar API for your project.

3. Install the required Python libraries:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

4. Create Python module:

```python
# import required libraries
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import os

SCOPES = ['https://www.googleapis.com/auth/calendar']

def service_account_login():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            
    service = build('calendar', 'v3', credentials=creds)
    return service

def create_event(service, summary, location, description, start_time, end_time, attendees=None):
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [],
    }
    
    for attendee in attendees or []:
        event['attendees'].append({'email': attendee})

    event = service.events().insert(calendarId='primary', body=event).execute()

    print(f"Event created: {event['htmlLink']}")
```

The 'create_event' function can be used to create an event in Google Calendar. You can add event name(summary), location, and start-end datetime in required format.

Output will return you the link of the created event.

Note: Activities like reading a file from the disk or introducing a delay into an application are considered outside the norm for the use-case provided, thus you will have to implement this using your own Python environment.