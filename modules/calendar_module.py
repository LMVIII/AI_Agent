Creating a Python module that interacts with Google's API requires implementing OAuth2 for accessing user info, handling dependencies like the Google Client Library, setting up Google Cloud, creating credentials, and more. Below is a baseline for creating a Google Calendar event via a Python script. You need to use the `google-api-python-client` and `google-auth-httplib2` and `google-auth-oauthlib` libraries for this.

You can install these libraries using pip:

```bash
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

Now we can write the Python script,

Note that you need to provide your own credential.json file you created from your Google Cloud account.

```python
#Remember to replace "credentials.json" with your own file.
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import os.path
import datetime
import pickle

from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event():
    """Shows basic usage of the Google Calendar API.
    Lists the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

```

Please note: "credentials.json" is a file that is downloaded after creating credentials for your project in Google Cloud Platform's APIs & Services pages. Make sure to save this file and replace `'credentials.json'` with your own file's path. This file stores your `Client ID` and `Client secret`. 
Without it, Google does not know who you are and won't allow the creation of calendars.

Also note: The above program is only for getting the events already present in the calendar, for creating an event you need to call `service.events().insert()` with the event data. 

Make sure to enable the Google Calendar API from your Google Cloud Project and take a look at Python Quickstart of Google Calendar API here: https://developers.google.com/calendar/quickstart/python for more information.