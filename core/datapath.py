import sys
from os.path import join

if getattr(sys, 'frozen', False):
	# we are running in a |PyInstaller| bundle
	main_dir = sys._MEIPASS
	data_ex = "./data"
	img_ex = "./img"
	cache = join(sys._MEIPASS, "cache")
	data_in = join(sys._MEIPASS, "data")
	img_in = join(sys._MEIPASS, "img")
	font_in = join(sys._MEIPASS, "font")
else:
	# we are running in a normal Python environment
	main_dir = "."
	data_ex = "../data"
	img_ex = "../img"
	cache = "./cache"
	data_in = "./data"
	img_in = "./img"
	font_in = "./font"

font = "NotoSansJP-Regular.otf"