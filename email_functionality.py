import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config import *

# The mail addresses and password
# sender_address = gmail_address
# sender_pass = gmail_password
# receiver_address = receiver_address
#gmail_port_number=gmail_port_number
# from email.message import EmailMessage
def send_email(timestamp: str, actual_filename: str) -> str:
    try:
        #Setup the MIME
        message = MIMEMultipart()
        message['From'] = gmail_address
        message['To'] = receiver_address
        message['Subject'] = 'The required job list created at '+ timestamp   #The subject line
        message.attach(MIMEText('Please find attached excel with jobs!', 'plain'))

        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(actual_filename, "rb").read())
        encoders.encode_base64(part)
        header_value = 'attachment; filename="{}"'.format(actual_filename)
        part.add_header('Content-Disposition', header_value)
        message.attach(part)

        #Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', gmail_port_number) #use gmail with port
        session.starttls() #enable security
        session.login(gmail_address, gmail_password) #login with mail_id and password
        session.sendmail(gmail_address, receiver_address, message.as_string())
        session.quit()
        return 'Mail Sent'
    except Exception:
        return 'Mail not sent '+Exception