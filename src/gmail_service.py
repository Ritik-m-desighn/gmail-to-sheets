import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/spreadsheets']
STATE_FILE = 'processed_ids.json'

def get_gmail_service():
    creds = None
    # Token storage logic [cite: 48, 60]
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds), creds

def get_unread_emails(service):
    # Fetch unread emails from Inbox [cite: 30, 31]
    results = service.users().messages().list(userId='me', q='is:unread label:INBOX').execute()
    messages = results.get('messages', [])
    
    # State Persistence Logic 
    processed_ids = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            processed_ids = json.load(f)
    
    # Filter out IDs already in our local state 
    new_messages = [m for m in messages if m['id'] not in processed_ids]
    return new_messages

def mark_as_read(service, msg_id):
    service.users().messages().modify(
        userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}
    ).execute()
    
    # Save ID to state file to prevent duplicates 
    processed_ids = []
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            processed_ids = json.load(f)
    processed_ids.append(msg_id)
    with open(STATE_FILE, 'w') as f:
        json.dump(processed_ids, f)