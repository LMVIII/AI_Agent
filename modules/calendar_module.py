Sure, Here is a Python module that schedules events in Google Calendar using OAuth2. Please note that due to security reasons, we are not filling in client_id and client_secret here. Also, make sure that you have Google client library - if not please do pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

```python
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

def schedule_event(summary, location, description, start_time, end_time):
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']

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
        # Save the credentials for the next run.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API.
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    event_result = service.events().insert(
        calendarId='primary',
        body={
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
        }
    ).execute()

    print('Event created: %s' % (event_result.get('htmlLink')))

if __name__ == "__main__":
    schedule_event('Test Event', 'Test Location', 'Test Description', '2022-11-16T15:00:00', '2022-11-16T18:00:00')
```

Before running the script, you will need to download credentials.json from your Google Cloud Console where you have enabled the Calendar API. The client_id and client_secret are inside this file. 

The token.pickle file will be created automatically after the first run of the script and the user logged into his Google account where he has given access to. This file contains the user's access and refresh tokens. 

This module does not handle errors; in a production environment you would want to add error handling.