To interact with Google Calendar using Python, we'll use the Google Client Library. This will also involve setting up OAuth 2.0 in the Google Cloud Console to get the necessary credentials.

Below is a basic Python module, which you can use as a starting point. It has a `create_event` function that creates an event in the primary Google Calendar for the authenticated user.

```python
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_service():
    """Shows basic usage of the Google Calendar API
    Returns a Google Calendar API service.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        service = build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(e)
        return None

    return service


def create_event(summary, location, description, start, end):
    service = create_service()

    if service is None:
        print("Failed to create service")
        return

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start,
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end,
            'timeZone': 'America/New_York',
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
    print('Event created: %s' % (event.get('htmlLink')))

# Example usage
create_event(
    summary='Google I/O 2025',
    location='800 Howard St., San Francisco, CA 94103',
    description='A chance to learn more about Google\'s developer products.',
    start='2025-05-28T09:00:00-07:00',
    end='2025-05-28T17:00:00-07:00'
)
```

Be sure to replace the 'credentials.json' with your own OAuth2 credentials file which you would download from the Google Cloud Console. You can follow the Python Quickstart guide on the Google Calendar API Python docs to see how you can download the credentials.json file.

Notice that this script will open a new window in your default web browser and ask for permission to access your Google Calendar data. After giving it the permission, you can close the browser and run your script again to access your data. It will store your access token in a file named 'token.pickle', and it will use it for subsequent runs.

Before running this code, install the necessary libraries using pip:

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```