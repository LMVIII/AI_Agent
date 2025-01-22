from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from base64 import urlsafe_b64encode
from datetime import datetime, timedelta, timezone
import pytz
import logging
import traceback

# Enable detailed logging
logging.basicConfig(level=logging.DEBUG)

# Scopes for Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def format_time_to_timezone(utc_time, timezone_name):
    """
    Convert UTC datetime to the specified time zone.
    """
    tz = pytz.timezone(timezone_name)
    local_time = utc_time.astimezone(tz)
    return local_time.strftime("%A, %B %d, %Y at %I:%M %p %Z")

def create_email(recipient, subject, body):
    """
    Create an email message in the required format for Gmail API.
    """
    try:
        email_message = MIMEMultipart()
        email_message['To'] = recipient
        email_message['Subject'] = subject
        email_message['From'] = "your-email@gmail.com"  # Replace with your email
        email_message.attach(MIMEText(body, 'plain'))  # Plain text content
        encoded_message = urlsafe_b64encode(email_message.as_bytes()).decode("utf-8")
        return {"raw": encoded_message}
    except Exception as e:
        print("Error occurred while creating email:", e)
        print(traceback.format_exc())
        return None

def send_scheduling_email():
    """
    Send a scheduling email with suggested times.
    """
    try:
        # Load credentials (ensure token.json exists with correct scopes)
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
        gmail_service = build('gmail', 'v1', credentials=credentials)

        # Define email details
        recipient_name = "John Doe"  # Replace with recipient's name
        recipient_email = "recipient@example.com"  # Replace with recipient's email
        timezone_name = "America/Los_Angeles"  # Replace with recipient's time zone (e.g., PST)

        # Generate availability for the next 5 days
        utc_now = datetime.now(timezone.utc)
        suggested_times = [
            format_time_to_timezone(utc_now + timedelta(days=i, hours=9), timezone_name)
            for i in range(1, 6)
        ]

        # Create email content
        subject = "Scheduling a Meeting"
        body = (
            f"Hi {recipient_name},\n\n"
            f"I’d like to schedule a meeting with you. Here are my available times over the next 5 days:\n"
            + "\n".join(f"- {time}" for time in suggested_times) +
            "\n\nPlease let me know which time works best for you, or suggest an alternative time.\n\n"
            "Thank you,\nYour Name"
        )

        # Create and send the email
        email_body = create_email(recipient_email, subject, body)
        if email_body:
            response = gmail_service.users().messages().send(userId="me", body=email_body).execute()
            print(f"Scheduling email successfully sent to {recipient_email}. Response ID: {response['id']}")
        else:
            print("Failed to create the email.")

    except Exception as e:
        print("An error occurred while sending the scheduling email:")
        print(traceback.format_exc())

if __name__ == "__main__":
    send_scheduling_email()