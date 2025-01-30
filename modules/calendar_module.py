Before we go ahead, note that before you can use the Google Calendar API, you should have a project with a configured OAuth2.0 client downloaded as a JSON file. Downloaded json file should be in your working directory as this will be used for authenticating your application. Once you have that, you can start creating your Python app.

Here's a simple way to create a Python module to schedule events in Google Calendar using OAuth2:

Install required libraries, google-auth, google-auth-oauthlib, google-auth-httplib2, and google-api-python-client, using pip:
```sh
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

You can now create the Python module(let's name it `calendar_event.py`):

```python
import os.path
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json
SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google_account():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


def schedule_event(service, event):
    return service.events().insert(calendarId='primary', body=event).execute()


def create_event(summary, location, description, start_time_str, end_time_str):
    return {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time_str,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time_str,
            'timeZone': 'America/Los_Angeles',
        },
    }


if __name__ == '__main__':
    service = authenticate_google_account()
    event = create_event('Google I/O 2022', '800 Howard St., San Francisco, CA 94103',
                         'A chance to learn about Google\'s latest developer products.',
                         datetime.datetime.now().isoformat(), (datetime.datetime.now() + datetime.timedelta(hours=2)).isoformat())
    scheduled_event = schedule_event(service, event)
    print('Event created: %s' % (scheduled_event.get('htmlLink')))
```

This is a maximum simplified and clear example, make sure to measure all risks and potential security wholes in case of making it a production part of your software. Creating real-world application may require a lot more, like secret management, error-checking and handling, retries, user-interface, deployment scripts, etc. But you can use this to further extend as per your use case.