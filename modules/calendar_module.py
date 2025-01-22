Creating a Python module to schedule events in Google Calendar using OAuth2 protocol involves interacting with Google APIs. This process consists of two main steps:

1. Set up the Google Calendar API and OAuth2.0.

2. Write the Python script to interact with the API.

Here, I'll outline how to implement the code in step two, assuming that step one is complete. 

To create a Python module for this, we will use Google's API client library which should be installed if it isn't already. Install it using pip:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
Main Python module (let's call it `gcal.py`):

```python
import pickle
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service():
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
    return service

def create_event(service, event):
    # Call the Calendar API
    event = service.events().insert(calendarId='primary', body=event).execute()
    return event.get('htmlLink')

def main():
    # Before executing this module, you should create event dictionary.
    event = {
        # Your event dictionary.
    }
    service = get_calendar_service()
    create_event(service, event)

if __name__ == '__main__':
    main()
```

In the above code, make sure that the `credentials.json` file (which you would have gotten from enabling the Google Calendar API in part 1) is in the same directory. Also, to extend the above, you would create a dictionary of event details in the `main()` function to create an event.
Before running this, ensure you have the `credentials.json` correctly set up from Google Cloud Console, because the OAuth2 process requires it. 

Please make sure that the Scopes, token.pickle file, and credentials.json is correctly set as per your application.

This is a simple example and might need changes based on your exact requirements such as error checking, threading, GUI, etc.