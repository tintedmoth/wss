from kivy.app import App
from kivy.base import stopTouchApp
from kivy.clock import Clock
from kivy.uix.widget import Widget
from plyer import email

from core.datapath import *


class EmailApp(App):
	def build(self):
		parent = Widget()
		return parent

	def send_error(self, version="", room="", *args):
		log = open(f"{data_ex}/log", "r", encoding="utf-8")
		text = ""
		p = False
		for line in log.readlines():
			if "error" in line.lower():
				p = True
			if p:
				text += line
		email.send(recipient="tsws@totuccio.com",
		           subject=f"Error in tews {version} {room}",
		           text=text,
		           create_chooser=False)
		Clock.schedule_once(self.end, 1)

	def send_email(self, *args):
		email.send(recipient="tews@totuccio.com",
		           subject="",
		           text="",
		           create_chooser=False)

	def stop(self, *largs):
		self.root_window.close()
		return super(EmailApp, self).stop(*largs)

	def end(self, dt):
		stopTouchApp()

	def on_pause(self):
		return True
