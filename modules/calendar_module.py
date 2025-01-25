Sure, the following example provides a basic structure on how to build a python module to schedule events in Google Calendar using OAuth2. This example utilized Google’s Client Library to implement the OAuth2. 

Keep in mind, this program won't work unless you have the "credentials.json" file, which stores the details of your API Key and can be created and downloaded from Google Cloud Console.

```python
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def service_account_login():
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
    except Exception as e:
        print(e)
        return None

    return service

def create_event(service, event_info):
    try:
        event = service.events().insert(calendarId='primary', body=event_info).execute()
        return event['id']
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

if __name__ == '__main__':
    # An example event info, values can be replaced as needed
    event_info = {
      'summary': 'Event summary',
      'description': 'Event description',
      'start': {
        'dateTime': 'yyyy-mm-ddThh:mm:ss',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': 'yyyy-mm-ddThh:mm:ss',
        'timeZone': 'America/Los_Angeles',
      },
    }
    service = service_account_login()
    if service is not None:
        event_id = create_event(service, event_info)
        if event_id is not None:
            print(f'Event created with id: {event_id}')
```

This is a basic example of how to authenticate using OAuth and create an event on Google Calendar. Don't forget to replace `'yyyy-mm-ddThh:mm:ss'` with the actual date and time.
Also, you will need to install the required packages if not already installed using pip:
```shell
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```