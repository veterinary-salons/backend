from django.core import mail

from authentication.models import EmailCode


def get_recovery_code(email):
    code, created = EmailCode.objects.get_or_create(email=email)
    return code

def send_email_message(
    subject: str, message: str, sender: str, recipients: list
):
    with mail.get_connection() as connection:
        message = mail.EmailMessage(
            subject,
            message,
            sender,
            recipients,
            connection=connection,
        )
        messages_sent = message.send()
    return messages_sent
