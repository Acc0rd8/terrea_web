from pydantic import EmailStr
from smtplib import SMTP_SSL, SMTPAuthenticationError

from src.tasks.celery import app_celery
from src.tasks.email_templates import create_register_confirmation_template
from src.config import settings
from src.logger import logger


@app_celery.task
def send_register_confirmation_email(email_to: EmailStr):
    """ Send register email

    Args:
        email_to (EmailStr): User email
    """
    msg = create_register_confirmation_template(email_to) # Creating email message template
    try:
        with SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASS)
            server.send_message(msg) # Sending message on User email
            
            logger.info(msg='The message has been sent') # log
    except SMTPAuthenticationError as e:
        msg = 'SMTPAuthenticationError'
        extra = {'Error': e}
        logger.critical(msg=msg, extra=extra) # log
