from dotenv import load_dotenv
import os
from email_tools import send_email

load_dotenv()

def test_email_connection():
    """Test email sending with SSL connection"""
    
    print("\nTesting email connection...")
    result = send_email(
        to_email="webdevpiyush.07@gmail.com",
        subject="Test Email",
        body="This is a test email using SSL connection."
    )
    print(result)

if __name__ == "__main__":
    test_email_connection()