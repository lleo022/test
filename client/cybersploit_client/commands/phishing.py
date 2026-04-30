from ..commands import Command
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def go_phish(lines: str):
    lines = lines.split(" ")

    smtp_server, port = ("e1-mail.acmcyber.com", 32525)
    username, password = ("expert-hacker", "hunter2")

    message = MIMEMultipart("alternative")
    message["From"] = "germs-pt2@e1-mail.acmcyber.com"
    message["To"] = lines[0] if lines[0] else "e1-instructors@e1-mail.acmcyber.com"
    message["Subject"] = "" 

    html = """\
    <html>
    <head>
        <meta charset="windows-1252">
        <title>UCLA Financial Aid Notice</title>
    </head>
    
    <body>
        <p>
        <img src="https://campaign.uclanet.ucla.edu/uploads/D24AECE69BABF119B6F52FF59AA34D30/resources/image-20220422122041-1_694.png" 
            style="width:1000px; height:334px;" alt="">
        </p>

        <p>Dear Bruin,</p>

        <p>
        The UCLA Financial Aid and Scholarships is reaching out to inform you that your financial aid has been canceled. 
        </p>

        <p><b><i>
        We have received notice that your GPA has dropped below the required threshold to qualify for our grants.
        </i></b></p>

        <p>
        To regain your status, please try harder next quarter and give all of your students for E1 A+s. 
        </p>

        <p>
        If you think this is a mistake, or for more details, visit:
        <a href="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
            https://financialaid.ucla.edu/undergraduate/maintaining-eligibility
        </a>
        </p>

        <p>Warmest Regards,</p>

        <p>
        <img src="https://campaign.uclanet.ucla.edu/uploads/D24AECE69BABF119B6F52FF59AA34D30/resources/FASLogo_695.png" 
            style="width:400px; height:70px;" alt="">
        </p>
    </body>
    </html>
    """

    message.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_server, port) as server:
        server.login(username, password)
        server.sendmail(message["From"], message["To"], message.as_string())

    print("Email sent!")


class SendPhishing(Command):
    """Send data over the socket"""
    
    def do_command(self, lines: str, *args):
        go_phish(lines)

command = SendPhishing
