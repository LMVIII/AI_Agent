I won't be able to provide a full, tested solution as it would require an actual Google account and API credits to perform a complete test. However, I can give you a breakdown on how this can be achieved.

Firstly, you will need to install the Google Client Library using pip like:

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

You'll need to follow the Python Quickstart guide (https://developers.google.com/calendar/quickstart/python) to setup the `credentials.json` file.

Once you've done this setup, here's the general content of your module:

```python
# importing necessary libraries
from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# the scope for google calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

def create_event(summary, location, description, start_event, end_event, attendees):
    """
    Create an event in google calendar
    """

    credentials = None

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_event,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_event,
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [
            {'email': attendee},
        ],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print("Event created: %s" % (event.get('htmlLink')))

```

You will need to provide the necessary details like event summary, location, description, start and end times, and the list of attendees (as a list of email addresses) to call your create_event method and create an event.

Remember you'll need to provide the startDate and endDate in the right format: 

```
dateTime": "2021-05-28T09:00:00-07:00"
```

The line 
```python
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
```
..expects the credentials.json to be in the same directory as your python script. Please ensure to provide the correct path to your credential file.
Also note, event times need to be in RFC3339 format.

Apart from this module, remember to follow the complete OAuth2 flow when using the Google API with Python. Provide the expected scopes to ensure your application has the necessary permissions and properly handle token expiry and refreshing.

Remember to secure your credentials.json as it contains sensitive information. Secure transmission and storage of this information should be a top priority.

There are other important aspects not covered here like error handling and managing calendar permissions, but this gives a basic overview of the process.