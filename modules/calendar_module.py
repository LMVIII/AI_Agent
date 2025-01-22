To schedule events in Google Calendar using OAuth2, you will need to have a Google account and to have enabled the Google Calendar API in your Google Cloud Console. You will also need to install the `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, and `google-api-python-client` libraries. We'll also use the `datetime` and `pickle` libraries in this example.

Here is an basic example on how to create an event on Google Calendar using Python and OAuth2.0:

```python
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import datetime

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def service_account_login():
    """Loads in the credentials and creates a service"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    return service

def create_event(service):
    """Creates an event on the user's primary calendar"""
    start_time = datetime.datetime(2022, 7, 4, 21, 30, 0)
    end_time = start_time + datetime.timedelta(hours=4)
    timezone = 'America/Los_Angeles'
    
    event = {
      'summary': 'Amazing Event!',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'Really, you should come to this event.',
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
        'overrides': [{'method': 'email', 'minutes': 24 * 60}, {'method': 'popup', 'minutes': 10}],
      },
    }

    service.events().insert(calendarId='primary', body=event).execute()
    
if __name__ == '__main__':
    service = service_account_login()
    create_event(service)
```

This example takes in a date and time for an event, a location, and a summary to create an event on Google Calendar. The authorization tokens are stored in a pickle file and retrieved before each event creation. To get the required 'client_secrets.json' file, you need to setup OAuth credentials on Google Cloud Platform and download the file.

Remember that this is a simplistic approach and won't cover every possible situation. Always check the Google Calendar Python API for more complex operations.