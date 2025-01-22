Here is a basic skeleton of a Python module using Google Calendar API to create events. It uses the Google Auth library for OAuth 2.0.

Please make sure that you have Google Calendar API enabled, and have valid `credentials.json` available which needs to be generated from the Google Cloud Platform.

Here is the code to install necessary Python packages:
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```
Here is the Python module `google_calendar.py`:

```python
import datetime
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def service_account_login():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        return service
    except Exception as e:
        print(e)
        return None

def create_event(service, event_info):
    try:
        event = service.events().insert(calendarId='primary', body=event_info).execute()  
        return "Event created : %s" % (event.get('htmlLink'))
    except Exception as e:
        return "An error occurred : %s" % (e)

def prepare_event():
    # Prepare the event's info
    event_info = {
      'summary': 'Google I/O 2021',
      'location': '8 Parkway, Mountain View, CALIFORNIA, USA',
      'description': 'Educational Program',
      'start': {
        'dateTime': '2021-11-09T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2021-11-09T13:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    return event_info

def main():
    service = service_account_login()
    if service is not None:
        event_info = prepare_event()
        print(create_event(service, event_info))
        
if __name__ == '__main__':
    main()
```
This script first attempts to log in to the Google Calendar API using OAuth2 credentials. After successfully logging in, the script prepares an event using the defined information, and then create an event using the Google Calendar service. If successful, it will print the event URL; otherwise, it will print the error message.

Please replace 'summary', 'location', 'description', 'start', 'end', etc. in method `prepare_event()` as per your event's details. You can also modify SCOPES according to your application's access requirements.