#!/usr/bin/python2

import gtk
from dockbarx.applets import DockXApplet
from subprocess import Popen
from threading import Thread
import time
import socket

HOST = '127.0.0.1'
PORT = 8086
BUFFER_SIZE = 1024

class ProcessThread(Thread):
	
	def __init__(self, process):
		def target():
			self.process = Popen(process)
			self.process.wait()
		Thread.__init__(self, target=target)
	
	def stop(self):
		print 'stopped'
		self.process.terminate()

class StartMenuApplet(DockXApplet):
	"""An example applet for DockbarX standalone dock"""

	def __init__(self, dbx_dict):
		DockXApplet.__init__(self, dbx_dict)
		self.image = gtk.Image()
		self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
		self.add(self.image)
		self.image.show()
		
		self.active = False
		self.hover = False
		
		self.process = ProcessThread(['startmenu'])
		self.process.start()
		
		self.thread = Thread(target=self.update)
		self.thread.start()
		
		self.connect('enter-notify-event', self.on_mouse_over)
		self.connect('leave-notify-event', self.on_mouse_leave)
		self.connect('clicked', self.clicked)
		self.show()
	
	# Socket
	def send(self, argument):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((HOST, PORT))
		except socket.error, OSError:
			return
		s.send(argument.decode('utf-8'))
		data = s.recv(BUFFER_SIZE)
		s.close()
		return data
	
	# Update thread
	def update(self):
		while True:
			if self.hover:
				continue
			output = self.send('status')
			if output == '1':
				self.active = True
				self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
			else:
				self.active = False
				self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
			time.sleep(0.05)
	
	# Event handlers
	def clicked(self, widget, event):
		print 'clicked'
		if self.active or not self.hover:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
			self.send('hide')
			self.active = False
		else:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
			self.send('show')
			self.active = True
			self.hover = False
	
	def on_mouse_over(self, widget, event):
		self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
		self.hover = True
	
	def on_mouse_leave(self, widget, event):
		if not self.active:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
		self.hover = False

def get_dbx_applet(dbx_dict):
	applet = StartMenuApplet(dbx_dict)
	return applet
