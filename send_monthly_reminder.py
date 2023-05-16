"""Script to send monthly reminder to enter meter readings in the app."""

from datetime import datetime

from mako.template import Template

from email_service.src.mail.mail import Mail
from email_service.src.mail.utils import get_env_var
from src.constants import FRENCH_MONTHS

CURRENT_MONTH = datetime.now().month
EMAILS = get_env_var("EMAILS").split(",")
ATTACHMENT_PATHS: list = []
MAIL_SUBJECT = "Rappel: relevés d'index"


for email in EMAILS:
    html_template = Template(filename="mail_content.html")
    html_content = html_template.render(
        user=email.split("@")[0], month=FRENCH_MONTHS[CURRENT_MONTH].lower()
    )
    mail = Mail(
        attachment_paths=ATTACHMENT_PATHS,
        html_content=html_content,
        emails=[email],
        mail_subject=MAIL_SUBJECT,
    )
    mail.send()
