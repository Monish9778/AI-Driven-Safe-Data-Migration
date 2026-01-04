import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT

def send_alert(error_message: str) -> None:
    msg = MIMEText(error_message)
    msg["Subject"] = "Production Data Migration Error"
    msg["From"] = "migration.alerts@fintechcorp.com"
    msg["To"] = "data.ops@fintechcorp.com"

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.send_message(msg)
