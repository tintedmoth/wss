import logging
from os import mkdir, environ
from os.path import exists

from core.datapath import *

if not exists(data_ex):
	mkdir(data_ex)

with open(f"{data_ex}/log", "w") as log_file:
	pass
logging.basicConfig(filename=f"{data_ex}/log", level=logging.DEBUG)

environ["KIVY_NO_CONSOLELOG"] = "1"

from android.permissions import request_permissions, Permission

request_permissions([Permission.INTERNET, Permission.ACCESS_WIFI_STATE, Permission.ACCESS_NETWORK_STATE])

from kivy.config import Config

Config.set("graphics", "fullscreen", "auto")

import kivy.core.window as window
from kivy.base import EventLoop
from kivy.cache import Cache
from core.emailapp import EmailApp
from core.gameapp import GameApp

window.Window.clearcolor = (0, 0, 0, 1.)
gameapp = GameApp()

if __name__ in ("__android__", "__main__"):
	try:
		gameapp.run()
	except:
		logging.exception("Got exception on main handler")
		emailapp = EmailApp()
		emailapp.send_error(gameapp.version, gameapp.netroom)
