To interact with the Google Calendar API using python, you need to use Google client libraries. Here is a sample module using which you can schedule an event:

```python
# Python Module : google_calendar_scheduler.py
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_account():
    """Shows basic usage of the Google Calendar API."""

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def schedule_event(service, start_time_str, end_time_str, summary, description, location):
    """Schedules an event on the Google Calendar."""

    start_time = datetime.datetime.strptime(start_time_str, '%Y-%m-%dT%H:%M:%S')
    end_time = datetime.datetime.strptime(end_time_str, '%Y-%m-%dT%H:%M:%S')

    event_result = service.events().insert(calendarId='primary',
        body={
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'Asia/Kolkata'},
            "end": {"dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'Asia/Kolkata'},
            "location": location
        }
    ).execute()

    print(f"Event created: {event_result['htmlLink']}")
    
    return event_result
```
Here is how to use this module from another python file:

```python
# Python Script
from google_calendar_scheduler import authenticate_google_account, schedule_event

def main():
    service = authenticate_google_account()

    start_time_str = '2022-07-08T09:00:00'
    end_time_str = '2022-07-08T10:00:00'
    summary = "Meeting with John"
    description = "Discuss about the new project"
    location = "Conference Room"

    schedule_event(service, start_time_str, end_time_str, summary, description, location)

if __name__ == '__main__':
    main()
```
This would schedule an event from 9 AM to 10 AM on July 8, 2022.

Please remember to replace `'credentials.json'` with your actual details and to get your credentials visit https://developers.google.com/calendar/quickstart/python and click on "Enable the Google Calendar API". Download the JSON file and replace 'credentials.json' in the script with your path to the JSON file.

Please remember to always review and follow Google's best practices for using OAuth2, including never exposing your client secret.