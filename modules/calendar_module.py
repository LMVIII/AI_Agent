In python, the `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, `google-api-python-client` libraries are necessary to work with Google services API like Google calendar, Google drive etc. 

You can install these libraries using pip:

```python
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

Below is the Python module for scheduling events in Google Calendar using OAuth2:

```python
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def service_account_login():
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

    return build('calendar', 'v3', credentials=creds)


def create_event(service, summary, location, description, start_time_str, end_time_str, attendees):
    # Call the Calendar API
    start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")
    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": summary,
                                               "location": location,
                                               "description": description,
                                               "start": {"dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'Asia/Kolkata'},
                                               "end": {"dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"), "timeZone": 'Asia/Kolkata'},
                                               "attendees": attendees,
                                           }
                                           ).execute()

    return event_result['id']


if __name__ == '__main__':
    service = service_account_login()
    attendees = [{"email": 'attendee1@gmail.com'}, {"email": 'attendee2@gmail.com'}]
    create_event(service, 'Meeting with Team', 'Office', 'Discuss about the product', 
                 '2021-09-24 15:00:00', '2021-09-24 16:30:00', 
                 attendees)

```
Please remember to replace 'credentials.json' with the path to your actual credentials file.
This script will open a new window to authenticate via google OAuth2, you only need to do this once, your tokens will be stored in token.pickle for future usage. 

Creating an event with Google Calendar needs a calendarId, in this case, it is 'primary' to represent the primary calendar of the user, you can change it if you want to use other calendars. 
A time zone is also specified for the start and end time of the event. The attendees are a list of email addresses in dict format. Other optional arguments can also be added, please check the Google Calendar API for more details.