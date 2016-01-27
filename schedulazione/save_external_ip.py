#!/usr/bin/python
import smtplib
import commands
import sqlite3
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

flag_sent_mail = 0;
insert_message = "";
#CONNECT DB LOCAL 
try:
        conn = sqlite3.connect('db_sent_email.db')
        c = conn.cursor()
        c.execute("SELECT external_ip FROM save_external_ip WHERE id = (SELECT MAX(id) FROM save_external_ip);")
        row = c.fetchone()
        new_ip=commands.getstatusoutput('sudo upnpc -s | grep ^ExternalIPAddress | cut -c21-');
        if new_ip[1] != row[0]:
		local_ip = commands.getstatusoutput('sudo upnpc -s | grep ^Local\ LAN\ ip\ address | cut -c24-');
                external_ip = commands.getstatusoutput('sudo upnpc -s | grep ^ExternalIPAddress | cut -c21-');
                bit_rate = commands.getstatusoutput(' sudo upnpc -s | grep ^MaxBitRateDown | cut -c18-');
                byte_up_down = commands.getstatusoutput('sudo upnpc -s | grep ^Bytes| cut -c10-');
                packet_up_down = commands.getstatusoutput('sudo upnpc -s | grep ^Packets | cut -c10-');
                time_started = commands.getstatusoutput('upnpc -s | grep ^\ \ Time\ started'); 
                query = "INSERT INTO save_external_ip (local_ip, external_ip, bit_rate, byte_up_down, packet_up_down, time_started) VALUES ('"+ local_ip[1] + "', '"+ external_ip[1] + "', '"+ bit_rate[1] + "', '"+ byte_up_down[1] + "', '"+ packet_up_down[1] + "', '"+ time_started[1] + "')"; 
                c.execute(query);
                conn.commit();
		flag_sent_mail = 1;
		insert_message = "Il tuo nuovo indirizzo ip esterno: " + external_ip[1] + ".\nl' indrizzo local del rasberry e: " +local_ip[1];
		insert_message = insert_message + ".\n il BIT RATE attuale: MaxBitRateDown " +  bit_rate[1] + ".\nTotale BYTE RICEVUTI E INVIATI: " + byte_up_down[1];
		insert_message = insert_message + ".\n Totale Pacchetti inviati e ricevuti: " + packet_up_down[1] + ", \n Il tempo totale della connessione con indirizzio ip attuale: " + time_started[1];
		insert_message = insert_message + "\n PER COLLEGARE CON TRANSMISSION VAI SU: http://"+external_ip[1] +":9091";
		insert_message = insert_message + "\n PER COLLEGARE CON SSH COLLEGATI DAL TERMINALE CON SSH: ssh neptune_pi@"+external_ip[1]+" -p 22 \n \n"
        else: 
		flag_sent_mail =0;
	new_ip=commands.getstatusoutput('sudo upnpc -s | grep ^ExternalIPAddress | cut -c21-');
	byte_up_down=commands.getstatusoutput('sudo ifconfig eth0 | awk "/RX\ bytes/ "');
	rx_packets= commands.getstatusoutput('sudo ifconfig eth0 | awk "/RX\ packets/ "');
	tx_packets = commands.getstatusoutput('sudo ifconfig eth0 | awk "/TX\ packets/ "');
	packet_up_down = rx_packets[1] + " ,  " +tx_packets[1];  
	query_internal = "INSERT INTO internal_data (external_ip, packet_up_down, byte_up_down) VALUES ('" + new_ip[1] + "', '" +packet_up_down + "', '"+byte_up_down[1] + "');";
	c.execute(query_internal);
	conn.commit(); 
	insert_message = insert_message + "I dati del RASPBERRY: "
	insert_message = insert_message + "\n Totale BYTE RICEVUTI E INVIATI: " + byte_up_down[1] + "\nTotale Pacchetti inviati e ricevuti: " + packet_up_down
	insert_message = insert_message + "\n \n \n \n Best Regards. \n Singh Sukhjinder. \n Home Admin"
except conn.Error, e:
        print "Error %s" % e.args[0]
        sys.exit(1)
finally:
    if conn:
        conn.close() 
if flag_sent_mail==1:
	# DATI DEL RECEIVERS E DI SENDER
	sender = '******@gmail.com'
	receivers = ['******@gmail.com', '*******@hotmail.it'];
	msg = MIMEMultipart('alternative');
	msg['Subject'] = "External IP ADDRESS AS CHANGE ";
	msg['From'] = sender;
	msg['To'] = ", ".join(receivers) ;

	#ATTACH MESSAGE DI TIPO TEXT
	messaggeBody = MIMEText(insert_message, 'plain');
	msg.attach(messaggeBody);

	#CONFIGURAZIONI
	username = '******';
	password = '******';
	try:
	   smtpObj = smtplib.SMTP('smtp.gmail.com:587')
	   smtpObj.starttls()
	   smtpObj.login(username,password)
	   smtpObj.sendmail(sender, receivers, msg.as_string())        
	   smtpObj.quit() 
	except smtplib.SMTPException:
	   print "Error: unable to send email"
