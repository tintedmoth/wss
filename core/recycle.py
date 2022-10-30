from kivy.properties import StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from core.button import Button
from core.datapath import *
class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
	def __init__(self, **kw):
		super().__init__(**kw, orientation="vertical", size_hint_y=None)
		self.bind(minimum_height=self._hmin)
	def _hmin(self, inst, val):
		self.height = val
class MyButton(Button):
	def __init__(self, **kwargs):
		super(MyButton, self).__init__(**kwargs)
		self.halign = "center"
		self.valign = "middle"
		self.font_name = f"{font_in}/{font}"
	def on_press(self):
		self.parent.parent.set_title = self.id
class RV(RecycleView):
	set_title = StringProperty("")
	download = StringProperty("")
	def __init__(self, **kwargs):
		super(RV, self).__init__(**kwargs)
		self.box = SelectableRecycleBoxLayout()
		self.add_widget(self.box)
		self.viewclass = "MyButton"
		self.data = []
