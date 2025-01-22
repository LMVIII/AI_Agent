Sure, the following is a simple Python example of a Google Calendar API integration with OAuth2. This will allow you to add an event to Google Calendar. We'll use the 'google-auth', 'google-auth-httplib2', 'google-auth-oauthlib', 'google-api-python-client', 'oauthlib' libraries.

Here is the basic script:

```python
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def login_to_google_account():
    """Shows basic usage of the Google Calendar API.
    Logs into account and returns the service.
    """
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

def create_event(service):
    """Create an event on Google Calendar.
    Uses service obtained from login_to_google_account().
    """
    event = {
        'summary': 'Example event',
        'location': 'Somewhere',
        'start': {
            'dateTime': '2022-07-01T09:00:00',
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': '2022-07-01T17:00:00',
            'timeZone': 'America/Los_Angeles',
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

# Create a new event
service = login_to_google_account()
create_event(service)
```

Before running the code, make sure you go through the following steps:
1. Turn on the Google Calendar API and download the 'credentials.json' file: https://developers.google.com/calendar/quickstart/python
2. Install the necessary libraries (`pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`)
3. Put the 'credentials.json' file in the same directory as this script
4. Run the script! The first time it runs it will open a window to Google's sign in and consent screen.

Please modify this code according to your specific needs. This is a simple framework on how to authenticate to Google's Calendar API and insert a new event. 

Also, remember to handle exceptions as required for your application.