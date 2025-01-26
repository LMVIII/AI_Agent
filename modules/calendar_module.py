Sure, to handle this task, you will need to set up Google Calendar API and get the credentials.json file:

1. Go to Google Cloud Console: https://console.cloud.google.com/
2. Create a new project or select an existing one.
3. Enable Google Calendar API for that project.
4. Setup OAuth2.0 by creating new credentials -> OAuth client Id -> Web application -> Authorized redirect URIs -> http://localhost:8000/
5. Download the JSON file, rename it as credentials.json

Now you can start developing the Python script. Below is a sample module that you can use as a reference:

```python
import os.path
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def setup_api():
    """Setup the Google Calendar API."""
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

def schedule_event(start_time_str, end_time_str, summary, description, location):
    """Schedule a new event."""
    service = setup_api()

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
    print(f'Event created: {event["htmlLink"]}')
```

You can use this module's `schedule_event` function to schedule events. It takes the start and end times as string in 'yyyy-mm-ddThh:mm:ss' format, the summary (name of the event), the description and the location as input.

Note that before the first usage of script, consider installing necessary packages with pip
```sh
pip install --upgrade google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

And you should run Python scripts on a server with a running browser for an OAuth2 authentication process. The OAuth2 authorization process leads a user to the link which should be followed to allow application access to the Google Calendar events. Upon successful authorization, 'token.json' will be created, which should be saved for consequent usages.

Please replace 'America/Los_Angeles' with your time zone.