import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_email(to_email: str, subject: str, body: str) -> str:
    """Send an email using Gmail SMTP with SSL encryption.
    
    Args:
        to_email (str): Recipient's email address
        subject (str): Email subject line
        body (str): Email body content
        
    Returns:
        str: Status message of the email operation
    """
    try:
        # Gmail SMTP settings with SSL
        smtp_server = "smtp.gmail.com"
        smtp_port = 465
        
        # Get credentials from environment variables
        sender_email = os.getenv("EMAIL_ADDRESS")
        app_password = os.getenv("EMAIL_APP_PASSWORD")

        # Verify credentials exist
        if not sender_email or not app_password:
            return "Failed to send email: Missing email credentials in .env file"
        
        # Create the email message
        msg = MIMEMultipart('alternative')
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject

        # Convert \n to <br> for HTML
        html_body = body.replace('\n', '<br>')
        html_content = f"""
        <html>
            <body>
                <p>{html_body}</p>
            </body>
        </html>
        """

        # Attach both plain text and HTML versions
        msg.attach(MIMEText(body, 'plain'))
        msg.attach(MIMEText(html_content, 'html'))

        # Use SSL connection
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            
        return f"Email sent successfully to {to_email}"
            
    except smtplib.SMTPAuthenticationError:
        return ("Failed to send email: Authentication failed. "
                "Please verify your Gmail credentials and App Password.")
    except Exception as e:
        return f"Failed to send email: {str(e)}"