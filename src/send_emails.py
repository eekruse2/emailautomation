import os
import smtplib
import pandas as pd
import json
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_template(template_path):
    """Load the email template from file."""
    with open(template_path, 'r') as file:
        return file.read()

def personalize_email(template, business_name):
    """Replace placeholders in the template with actual values."""
    # Replace the business name placeholder
    content = template.format(business_name=business_name)
    
    # Convert plain text to HTML with hyperlinks
    lines = content.split('\n')
    html_lines = []
    
    for line in lines:
        if line.strip() == '':
            html_lines.append('<br>')
        elif line.startswith('-'):
            # Handle bullet points
            html_lines.append(f'&bull;{line[1:]}<br>')
        elif 'LinkedIn' in line:
            # Add LinkedIn hyperlink
            line = line.replace('LinkedIn', '<a href="https://www.linkedin.com/in/eliana-kruse/">LinkedIn</a>')
            html_lines.append(f'{line}<br>')
        elif 'co-founder' in line.lower():
            # Add co-founder hyperlink
            line = line.replace('co-founder', '<a href="https://www.linkedin.com/in/sumanth-karnati/">co-founder</a>')
            html_lines.append(f'{line}<br>')
        else:
            html_lines.append(f'{line}<br>')
    
    html_content = '\n'.join(html_lines)
    return html_content

def save_draft(business_name, email, subject, body):
    """Save email draft to a file."""
    draft = {
        'business_name': business_name,
        'email': email,
        'subject': subject,
        'body': body,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Create drafts directory if it doesn't exist
    os.makedirs('drafts', exist_ok=True)
    
    # Save draft to a JSON file
    filename = f"drafts/{business_name.replace(' ', '_').lower()}_draft.json"
    with open(filename, 'w') as f:
        json.dump(draft, f, indent=2)
    print(f"Draft saved for {business_name} at {filename}")

def send_email(sender_email, sender_password, recipient_email, subject, body):
    """Send an email using SMTP."""
    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    # Add both plain text and HTML parts
    text_part = MIMEText(
        body.replace('<br>', '\n')
            .replace('&bull;', '- ')
            .replace('<a href="https://www.linkedin.com/in/eliana-kruse/">LinkedIn</a>', 'LinkedIn')
            .replace('<a href="https://www.linkedin.com/in/sumanth-karnati/">co-founder</a>', 'co-founder'),
        'plain'
    )
    html_part = MIMEText(f'<html><body>{body}</body></html>', 'html')
    
    msg.attach(text_part)
    msg.attach(html_part)

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {recipient_email}")
    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {str(e)}")

def main():
    # Load configuration from environment variables
    sender_email = "elianakruse@gmail.com"  # Your email address
    sender_password = os.getenv('GMAIL_APP_PASSWORD')  # Will be set up through .env file
    subject = os.getenv('EMAIL_SUBJECT', 'Seeking your inventory expertise - UW-Madison startup')

    # Paths
    csv_path = os.path.join('data', 'businesses.csv')
    template_path = os.path.join('templates', 'email_template.txt')

    # Load data and template
    try:
        df = pd.read_csv(csv_path)
        template = load_template(template_path)
    except Exception as e:
        print(f"Error loading files: {str(e)}")
        return

    # Process each business
    for _, row in df.iterrows():
        business_name = row['business_name']
        recipient_email = row['email']
        
        # Personalize email
        personalized_body = personalize_email(template, business_name)
        
        if recipient_email.lower() == 'not listed' or recipient_email.strip() == '':
            # Save as draft if email is not available
            save_draft(business_name, recipient_email, subject, personalized_body)
        else:
            # Save as draft for review
            save_draft(business_name, recipient_email, subject, personalized_body)
            print(f"\nDraft created for {business_name} ({recipient_email})")

    print("\nAll drafts have been created. To send the emails after review:")
    print("1. Check the 'drafts' directory for all email drafts")
    print("2. Review each draft")
    print("3. Run the send_approved_emails.py script when ready to send")

if __name__ == "__main__":
    main() 