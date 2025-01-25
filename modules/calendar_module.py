To interact with Google Calendar, we'll use the Google Calendar API. Google provides client libraries for interacting with this API in various programming languages. These client libraries make it easy to interact with the Google Calendar API, handling a lot of the boilerplate work for you.

The Google Calendar API requires an authorized request, which we'll authenticate using the OAuth2 protocol.

Let's create a Python module that provides this functionality.

NOTE: Before we begin, you need to create credentials for your application in the Google API Console. After creating the project, go to the "Credentials" tab and create OAuth2 credentials. The process will generate a `"credentials.json"` file which should be downloaded and saved into your working directory.

Now, let's start creating the python module named `gcalendar.py`:

```python
import datetime
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def service_account_login():
    """Login to the Google Calendar API and return a service instance."""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)

def create_event(service, calendar_id, start_time_str, end_time_str, summary, description=None, location=None):
    """Create a new event in the specified calendar."""
    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'America/Los_Angeles',
        }
    }

    return service.events().insert(calendarId=calendar_id, body=event).execute()
```

You can use this module like so:

```python
import gcalendar

# Initiate the Google Calendar API service
service = gcalendar.service_account_login()

# ID of the calendar where the event will be created. You can use 'primary' for your primary calendar
calendar_id = 'primary'

# Create an event
event = gcalendar.create_event(
    service, 
    calendar_id,
    'YYYY-MM-DDTHH:MM:SS', # Start time in ISO 8601 format
    'YYYY-MM-DDTHH:MM:SS', # End time in ISO 8601 format
    'Event Summary', # Event title
    'Event Description', # Event description
    'Event Location' # Event location
)

print(f'Event created: {event["htmlLink"]}')
```

Remember to replace 'YYYY-MM-DDTHH:MM:SS' with the actual date and time of the event.