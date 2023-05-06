import aiosendgrid
from .config import Settings
from sendgrid.helpers.mail import Content, Email, Mail, To

config=Settings()

async def send_mail(from_address, to_address, subject, content, content_type="text/plain"):
    from_email = Email(from_address,)
    to_email = To(to_address)
    content = Content(content_type, content)
    mail = Mail(from_email, to_email, subject, content)
    async with aiosendgrid.AsyncSendGridClient(api_key=config.mail) as client:
        return await client.send_mail_v3(body=mail.get())