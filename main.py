import logging
from logging.handlers import SMTPHandler
from os import environ
from core.datapath import *
with open(f"{data_ex}/log", "w", encoding="utf-8") as log_file:
	pass
logging.basicConfig(filename=f"{data_ex}/log", level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
smtp_handler = SMTPHandler(mailhost=('smtp.totuccio.com', 587), fromaddr='tsws@totuccio.com', toaddrs=['tintedmoth@gmail.com'], subject='Error', credentials=('tsws@totuccio.com', 'error3mail'), secure=())
smtp_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(smtp_handler)
environ["KIVY_NO_CONSOLELOG"] = "1"
if platform == 'android':
	def permission_callback(permission, results):
		if all([result for result in results]):
			print("Got all permissions")  
		else:
			print("Did not get all permissions")
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
