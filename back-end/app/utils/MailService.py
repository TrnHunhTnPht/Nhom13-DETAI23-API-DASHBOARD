import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendOTP(receiver_email, otp):
    sender_email = "thcstrandainghiaphat8a2@gmail.com"
    sender_password = "lwvnaaxxntumcryy"
    
    subject = "Verify"
    message = otp

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
