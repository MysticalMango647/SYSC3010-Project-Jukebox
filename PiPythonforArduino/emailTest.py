import smtplib

subject='song played'
bodyText="""\
song played
"""
SMTP_SERVER='smtp.gmail.com'
SMTP_PORT=465
USERNAME='emailtestsend3@gmail.com'
PASSWORD='emailTestSend!'
RECIEVER_EMAIL='emailtestrecieve@gmail.com'

headers = ["From: " + USERNAME, "Subject: " + subject, "To: " + RECIEVER_EMAIL,
"MIME-Version: 1.0", "Content-Type: text/html"]
headers = "\r\n".join(headers)

session=smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
#session.ehlo()
session.login(USERNAME, PASSWORD)
session.sendmail(USERNAME, RECIEVER_EMAIL, headers + "\r\n\r\n" + bodyText)
session.quit()
print("Email sent")