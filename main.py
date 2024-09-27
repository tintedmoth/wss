import logging
from datetime import datetime
from logging.handlers import SMTPHandler
from os import environ

from kivy.config import Config

from core.datapath import *
from core.mail import *

with open(f"{data_ex}/log", "w", encoding="utf-8") as log_file:
	pass
logging.basicConfig(filename=f"{data_ex}/log.log", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
smtp_handler = SMTPHandler(mailhost=(mailadd[0], 587), fromaddr=mailadd[1], toaddrs=[mailadd[3]], subject='Error', credentials=(mailadd[1], mailadd[2]), secure=())
smtp_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(smtp_handler)

environ["KIVY_NO_CONSOLELOG"] = "1"

if platform == 'android':
	from android.permissions import Permission, request_permissions

	request_permissions([Permission.INTERNET, Permission.ACCESS_WIFI_STATE, Permission.ACCESS_NETWORK_STATE,Permission.WRITE_EXTERNAL_STORAGE])


Config.set("graphics", "fullscreen", "auto")
import kivy.core.window as window

window.Window.clearcolor = (0, 0, 0, 1.)
from core.gameapp import GameApp

gameapp = GameApp()

if __name__ in ("__android__", "__main__"):
	try:
		gameapp.run()
	except Exception as e:
		smtp_handler.subject = f"Error {mail[0]} {mail[1]} {e} {datetime.now()}"
		logging.exception(f"Got exception on main handler.", exc_info=True)
