#!/usr/bin/python2

import gtk
from dockbarx.applets import DockXApplet
from subprocess import Popen
from threading import Thread

class ProcessThread(Thread):
	
	def __init__(self, process, cb):
		def target():
			print 'start'
			self.process = Popen(process)
			self.process.wait()
			cb()
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
		self.thread = None
		self.process = None
	
	def process_cb(self):
		self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
		self.active = False
		self.thread = None
	
	def clicked(self, widget, event):
		print 'clicked'
		if self.active:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')
			if self.thread:
				self.thread.stop()
				self.thread = None
			self.active = False
		elif not self.thread:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
			self.thread = ProcessThread(['startmenu'], self.process_cb)
			self.thread.start()
			self.active = True
	
	def on_mouse_over(self, widget, event):
		self.image.set_from_file('/usr/share/dockbarx/applets/startmenu-active.png')
	
	def on_mouse_leave(self, widget, event):
		if not self.active:
			self.image.set_from_file('/usr/share/dockbarx/applets/startmenu.png')

def get_dbx_applet(dbx_dict):
	applet = StartMenuApplet(dbx_dict)
	return applet
