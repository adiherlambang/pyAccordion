from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from flask import current_app as app

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class gmailServices:

    @staticmethod
    def create_message(sender, to, subject, message_text,cc=None, bcc=None):
        message = MIMEMultipart()
        
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject

        if cc:
            message['cc'] = cc  # Add CC addresses

        if bcc:
            message['bcc'] = bcc  # Add BCC addresses
        
        # text_part = MIMEText(message_text, 'plain')
        # message.attach(text_part)
        
        html_part = MIMEText(f'<html><body><p>{message_text}</p></body></html>', 'html')
        message.attach(html_part)

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {'raw': raw_message}

    @staticmethod
    def send_email(app, service, user_id, message):
        try:
            sent_message = service.users().messages().send(userId=user_id, body=message).execute()
            service.users().messages().modify(userId=user_id, id=sent_message['id'], body={'addLabelIds': ['SENT']}).execute()
            app.logger.info(f"Message sent: {sent_message['id']}")
            return message
        except Exception as e:
            app.logger.info(f"An error occurred: {e}")
            return e

    @staticmethod
    def main(app,to, subject, message_text, cc=None, bcc=None):
        """Shows basic usage of the Gmail API.
        Lists the user's Gmail labels.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('./app/xetc/token.json'):
            creds = Credentials.from_authorized_user_file('./app/xetc/token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    './app/xetc/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('./app/xetc/token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            # Call the Gmail API
            service = build('gmail', 'v1', credentials=creds)
            # Compose the email
            sender = 'dummyapiconnected@gmail.com'
            recipient = to
            cc_recipient = cc
            bcc_recipient = bcc
            subject = subject
            message_text = message_text

            message = gmailServices.create_message(sender, recipient, subject, message_text, cc_recipient, bcc_recipient)

            # Send the email
            sendEmail = gmailServices.send_email(app, service, 'me', message)

            return sendEmail

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            app.logger.info(f'An error occurred: {error}')
            return error
    