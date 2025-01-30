Creating a Python module to schedule events in Google Calendar using OAuth2 involves interacting with Google's Calendar API. Here is a basic example of how you can achieve this:

This module relies on Google's `oauthlib` for OAuth2, and the `google-auth`, `google-auth-httplib2`, and `google-auth-oauthlib`, and `google-api-python-client` libraries, so make you sure you have these installed on your Python environment.

You can install them using pip:

```bash
pip install google-auth google-auth-httplib2 google-auth-oauthlib google-api-python-client
```

Below is the module `google_cal.py`:

```python
import os.path
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete your saved credentials
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def service_account_login(creds_file):
    creds = None
    # Check if the token.pickle file exists as it contains your credentials.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
            
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Store the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)

    return service

def create_event(service):
    event = {
      'summary': 'Google Calendar event from Python',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A newly created event from Python module',
      'start': {
        'dateTime': '2022-09-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2022-09-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'recurrence': [
        'RRULE:FREQ=DAILY;COUNT=2'
      ],
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    
if __name__ == '__main__':
    creds_file = 'credentials.json' # Add path to your credentials.json file
    service = service_account_login(creds_file)
    create_event(service)
```

This module enables OAuth2 with Google services and uses these credentials to create an event in your primary Google Calendar.

Ensure you have the `credentials.json` file downloaded from the Google Cloud Console for OAuth2.0 Client IDs (Application type: Desktop app) as per this guide:
https://developers.google.com/workspace/guides/create-credentials

And remember to replace values in `create_event` method like 'summary', 'location', 'description', 'start', 'end' and 'recurrence' with your actual info.

Note: The user must authenticate themselves with their Google account when running the python script. The user will be redirected to their web browser and asked to log in with their Google account.
