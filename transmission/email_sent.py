#!/usr/bin/python
import smtplib
import commands
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender = 'email della persone che invia'
receivers = ['primo ricevitore', 'secondo ricevitore']
msg = MIMEMultipart('alternative')
msg['Subject'] = "Transmission File "
msg['From'] = sender
msg['To'] = ", ".join(receivers) 
# Legge un file.
in_file = open(sys.argv[1],"r")
text = in_file.read()
in_file.close()
#close file
messaggeBody = MIMEText(text, 'plain')
msg.attach(messaggeBody)

username = 'in questo caso username del gmail'
password = 'passwrod del email'
try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
   smtpObj.starttls()
   smtpObj.login(username,password)
   smtpObj.sendmail(sender, receivers, msg.as_string())        
   smtpObj.quit()
   print "Successfully sent email"
except smtplib.SMTPException:
   print "Error: unable to send email"
