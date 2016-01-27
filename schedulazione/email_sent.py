#!/usr/bin/python
import smtplib
import commands
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# prima di eseguire questo codice upnpc devo installarlo apt-get install miniupnpc
#ip = commands.getstatusoutput('sudo upnpc -s | grep ^ExternalIPAddress | cut -c21-')
ip = commands.getstatusoutput('sudo upnpc -s')
sender = 'email_del_persona che invia' # quello che manda la mail
receivers = ['secondo_email', 'primo_email'] #quelli che ricevono
msg = MIMEMultipart('alternative')
msg['Subject'] = "Indirrizio IP del Raspberry"
msg['From'] = sender
msg['To'] = ", ".join(receivers) 
text = "Hi!\n \n il tuo indirizzio ip di casa : " + ip[1]
ifconfig = commands.getstatusoutput('sudo ifconfig')

text = text + "\n \n Il commando ifconfig del raspberry: \n \n" + ifconfig[1]

messaggeBody = MIMEText(text, 'plain')
msg.attach(messaggeBody)

username = 'email' # in questo caso username del gmail
password = 'password_email'
try:
   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
   smtpObj.starttls()
   smtpObj.login(username,password)
   smtpObj.sendmail(sender, receivers, msg.as_string())        
   smtpObj.quit()
   print "Successfully sent email"
except smtplib.SMTPException:
   print "Error: unable to send email"
