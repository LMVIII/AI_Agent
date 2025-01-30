Sure, let's break it down into steps:

First, you need to install the Google Client Library. You can do this by using the following command:
```python
    pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
Create a new python module named `google_calendar.py`:

```python
    from googleapiclient.discovery import build
    from google_auth_oauthlib.flow import InstalledAppFlow
    import datetime

    # Set the scopes and discovery file
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    DISCOVERY_FILE = "/path/to/client_secret.json"

    def authenticate_google_account():
        flow = InstalledAppFlow.from_client_secrets_file(DISCOVERY_FILE, SCOPES)
        credentials = flow.run_console()
        return build('calendar', 'v3', credentials=credentials)

    def create_event(service, start_time_str, summary, duration=1, description=None, location=None):
        end_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S") + \
                   datetime.timedelta(hours=duration)

        event_result = service.events().insert(
            calendarId='primary',
            body={
                "summary": summary,
                "description": description,
                "location": location,
                "start": {
                    "dateTime": start_time_str,
                    "timeZone": 'Your_Time_Zone',
                },
                "end": {
                    "dateTime": end_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "timeZone": 'Your_Time_Zone',
                },
            }
        ).execute()

        print(f'Created event {event_result["id"]}')
        return event_result
```
Please replace "Your_Time_Zone" with your time zone, "/path/to/client_secret.json" with a path to your OAuth 2.0 client secret json file. You can get the "client_secret.json" file from Google Cloud Console.

Then, you can use it to create an event:
```python
    if __name__ == '__main__':
        service = authenticate_google_account()
        create_event(service, '2023-06-09 09:00:00', 'Doctor Appointment', 1,
                     'First check-up', '123 abc street')
```
This will create a 1-hour long appointment on June 9th, 2023 at 9:00am.

Please note:

1. Go through the OAuth Consent Screen and grant permission during the execution of the script.
2. The start time format is important and always needs to be in "Y-m-d H:M:S".
3. The date, details and other settings could be modified to better suit your needs.
4. OAuth2 require you to enable the Google Calendar API on the Google Cloud Console and create a project.
5. Use care with your client_secret.json file - it contains keys that should be kept private and not shared or exposed publicly.