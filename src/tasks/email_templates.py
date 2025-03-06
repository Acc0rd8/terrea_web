from email.message import EmailMessage
from pydantic import EmailStr

from src.config import settings


def create_register_confirmation_template(email_to: EmailStr):
    """ Create register email template

    Args:
        email_to (EmailStr): User email

    Returns:
        EmailMessage: Email meesage for User
    """
    email = EmailMessage()
    
    email['Subject'] = 'Confirm Registration'
    email['From'] = settings.SMTP_USER
    email['To'] = email_to
    
    email.set_content(
        f'''
            <h1>Registration</h1>
            <p>You have been registred at Terrea Web</p>
        ''',
        subtype='html'
    )
    return email