Creating a Python module to schedule events in Google Calendar using OAuth2 authentication involves multiple steps and requires some dependencies. Here is an example of how you might set up the basics of a module like this:

```python
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

# The SCOPES your module needs to access Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def schedule_event(start_time, summary, duration=1, attendees=None, description=None):
    service = build('calendar', 'v3', credentials=get_credentials())
    # Here you needs to write detailed implementation on how you're going to prepare 'event' object.
    # 'event' object might look like: 
    event = {
    'summary': summary,
    'location': '', 
    'description': description, 
    'start': {
        'dateTime': start_time, 
        'timeZone': 'America/Los_Angeles', 
        },
    'end': {
        'dateTime': start_time+datetime.timedelta(hours=duration),
        'timeZone': 'America/Los_Angeles',
        },
    'attendees': [
        {'email': attendee},
        ],
    }
    
    # Call the Calendar API
    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

```

Note: 
- You will need to have a 'credentials.json' file present in your application's directory. This file can be obtained by enabling the Google Calendar API in your Google Cloud Console.
- This code will open a web page where you need to allow the permissions for your Google account and then it will store the token in a 'token.pickle' file for future uses.
- This code assumes that 'start_time' is passed as a datetime object so please make sure to import the datetime module. Also, 'attendees' should be a list of email addresses.
- Also, detailed implementation regarding how to prepare the 'event' object in detail. Please refer Google Calendar Events Insert API documentation (https://developers.google.com/calendar/api/v3/reference/events/insert) for the same.

This sample code above is a starting point which will need to be extended and adjusted to suit your specific requirements and the specific data structures of your application.