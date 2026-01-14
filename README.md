# Gmail to Google Sheets Automation

GITHUB-REPO +"(https://github.com/Ritik-m-desighn/gmail-to-sheets.git)"
GITHUB-REPO +"(https://youtu.be/6hSD8BA6pZk)"


  
## Overview
This Python-based system automates the process of fetching unread emails from Gmail and logging them into a Google Sheet. [cite_start]It uses OAuth 2.0 for secure access and maintains state to prevent duplicate entries [cite: 1-6].

## High-Level Architecture


1. **Trigger**: Script runs and authenticates via OAuth 2.0.
2. [cite_start]**Fetch**: Connects to Gmail API to retrieve messages with `is:unread` label[cite: 31].
3. [cite_start]**Parse**: Extracts Sender, Subject, Date, and Body; converts HTML to plain text[cite: 50].
4. [cite_start]**State Check**: Compares Email ID against `processed_ids.json` to prevent duplicates[cite: 71, 72].
5. [cite_start]**Append**: Adds new data to Google Sheets via Sheets API[cite: 51].
6. [cite_start]**Update**: Marks email as 'Read' in Gmail and updates the local state file[cite: 32].

## Setup Instructions
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. [cite_start]Place your `credentials.json` in the `credentials/` folder[cite: 40, 41].
4. Run `python src/main.py` and complete the OAuth flow in your browser.

## Technical Details
- [cite_start]**OAuth Flow**: Uses the `InstalledAppFlow` for local authorization, generating a `token.json` for session persistence[cite: 69].
- **Duplicate Prevention**: Every email has a unique `id`. We store processed IDs in `processed_ids.json`. [cite_start]Even if an email is marked "Unread" again, the script skips it if the ID exists in the file[cite: 71].
- [cite_start]**State Persistence**: Local JSON file storage was chosen for simplicity and to avoid the need for an external database for this scope[cite: 72].

## Challenges & Limitations
- **Challenge**: Handling giant email bodies that exceeded Google Sheets' 50,000 character limit.
- **Solution**: Implemented a truncation logic in `email_parser.py` to cap content at 20,000 characters.
- [cite_start]**Limitation**: The current state file is local; in a production environment, a database like PostgreSQL would be preferred for scalability[cite: 74].