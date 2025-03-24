import datetime
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
from dotenv import load_dotenv

load_dotenv()
__from = os.getenv("USR")
__passwd = os.getenv("PASSWD")
__to = os.getenv("RECEIVER")


def send_email(title, body, attachment_path):
    msg = MIMEMultipart()

    msg["Subject"] = (
        f'Envio automático {title}\
    {datetime.date.today().strftime("%d/%m/%Y")}'
    )

    msg["From"] = __from

    msg["To"] = __to

    msg.attach(
        MIMEText(body, "HTML"),
    )

    with open(attachment_path, "rb") as arquivo:
        att = MIMEBase("application", "octet-stream")
        att.set_payload(arquivo.read())
        encoders.encode_base64(att)

        att.add_header(
            "Content-Disposition",
            f"attachment; filename={attachment_path.split('/')[-1]}",
        )
    msg.attach(att)
    __send_email(msg)


# portas (587 - 465) -> gmail

# with smtplib.SMTP('smtp.gmail.com', 465) as smtp:


def __send_email(message):
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        try:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(__from, __passwd)
            smtp.sendmail(__from, __to, message.as_string())
            print(f"{time.strftime('%X')} >> email enviado")
        except Exception as e:
            print(f"{time.strftime('%X')} >> {e}")
