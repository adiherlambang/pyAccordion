from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from base64 import urlsafe_b64encode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
import mimetypes
from email import encoders
# from flask import current_app as app

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.modify']

class gmailServices:
    
    @staticmethod
    def create_message(sender, to, subject, message_text, cc=None, bcc=None):
        # Create an instance of MIMEMultipart
        message = MIMEText(message_text)

        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        if cc:
            message['cc'] = cc  # Add CC addresses
        if bcc:
            message['bcc'] = bcc  # Add BCC addresses
        # Attach the HTML part
        
        # Encode the bytes of the MIME message content
        raw_message = urlsafe_b64encode(message.as_bytes()).decode("utf-8")
        return {'raw': raw_message}

    @staticmethod
    def create_message_with_attachment(sender, to, subject, message_text, file_path,cc=None, bcc=None):
        """Create a message for an email."""
        message = MIMEMultipart()
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        if cc:
            message['cc'] = cc  # Add CC addresses

        if bcc:
            message['bcc'] = bcc  # Add BCC addresses
        
        html_part = MIMEText(f'{message_text}', 'html')
        message.attach(html_part)

        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            with open(file_path, 'rb') as f:
                message.attach(MIMEText(f.read().decode('utf-8'), _subtype=sub_type))
        elif main_type == 'image':
            with open(file_path, 'rb') as f:
                message.attach(MIMEImage(f.read(), _subtype=sub_type))
        elif main_type == 'audio':
            with open(file_path, 'rb') as f:
                message.attach(MIMEAudio(f.read(), _subtype=sub_type))
        else:
            with open(file_path, 'rb') as f:
                attachment = MIMEBase(main_type, sub_type)
                attachment.set_payload(f.read())
                encoders.encode_base64(attachment)
                attachment.add_header('Content-Disposition', f'attachment; filename={os.path.basename(file_path)}')
                message.attach(attachment)

        raw_message = urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}

    @staticmethod
    def send_email(app, service, sender, to, subject, body, attachment_path=None,cc_recipient=None,bcc_recipient=None):
        if attachment_path:
            app.logger.info(f"send email with attachment")
            message = gmailServices.create_message_with_attachment(sender, to, subject, body, attachment_path,cc_recipient,bcc_recipient)

            try:
                message = service.users().messages().send(userId="me", body=message).execute()
                app.logger.info(f"Message Id: {message['id']}")
                return message
            except Exception as error:
                app.logger.error(f"An error occurred: {error}")
        
        else:
            app.logger.info(f"send email without attachment")
            # app.logger.info(f"Message : {sender}, {to}, {subject}, {body},{cc_recipient},{bcc_recipient}")
            message = gmailServices.create_message(sender, to, subject, body,cc_recipient,bcc_recipient)
            
            try:
                sent_message = service.users().messages().send(userId="me", body={message}).execute()
                app.logger.info(f"Message Id: {message['id']}")
                return sent_message
            except Exception as error:
                app.logger.error(f"An error occurred: {error}")
            
    @staticmethod
    def testMail(app,to, subject, message_text, cc=None, bcc=None):
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
            sendEmail = gmailServices.send_email(app, service, message , subject, message_text, cc_recipient, bcc_recipient)

            return sendEmail

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            app.logger.info(f'An error occurred: {error}')
            return error
    
    @staticmethod
    def send_email_with_attachment(app,to, subject, message_text, cc=None, bcc=None, attachment_data=None, attachment_filename=None):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('./app/xetc/token.json'):
            creds = Credentials.from_authorized_user_file('./app/xetc/token.json')
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
            service = build('gmail', 'v1', credentials=creds)

            # Set up email details
            sender = 'dummyapiconnected@gmail.com'
            to = 'septian.adi@mastersystem.co.id'
            subject = subject
            body = message_text
            cc_recipient = "adiherl91@gmail.com"
            bcc_recipient = bcc

            # Specify the file path of the attachment
            attachment_path = attachment_filename

            # Send the email
            sendEmail = gmailServices.send_email(app, service, sender, to, subject, body, attachment_path,cc_recipient)
            
            return sendEmail
        
        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            app.logger.info(f'An error occurred: {error}')
            return error
