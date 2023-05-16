"""Module to send mail with attachments."""

import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from dotenv import load_dotenv

from email_service.src.mail.constants import PASSWORD, PORT, SENDER, SERVER
from email_service.src.mail.utils import get_env_var

load_dotenv()


class Mail:
    """Class to send mail with attachments."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        emails: list,
        attachment_paths: list,
        text_content: str = "",
        html_content: str = "",
        mail_subject: str = "Newsletter",
    ):
        """
        Initialize the class.

        Parameters
        ----------
        emails: list
            List of emails to send the mail to.
        attachment_paths: list
            List of paths to the attachments.
        text_content: str
            Text content of the mail.
        html_content: str
            HTML content of the mail.
        """
        self.emails = emails
        self.attachment_paths = attachment_paths
        self.content = {"text": text_content, "html": html_content}
        self.mail_subject = mail_subject

    @staticmethod
    def add_attachment(mail, attachment_paths: list):
        """Add attachments to the mail."""
        for filepath in attachment_paths:
            mime_base = MIMEBase("application", "octet-stream")
            with open(filepath, "rb") as file:
                mime_base.set_payload(file.read())
            encoders.encode_base64(mime_base)
            mime_base.add_header(
                "Content-Disposition",
                f"attachment; filename={Path(filepath).name}",
            )
            mail.attach(mime_base)

    def attach_content(self, mail):
        """Add content to mail."""
        html_content = MIMEText(self.content["html"], "html")
        text_content = MIMEText(self.content["text"], "plain")

        mail.attach(text_content)
        mail.attach(html_content)

    @staticmethod
    def create_mail_service():
        """Create the mail service."""
        ssl_context = ssl.create_default_context()
        service = smtplib.SMTP_SSL(
            host=get_env_var(SERVER),
            port=get_env_var(PORT),
            context=ssl_context,
        )
        service.login(user=get_env_var(SENDER), password=get_env_var(PASSWORD))
        return service

    def send(self):
        """
        Create the mail and send it.

        Log in to the SMTP server.
        Construct the mail (subject, from, to) and attach the content.
        Attach the attachments.
        Send the mail.
        """
        service = self.create_mail_service()

        for email in self.emails:
            mail = MIMEMultipart("alternative")
            mail["Subject"] = self.mail_subject
            mail["From"] = get_env_var(SENDER)
            mail["To"] = email

            self.attach_content(mail)
            self.add_attachment(mail, self.attachment_paths)
            service.sendmail(
                from_addr=get_env_var(SENDER),
                to_addrs=email,
                msg=mail.as_string(),
            )

        service.quit()
