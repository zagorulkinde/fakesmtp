import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

msg = MIMEMultipart()
msg['From'] = 'zi@gmail.com'
msg['To'] = 'dimon689@gmail.com'
msg['Subject'] = 'simple email in python'
message = 'here is the email'
msg.attach(MIMEText(message))

mailserver = smtplib.SMTP('localhost', 1026)
mailserver.sendmail('zo@me.com','zi@me.com',msg.as_string())

mailserver.quit()
