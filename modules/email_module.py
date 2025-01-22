from email.mime.text import MIMEText
import base64

def get_gmail_signature(gmail_service):
    """
    Retrieve the Gmail signature using Gmail API.
    """
    try:
        send_as_config = gmail_service.users().settings().sendAs().list(userId="me").execute()
        for send_as in send_as_config.get("sendAs", []):
            if send_as.get("isPrimary"):
                return send_as.get("signature", "")
        return ""
    except Exception as e:
        print(f"Error fetching Gmail signature: {e}")
        return ""

def create_email(recipient, subject, body, gmail_service):
    """
    Create and send an email.
    """
    try:
        signature = get_gmail_signature(gmail_service)
        full_body = f"{body}<br><br>{signature}" if signature else body
        message = MIMEText(full_body, "html")
        message['To'] = recipient
        message['Subject'] = subject
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        return {"raw": encoded_message}
    except Exception as e:
        print(f"Error creating email: {e}")
        return None
