import sys
from os import mkdir
from os.path import join,exists
from kivy.utils import platform

if platform == 'android':
	from android.storage import app_storage_path

	def get_cache_directory_path():
		from android import mActivity
		context = mActivity.getApplicationContext()
		result = context.getExternalCacheDir()
		if result:
			return str(result.toString())
		else:
			return "./cache"

	main_dir = "."
	data_ex = app_storage_path()
	cache = get_cache_directory_path()
	data_in = "./data"
	img_in = "./img"
	font_in = "./font"
elif getattr(sys, 'frozen', False):
	main_dir = sys._MEIPASS
	data_ex = "./data"
	cache = "./cache"
	data_in = join(sys._MEIPASS, "data")
	img_in = join(sys._MEIPASS, "img")
	font_in = join(sys._MEIPASS, "font")
else:
	main_dir = "."
	data_ex = "./cache/data"
	cache = "./cache"
	data_in = "./data"
	img_in = "./img"
	font_in = "./font"

font = "NotoSansJP-Regular.otf"

if not exists(cache):
	mkdir(cache)
if not exists(data_ex):
	mkdir(data_ex)

