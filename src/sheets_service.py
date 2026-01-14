from googleapiclient.discovery import build

def get_sheets_service(creds):
    return build('sheets', 'v4', credentials=creds, static_discovery=False)

def append_to_sheet(service, spreadsheet_id, email_data):
    if not email_data:
        return

    # Critical: Ensure this is a list of lists (one list per row)
    values = []
    for e in email_data:
        row = [
            str(e['from']), 
            str(e['subject']), 
            str(e['date']), 
            str(e['content'])
        ]
        values.append(row)

    body = {'values': values}

    # Use 'RAW' instead of 'USER_ENTERED' if you want exactly what is in the string
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A1", # Use A1; 'append' automatically finds the next empty row
        valueInputOption="RAW", 
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()