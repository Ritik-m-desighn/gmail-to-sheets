import sys
import os
from gmail_service import get_gmail_service, get_unread_emails, mark_as_read
from email_parser import parse_message
from sheets_service import append_to_sheet, get_sheets_service
from config import SPREADSHEET_ID

def main():
    try:
        gmail_service, creds = get_gmail_service()
        messages = get_unread_emails(gmail_service)

        if not messages:
            print("No new unread emails to process.")
            return

        parsed_emails = []
        for msg in messages:
            full_msg = gmail_service.users().messages().get(userId='me', id=msg['id']).execute()
            data = parse_message(full_msg)
            parsed_emails.append(data)
            mark_as_read(gmail_service, msg['id']) # [cite: 32]

        sheets_service = get_sheets_service(creds)
        append_to_sheet(sheets_service, SPREADSHEET_ID, parsed_emails) # [cite: 51]
        print(f"Successfully processed {len(parsed_emails)} emails.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()