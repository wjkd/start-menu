#!/usr/bin/python2

import gtk
from dockbarx.applets import DockXApplet
from subprocess import Popen, call, check_output, CalledProcessError
from threading import Thread
import time

def do(args):
	try: call(args)
	except CalledProcessError: pass

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
		
		self.connect('enter-notify-event', self.on_mouse_over)
		self.connect('leave-notify-event', self.on_mouse_leave)
		self.connect('clicked', self.clicked)
		self.show()
		
		self.active = False
		self.started = False
		
	def start_process(self):
		self.process = ProcessThread(['startmenu'])
		self.process.start()
		
		self.thread = Thread(target=self.update)
		self.thread.start()
		self.started = True
	
	def update(self):
		while True:
			try:
				output = check_output(['startmenuctl', 'status'])
			except CalledProcessError:
				output = '0'
			if output == '1':
				self.active = True
				self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
			else:
				self.active = False
				self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
			time.sleep(0.5)
	
	def clicked(self, widget, event):
		print 'clicked'
		if self.active:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
			do(['startmenuctl', 'hide'])
			self.active = False
		else:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
			if not self.started:
				self.start_process()
			do(['startmenuctl', 'show'])
			self.active = True
	
	def on_mouse_over(self, widget, event):
		self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
	
	def on_mouse_leave(self, widget, event):
		if not self.active:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')

def get_dbx_applet(dbx_dict):
	applet = StartMenuApplet(dbx_dict)
	return applet
