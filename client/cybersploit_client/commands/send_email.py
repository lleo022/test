from ..commands import Command
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def go_phish(lines: str):
    recipient_parts = lines.split(" ")

    smtp_server, port = ("e1-mail.acmcyber.com", 32525)
    username, password = ("expert-hacker", "hunter2")

    message = MIMEMultipart("alternative")
    message["From"] = "germs-pt2@e1-mail.acmcyber.com"
    message["To"] = recipient_parts[0] if recipient_parts[0] else "e1-instructors@e1-mail.acmcyber.com"
    message["Subject"] = "UCLA Giveaway Demo Notification"

    html = """\
    <html>
    <head>
        <meta charset="UTF-8">
        <title>You Won the Scooter Giveaway!</title>
    </head>
    
    <body>

        <p>Dear Bruin,</p>

        <p>
        Congratulations! You've won the 
        <b> scooter giveaway</b> from The Mark LA. 
        </p>

        <p>
        <b>No action is required.</b> 
        </p>

    

        <p>Best,</p>
        <p>The Mark</p>
    </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(username, password)
        server.sendmail(message["From"], message["To"], message.as_string())

    print("Email sent!")


class SendPhishing(Command):
    """
    Sends a demo email.

    Usage:
    phishing test@example.com
    """
    
    def do_command(self, lines: str, *args):
        go_phish(lines)


command = SendPhishing