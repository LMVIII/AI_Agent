Sure, I will give you a simple example of how you can work this out. First, you will need to have Google's Python client library and also get `credentials.json` file from Google Cloud Console.

1. Install the Google Client Library
```shell
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
 
2. Get the `credentials.json` file from the [Google Cloud Console](https://console.cloud.google.com/).

3. Python Code:

```python
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googleapiclient.discovery import build
import datetime

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google_account():
    creds = None
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

    try:
        service = build('calendar', 'v3', credentials=creds)
        print('Google account authenticated')
        return service
    except Exception as e:
        print(f'Failed to create service, due to {str(e)}')
        return None


def create_event(service):
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # Set event details
    event_details = {
      'summary': 'Event Summary',
      'location': 'Event Location',
      'description': 'Event Description',
      'start': {
        'dateTime': '2022-12-25T09:00:00-07:00',
        'timeZone': 'America/New_York',
      },
      'end': {
        'dateTime': '2022-12-25T09:00:00-07:00',
        'timeZone': 'America/New_York',
      },
    }

    try:
        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()

        service.events().insert(calendarId='primary', body=event_details).execute()
        print('Event created')
    except Exception as e:
        print(f'Failed to create event, due to {str(e)}')


if __name__ == '__main__':
    service = authenticate_google_account()
    if service:
        create_event(service)
``` 

This code authenticates the user and inserts an event into the user's primary calendar. The `authenticate_google_account` function authenticates the user's Google account and the `create_event` function creates an event in the Google Calendar.

Please note that this is a simple example. There may be numerous scenarios where you want to handle possible exceptions and other things according to your application's requirements. Also ensure you have valid `credentials.json` file and correct SCOPES for accessing the Google Calendar API.