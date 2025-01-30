Sure, here's how you might approach it. The detailed implementation would use the Google Calendar API and Google's OAuth2.0 authentication.

```python
import datetime
import json
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def schedule_event(summary, location, description, start_time, end_time):
    """Shows basic usage of the Google Calendar API.
    Lists the next specified events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, prompt the user to log in.
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
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

```

This script defines a function `schedule_event` that takes the details of an event as parameters, and schedules it on the authenticated user's Google Calendar. You can modify it per your needs.

Remember, before running the module, you have to create a project on Google Cloud Console, enable calendar API and download the client configuration file and rename as 'credentials.json' to the root directory of your project, you can refer to the official Google API Python client guide. 

Note also, this is a simple implementation. For Production grade code, consider error handling, invalid inputs, security, testing etc.
Please replace `'America/Los_Angeles'` with appropriate timezone.

Make sure you have installed required libraries, using below commands you can install those,

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```