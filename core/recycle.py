from kivy.properties import StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

from core.button import Button
from core.datapath import *
from core.label import Label


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


class MyText(Label):
	def __init__(self, **kwargs):
		super(MyText, self).__init__(**kwargs)
		self.halign = "center"
		self.valign = "middle"
		self.font_name = f"{font_in}/{font}"
		self.bind(on_size=self._update_size)

	def _update_size(self, *args):
		self.texture_update()
		self.height = self.texture_size[1]
		self.text_size = self.texture_size
		self.texture_update()
		self.size = self.texture_size


class RV(RecycleView):
	set_title = StringProperty("")
	download = StringProperty("")

	def __init__(self, **kwargs):
		super(RV, self).__init__(**kwargs)
		self.box = SelectableRecycleBoxLayout()
		self.add_widget(self.box)
		self.viewclass = "MyButton"
		self.data = []


class RVText(RecycleView):
	def __init__(self, **kwargs):
		super(RVText, self).__init__(**kwargs)
		self.box = SelectableRecycleBoxLayout()
		self.add_widget(self.box)
		self.viewclass = "MyText"
		self.data = []
