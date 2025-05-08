import os
import json
import glob
from send_emails import send_email
from dotenv import load_dotenv

def main():
    # Load environment variables
    load_dotenv()
    
    sender_email = "elianakruse@gmail.com"
    sender_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not sender_password:
        print("Error: GMAIL_APP_PASSWORD not found in .env file")
        return
    
    # Get all draft files
    draft_files = glob.glob('../drafts/*_draft.json')
    
    if not draft_files:
        print("No draft files found in the drafts directory")
        return
    
    print("\nAvailable drafts:")
    for i, draft_file in enumerate(draft_files, 1):
        with open(draft_file, 'r') as f:
            draft = json.load(f)
        print(f"{i}. {draft['business_name']} ({draft['email']})")
    
    while True:
        choice = input("\nEnter the number of the draft to send, 'all' to send all, or 'q' to quit: ")
        if choice.lower() == 'q':
            break
            
        if choice.lower() == 'all':
            print("\nPreparing to send all emails...")
            sent_count = 0
            failed_count = 0
            
            for draft_file in draft_files:
                with open(draft_file, 'r') as f:
                    draft = json.load(f)
                
                if draft['email'].lower() == 'not listed' or draft['email'].strip() == '':
                    print(f"Skipping {draft['business_name']} - no email address available")
                    failed_count += 1
                    continue
                
                print(f"\nSending email to {draft['business_name']} ({draft['email']})...")
                try:
                    send_email(
                        sender_email,
                        sender_password,
                        draft['email'],
                        draft['subject'],
                        draft['body']
                    )
                    sent_count += 1
                    print(f"Successfully sent email to {draft['business_name']}")
                except Exception as e:
                    print(f"Failed to send email to {draft['business_name']}: {str(e)}")
                    failed_count += 1
            
            print(f"\nEmail sending complete!")
            print(f"Successfully sent: {sent_count}")
            print(f"Failed: {failed_count}")
            break
        
        try:
            index = int(choice) - 1
            if 0 <= index < len(draft_files):
                with open(draft_files[index], 'r') as f:
                    draft = json.load(f)
                
                if draft['email'].lower() == 'not listed' or draft['email'].strip() == '':
                    print(f"Cannot send email to {draft['business_name']} - no email address available")
                    continue
                
                print(f"\nDraft for {draft['business_name']}:")
                print(f"To: {draft['email']}")
                print(f"Subject: {draft['subject']}")
                print("\nBody:")
                print(draft['body'].replace('<br>', '\n').replace('&bull;', '- '))
                
                confirm = input("\nSend this email? (yes/no): ")
                if confirm.lower() == 'yes':
                    send_email(
                        sender_email,
                        sender_password,
                        draft['email'],
                        draft['subject'],
                        draft['body']
                    )
                    print(f"Successfully sent email to {draft['business_name']}")
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            print("Please enter a valid number, 'all', or 'q' to quit.")

if __name__ == "__main__":
    main() 