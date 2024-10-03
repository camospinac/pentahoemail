import os
import base64
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
def authenticate_gmail():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials_support.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def send_email(creds, to, subject, body, cc=None, bcc=None):
    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    if cc:
        message['cc'] = cc
    if bcc:
        message['bcc'] = bcc
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
    try:
        message = service.users().messages().send(
            userId='me', body={'raw': raw_message}).execute()
        print(f'Message sent to {to}')
        if cc:
            print(f'CC sent to {cc}')
        if bcc:
            print(f'BCC sent to {bcc}')
    except Exception as e:
        print(f'An error occurred: {e}')


creds = authenticate_gmail()
send_email(creds, 'dsuesca@link2know.co', 'Prueba de email desde soporte--2', 'Email enviado desde python.--2', 
               cc='ygonzalez@link2know.co, ygomez@link2know.co, agonzalez@link2know.co, ytorres@link2know.co', bcc='')
