Here is a simple Python module that uses the Google Calendar API with OAuth2 to schedule events.

Please note that this module only includes the function to create an event and doesn't include the full OAuth2 procedure. It's assumed the user already has a valid OAuth2 token.

Make sure you have google-auth, google-auth-transport-requests, google-auth-oauthlib, google-auth-httplib2, and google-api-python-client installed. You may install them via pip:

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib google-auth google-auth-transport-requests
```

```python
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

class GoogleCalendar:

    def __init__(self, token):
        """ Initialize the Google Calendar API client """
        self.creds = Credentials.from_authorized_user_file(token)
        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_event(self, summary, location, description, start_time, end_time, attendees=[], reminder_minutes=10):
        """
        Create an event on Google Calendar.
        """
        event = {
            'summary': summary,
            'location': location,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'America/Los_Angeles',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'America/Los_Angeles',
            },
            'attendees': [
                {'email': attendee} for attendee in attendees
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': reminder_minutes},
                ],
            },
        }

        event = self.service.events().insert(calendarId='primary', body=event).execute()
        print(f'Event created: {event.get("htmlLink")}')
        return event

```

In this class, `create_event` function takes in a summary of the event, a description, a start time, an end time, and a list of attendees (as email addresses). You can call this function to create an event, and it will return the created event information.

Make sure that you've turned on Calendar API for your project under Google console and have the appropriate credentials.

Make sure to replace `'America/Los_Angeles'` with the appropriate time zone for your use case.

Be sure your datetime is in RFC3339 format. For example: `2022-03-25T15:30:00.00Z`.

Please handle the exception for the request as per your application logic. Here I've just kept it at a very high level.