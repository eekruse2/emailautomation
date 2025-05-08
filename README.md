# Email Automation System

This project automates the process of sending personalized emails to multiple recipients using data from a CSV file.

## Project Overview

The system will:
1. Read business information from a CSV file containing business names and email addresses
2. Use a customizable email template
3. Personalize the email by inserting the business name
4. Send the customized email to each recipient's email address

## File Structure
- `data/` - Directory containing the CSV file with business information
- `templates/` - Directory containing email templates
- `src/` - Source code for the email automation system
- `requirements.txt` - Python dependencies

## CSV File Format
The CSV file should contain the following columns:
- `business_name` - Name of the business
- `email` - Email address of the business

## Email Template
The email template will be a text file that can include placeholders for personalization, such as `{business_name}` which will be replaced with the actual business name.

## Setup Instructions
1. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your CSV file in the `data/` directory
3. Create your email template in the `templates/` directory
4. Configure your email settings (SMTP server, credentials, etc.)
5. Run the automation script

## Usage
```bash
python src/send_emails.py
```

## Security Note
- Never commit sensitive information like email credentials to the repository
- Use environment variables or a secure configuration file for storing credentials 