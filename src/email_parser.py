import base64
import re

def parse_message(message):
    payload = message.get('payload', {})
    headers = payload.get('headers', [])

    subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
    sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
    date = next((h['value'] for h in headers if h['name'] == 'Date'), 'No Date')

    body_data = ""
    # Look for plain text first, then html
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                body_data = part['body'].get('data', '')
                break
        if not body_data: # Fallback to HTML if plain text missing
             for part in payload['parts']:
                if part['mimeType'] == 'text/html':
                    body_data = part['body'].get('data', '')
                    break
    else:
        body_data = payload.get('body', {}).get('data', '')

    content = ""
    if body_data:
        content = base64.urlsafe_b64decode(body_data).decode('utf-8', errors='ignore')
        
        # CLEANING: Remove HTML tags using Regex
        content = re.sub('<[^<]+?>', '', content) 
        # CLEANING: Replace multiple newlines with a single one
        content = re.sub(r'\n\s*\n', '\n', content)
        # TRUNCATE: Keep it under Google's cell limit
        content = content[:20000]

    return {
        'from': sender,
        'subject': subject,
        'date': date,
        'content': content.strip()
    }