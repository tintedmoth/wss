import logging
from logging.handlers import SMTPHandler
from os import mkdir, environ
from os.path import exists

from core.datapath import *

if not exists(data_ex):
	mkdir(data_ex)

with open(f"{data_ex}/log", "w",encoding="utf-8") as log_file:
	pass
logging.basicConfig(filename=f"{data_ex}/log", level=logging.DEBUG,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
smtp_handler = logging.handlers.SMTPHandler(mailhost=('smtp.totuccio.com', 587), fromaddr='tsws@totuccio.com', toaddrs=['tintedmoth@gmail.com'], subject='Error', credentials=('tsws@totuccio.com','error3mail'), secure=())
smtp_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(smtp_handler)

environ["KIVY_NO_CONSOLELOG"] = "1"

from kivy.utils import platform

if platform == 'android':
	from android.permissions import request_permissions, Permission, check_permission
	# request_permissions([Permission.INTERNET, Permission.ACCESS_WIFI_STATE, Permission.ACCESS_NETWORK_STATE])

	# https://www.youtube.com/watch?v=okpiDnSR4z8
	def permission_callback(permission, results):
		if all([result for result in results]):
			print("Got all permissions")  # ,writable dir = ", primary_external_storage_path())
		else:
			print("Did not get all permissions")

	# Ensures that the permissions are checked before proceeding
	# while not (check_permission(Permission.WRITE_EXTERNAL_STORAGE) and check_permission(Permission.READ_EXTERNAL_STORAGE)):
	# 	print("Both perms granted?: ", check_permission(Permission.WRITE_EXTERNAL_STORAGE) and check_permission(Permission.READ_EXTERNAL_STORAGE))
	# 	request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE], permission_callback)

from kivy.config import Config

Config.set("graphics", "fullscreen", "auto")

import kivy.core.window as window
from core.mail import mail
from core.gameapp import GameApp

window.Window.clearcolor = (0, 0, 0, 1.)
gameapp = GameApp()

if __name__ in ("__android__", "__main__"):
	try:
		gameapp.run()
	except:
		logging.exception(f"Got exception on main handler {mail[0]} {mail[1]}")
