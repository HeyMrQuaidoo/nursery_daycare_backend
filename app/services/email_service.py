from fastapi import status
from email.mime.text import MIMEText
from fastapi.exceptions import HTTPException
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from smtplib import SMTP_SSL, SMTPAuthenticationError

from app.core.config import template_path, settings
from app.modules.auth.schema.auth_schema import EmailBody


class EmailSendException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            headers=None,
        )


class EmailService:
    def __init__(self):
        self.EMAIL = settings.EMAIL
        self.EMAIL_PASSWORD = settings.EMAIL_PASSWORD
        self.SERVER = settings.EMAIL_SERVER
        self.template_path = template_path
        self.env = Environment(loader=FileSystemLoader(template_path))

    async def send_email(self, body: EmailBody):
        try:
            msg = MIMEMultipart()
            msg["Subject"] = body.subject
            msg["From"] = f"{settings.APP_NAME} <{self.EMAIL}>"
            msg["To"] = body.to
            msg.attach(MIMEText(body.message, "html"))

            port = 465  # 587 for TLS , 465 For SSL

            # Connect to the email server
            with SMTP_SSL(self.SERVER, port) as server:
                server.ehlo()
                server.login(self.EMAIL, self.EMAIL_PASSWORD)
                server.sendmail(self.EMAIL, body.to, msg.as_string())

            return {"message": "Email sent successfully"}
        except SMTPAuthenticationError as e:
            raise EmailSendException(detail=str(e))

    def render_template(self, template_name: str, **context):
        template = self.env.get_template(template_name)

        return template.render(context)

    async def send_template_email(
        self, to: str, subject: str, template_name: str, **context
    ):
        html_content = self.render_template(template_name, **context)
        body = EmailBody(to=to, subject=subject, message=html_content)

        try:
            await self.send_email(body)
        except EmailSendException as e:
            error_message = f"Error sending email: {e.detail}"
            raise HTTPException(status_code=500, detail=error_message)

    async def send_user_email(
        self, user_email: str, user_name: str, verify_link: str, subscription_link: str
    ):
        return await self.send_template_email(
            to=user_email,
            subject="New Account Created",
            template_name="confirmEmail.html",
            first_name=user_name,
            user_email=user_email,
            verify_link=verify_link,
            unsubscribe_link=subscription_link,
        )

    async def send_welcome_email(
        self, user_email: str, username: str, link: str, subscription_link: str
    ):
        return await self.send_template_email(
            to=user_email,
            subject=f"Welcome to {settings.APP_NAME}",
            template_name="welcome.html",
            first_name=username,
            user_email=user_email,
            reset_link=link,
            unsubscribe_link=subscription_link,
        )

    async def send_reset_password_email(
        self, email: str, username: str, reset_link: str, subscription_link: str
    ):
        return await self.send_template_email(
            to=email,
            subject="Reset Password Request",
            template_name="passwordReset.html",
            first_name=username,
            user_email=email,
            reset_link=reset_link,
            unsubscribe_link=subscription_link,
        )
