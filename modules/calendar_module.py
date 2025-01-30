Here's a Python script using Google Calendar API. I assumed that you already have your 'credentials.json' from the Google Cloud Console. 

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
    """Shows basic usage of the Google Calendar API.
    Lists the next 10 events on the user's calendar.
    """
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

    service = build('calendar', 'v3', credentials=creds)
    
    return service


def create_event(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' 
    event = {
      'summary': 'Event Name',
      'location': 'Event Location',
      'description': 'Event Description',
      'start': {
        'dateTime': now,
        'timeZone': 'America/Los_Angeles',
      },
      'attendees': [
        {'email': 'attendee1@gmail.com'},
        {'email': 'attendee2@gmail.com'},
      ],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))


if __name__ == '__main__':
    service = service_account_login()
    create_event(service)
```

In this code, 'service_account_login()' function is used to authenticate with OAuth2 by using the token in 'token.pickle'. If the token is not available or invalid, it will get a new one.

'create_event(service)' function creates new event to Google Calendar. Modify the 'event' dictionary in 'create_event(service)' function to suit your needs.

Remember to replace 'Event Name', 'Event Location', 'Event Description' and the emails in the 'attendees' list with actual values.

Please note that to run this Python script, you must first install the following dependencies:

```shell
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```