import asyncio
import logging
from pathlib import Path
from app.config import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class EmailService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            cls._instance.client = SendGridAPIClient(settings.sendgrid_api_key)
            cls._instance.from_email = settings.from_email

            templates_path = Path(__file__).parent.parent.parent / "templates"
            cls._instance.jinja = Environment(
                loader=FileSystemLoader(templates_path)
            )

            logger.info("EmailService initialized")

        return cls._instance

    async def send_email(self, to_email: str, subject: str, html: str) -> bool:
        message = Mail(
            from_email=self.from_email,
            to_emails=to_email, 
            subject=subject,
            html_content=html
        )
        try:
            response = await asyncio.to_thread(self.client.send, message)

            if 200 <= response.status_code < 300:
                logger.info("Email sent to %s (status %s)", to_email, response.status_code)
                return True
            else:
                logger.error(
                    "SendGrid returned non-success status %s for %s",
                    response.status_code,
                    to_email
                )
                return False

        except Exception as e:
            logger.exception("Failed to send email to %s: %s", to_email, e)
            return False

    def render_template(self, template_name: str, context: dict) -> str:
        template = self.jinja.get_template(template_name)
        return template.render(**context)

    async def send_welcome_email(self, to_email: str, username: str) -> bool:
        html = self.render_template(
            "welcome_email.html",
            {"username": username} 
        )
        return await self.send_email(
            to_email,
            "Welcome!",
            html
        )