Creating a Python module to schedule events in Google Calendar using OAuth2 involves integrating the Google Calendar API. Here's a simple module named `google_calendar.py` to demonstrate how to authenticate and create an event:

First, install the necessary Python libraries:

```shell
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib 
```

Here is the `google_calendar.py`:

```python
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the SCOPES. If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def auth_google_cal():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, prompt the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES) # 'credentials.json' obtained from Google Cloud Console.
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_event(start_time, end_time, summary, description=None, location=None):
    creds = auth_google_cal()

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Los_Angeles',
        },
        'reminders': {'useDefault': False},
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

```

To use the module to create an event:

```python
import datetime
import google_calendar

start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(hours=1)

summary = 'My Event'
description = 'This is my sample event created for Google Calendar.'
location = 'My Address, City, State'

google_calendar.create_event(start_time, end_time, summary, description, location)
```

In the 'credentials.json', replace it with your own OAuth2 credentials (client_id and client_secret) which you can obtain from the Google Cloud Console (https://console.developers.google.com/).
The first time you run this, it will prompt you to allow the app to access your Google Calendar. It will then store these credentials in a file named 'token.pickle'.