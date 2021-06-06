import sys
from os.path import join

if getattr(sys, 'frozen', False):
	main_dir = sys._MEIPASS
	data_ex = "./data"
	img_ex = "./img"
	data_in = join(sys._MEIPASS, "data")
	img_in = join(sys._MEIPASS, "img")
	font_in = join(sys._MEIPASS, "font")
else:
	main_dir = "."
	data_ex = "../data"
	img_ex = "../img"
	data_in = "./data"
	img_in = "./img"
	font_in = "./font"

font = "NotoSansJP-Regular.otf"