__all__ = ["SMTPRepository"]

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from email_validator import validate_email, EmailNotValidError
from jinja2 import Template

from src.config import settings


class SMTPRepository:
    def __init__(self):
        self._server = smtplib.SMTP(settings.SMTP.SERVER, settings.SMTP.PORT)

    def context_manager(self):
        self._server.starttls()
        self._server.login(settings.SMTP.USERNAME, settings.SMTP.PASSWORD.get_secret_value())
        yield
        self._server.quit()

    def send(self, message: str, to: str):
        try:
            valid = validate_email(to)
            to = valid.normalized
        except EmailNotValidError as e:
            raise ValueError(e)

        with self.context_manager():
            self._server.sendmail(settings.SMTP.USERNAME, to, message)

    def send_connect_email(self, email: str, auth_code: str):
        mail = MIMEMultipart("related")
        # Jinja2 for html template
        main = Template(
            """
            <html>
                <body>
                    <p>Hi!</p>
                    <p>Here is your temporary code for registration: {{ code }}</p>
                </body>
            </html>
            """,
            autoescape=True,
        )

        html = main.render(code=auth_code)
        msgHtml = MIMEText(html, "html")
        mail.attach(msgHtml)

        mail["Subject"] = "Registration in Monitoring Service"
        mail["From"] = settings.SMTP.USERNAME
        mail["To"] = email

        with self.context_manager():
            self._server.sendmail(settings.SMTP.USERNAME, email, mail.as_string())
