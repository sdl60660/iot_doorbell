#Solution based on: https://gist.github.com/mr-pj/75297864abef5c8f2d5c134be2656023#file-dashbutton-py
#pydhcplib code: https://github.com/dgvncsz0f/pydhcplib/blob/master/pydhcplib/dhcp_basic_packet.py

import datetime, time

import send_update
import datetime

from pydhcplib.dhcp_network import *

def send_texts():
	current_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
	print 'Button pressed at: ' + current_time
	send_update.main()

netopt = {'client_listen_port': "68", 'server_listen_port': "67", 'listen_address': "0.0.0.0"}

class Server(DhcpServer):
	def __init__(self, options, dashbuttons):
		DhcpServer.__init__(self, options["listen_address"],
								options["client_listen_port"],
								options["server_listen_port"])
		self.dashbuttons = dashbuttons

	def HandleDhcpRequest(self, packet):
		f = open('last_press.txt', 'rU')
		last_press = f.readline()
		last_press = datetime.datetime.strptime(last_press, '%Y-%m-%d %H:%M:%S.%f')
		print datetime.datetime.now() - last_press
		if datetime.datetime.now() - last_press > datetime.timedelta(seconds=15):
			print 'sending...'
			print
			mac = self.hwaddr_to_str(packet.GetHardwareAddress())
			#print packet.source_address
			f = open('last_press.txt', 'w')
			f.writelines(str(datetime.datetime.now()))
			self.dashbuttons.press(mac)


	def hwaddr_to_str(self, hwaddr):
		result = []
		hexsym = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']
		for iterator in range(6) :
			result += [str(hexsym[hwaddr[iterator]/16]+hexsym[hwaddr[iterator]%16])]
		return ':'.join(result)

class DashButtons():
	def __init__(self):
		self.buttons = {}

	def register(self, mac, function):
		self.buttons[mac] = function

	def press(self, mac):
		if mac in self.buttons:
			self.buttons[mac]()
			return True
		return False

		
dashbuttons = DashButtons()
dashbuttons.register('ac:63:be:cb:c8:b2', send_texts)
server = Server(netopt, dashbuttons)

while True :
    server.GetNextDhcpPacket()