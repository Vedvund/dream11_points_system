import email
import imaplib
import os
import smtplib
from datetime import datetime, timedelta, timezone
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from core.config import settings
from utils.helper.logger import setup_logging

email_logger = setup_logging()


class EmailClient:
    def __init__(self):
        self.email_address = settings.GMAIL_ACCOUNT
        self.app_password = settings.GMAIL_APP_PASSWORD

    # Method to send an email with HTML format and optional attachments
    def send_email(self, to_email, subject, html_message, attachments=None):
        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_message, 'html'))

        # Attach files if provided
        if attachments:
            for file_path in attachments:
                try:
                    with open(file_path, 'rb') as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename= {os.path.basename(file_path)}')
                    msg.attach(part)
                    email_logger.info(f"Attachment added: {file_path}")
                except Exception as e:
                    email_logger.error(f"Error attaching file {file_path}: {e}")

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()  # Secure the connection
                server.login(self.email_address, self.app_password)
                server.send_message(msg)
            email_logger.info("Email sent successfully!")
        except Exception as e:
            email_logger.error(f"Error sending email: {e}")

    # Method to receive emails from the past `n` minutes
    def receive_emails_from_last_n_minutes(self, minutes=10):
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(self.email_address, self.app_password)
            mail.select('inbox')

            # Calculate the date (IMAP uses date without time for search)
            date_since = (datetime.now() - timedelta(minutes=minutes)).strftime("%d-%b-%Y")
            email_logger.info(f"Searching emails SINCE {date_since}")

            # Search for emails since the calculated date
            result, data = mail.search(None, f'(SINCE "{date_since}")')
            if result != 'OK':
                email_logger.error("Failed to search emails")
                return

            mail_ids = data[0].split()
            email_found = False

            mails = []

            # Fetch and filter emails manually by time
            for mail_id in mail_ids:
                result, message_data = mail.fetch(mail_id, '(RFC822)')
                mail_details = {}
                for response_part in message_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Get the date of the email (timezone-aware)
                        email_date = email.utils.parsedate_to_datetime(msg['Date'])

                        # Convert current time to offset-aware datetime with the same timezone as the email
                        now_aware = datetime.now(timezone.utc).astimezone(email_date.tzinfo)

                        # Filter emails received within the last `n` minutes
                        if email_date >= now_aware - timedelta(minutes=minutes):
                            email_found = True
                            mail_details['subject'] = msg['subject']
                            mail_details['from'] = msg['from']

                            # Print the email body
                            if msg.is_multipart():
                                for part in msg.walk():
                                    if part.get_content_type() == "text/plain":
                                        body = part.get_payload(decode=True).decode()
                                        if body in mail_details:
                                            mail_details['body'] += f'{body}'
                                        else:
                                            mail_details['body'] = f'{body}'
                            else:
                                body = msg.get_payload(decode=True).decode()
                                mail_details['body'] = f'{body}'
                mails.append(mail_details)

            if not email_found:
                print(f"No emails found in the last {minutes} minutes.")
            return mails
        except Exception as e:
            email_logger.error(f"Error receiving email: {e}")


# Example usage:
if __name__ == "__main__":
    email_client = EmailClient()
    #
    # # Send an HTML email with optional attachments
    # html_message = "<h1>Test HTML Email</h1><p>This is a test email with <b>HTML</b> formatting.</p>"
    # attachments = ["path/to/file1.pdf", "path/to/file2.xlsx"]  # Optional attachments
    # email_client.send_email("vedvund@gmail.com", "HTML Email Test", html_message)
    #
    # # Receive emails from the past 30 minutes
    # all_mails = email_client.receive_emails_from_last_n_minutes(60)
    # for mail in all_mails:
    #     print(mail['subject'])
    #     print(mail['from'])
    #     print(mail['body'])
    #     print()
    # print()
