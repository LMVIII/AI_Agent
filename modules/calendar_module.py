To accomplish this, you would need to use Google's API client for Python, which can easily be installed with pip. Here’s a very high-level view of what you'll need to do:

```python
import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def create_event(service, calendar_id='primary', summary='New Event',
                 start_time=None, end_time=None, attendees=[]):
    try:
        start_time = datetime.datetime.now() if not start_time else start_time
        end_time = start_time + datetime.timedelta(hours=1) if not end_time else end_time

        event = {
            'summary': summary,
            'start': {'dateTime': start_time.isoformat()},
            'end': {'dateTime': end_time.isoformat()},
            'attendees': [{'email': a} for a in attendees],
        }

        service.events().insert(calendarId=calendar_id, body=event).execute()
        print('Event created.')
    except HttpError as error:
        print(f'An error occurred: {error}')


def authenticate():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
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
    except Exception as e:
        print(e)
        return None

    return service


if __name__ == '__main__':
    service = authenticate()
    if service:
        create_event(service)
```

This create_event function tries to insert a new event in the calendar using the provided details.

Please replace 'credentials.json' with your own Google APIs credentials file. If you do not have this file, you would need to create OAuth2 credentials in the Google API Console (console.developers.google.com), use it to generate a 'credentials.json' file and place it in the same directory as your Python script. 

Also, please note you may need to allow less secure apps to ON and Display Unlock Captcha for the Google Calendar account for which you are trying to run this script with. See Google Account Help if you have trouble with this.

Please remember to handle exceptions properly according to your specific requirements, this sample just prints out the exceptions to give a generic idea. This script also doesn't handle other details that you may need for a production environment, such as logging, HTTP error codes, retrying failed requests, etc.

*Note: This script involves OAuth 2.0 application, hence tread carefully, do not expose any sensitive details such as passwords, secret keys in public repository or anywhere insecure. Use environment variables or secure key management systems like Vault to handle such sensitive information.*