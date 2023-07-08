from kivy.properties import BooleanProperty, ObjectProperty, ListProperty, NumericProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput as Ti
from kivy.app import App

from core.button import Button
from core.datapath import *


class TextInput(Ti):
	cid = ""

	def __init__(self, cid="", **kwargs):
		super(TextInput, self).__init__(**kwargs)
		self.cid = cid
		self.font_name = f"{font_in}/{font}"
		self.multiline = False
		self.padding = [12, 3, 3, 3]
		self.bind(size=self._update_rect)

	def _update_rect(self, inst, value):
		self.height = inst.size[1]
		self.width = inst.size[0]


class CustomDropDown(DropDown):
	force_below = BooleanProperty(False)  

	def __init__(self, **kwargs):
		super(CustomDropDown, self).__init__(**kwargs)
		self.do_not_reposition = False  

	def _reposition(self, *largs):
		if self.do_not_reposition:
			return
		super(CustomDropDown, self)._reposition(*largs)
		if self.force_below:
			self.make_drop_below()

	def make_drop_below(self):
		self.do_not_reposition = True  
		if self.attach_to is not None:
			wx, wy = self.to_window(*self.attach_to.pos)
			wy += App.get_running_app().app.sd["popup"]["popup"].pos[1]
			self.height = wy  
			self.top = wy  
		self.do_not_reposition = False  


class SuTextInput(TextInput):
	code_inp = ObjectProperty()
	flt_list = ObjectProperty()
	word_list = ListProperty()
	starting_no = NumericProperty(3)
	suggestion_text = ''
	trait_btn = {}

	def __init__(self, notes=('Features', 'Suggestions', 'Abbreviations', 'Miscellaneous'),**kwargs):
		super(SuTextInput, self).__init__(**kwargs)

		self.dropdown = CustomDropDown(force_below=True)
		for note in notes:
			self.trait_btn[note] = Button(text=note, size_hint_y=None, height=30)

			self.trait_btn[note].bind(on_release=lambda btn: self.dropdown.select(btn.text))

			self.dropdown.add_widget(self.trait_btn[note])

		self.dropdown.bind(on_select=lambda instance, x: setattr(self, 'text', x))

	def filter_dropdown(self,widget,text):
		self.dropdown.clear_widgets()
		for btn in [_ for _ in self.trait_btn if text.lower() in _.lower()]:
			self.dropdown.add_widget(self.trait_btn[btn])

	def on_text(self, instance, value):
		if self.dropdown.parent is None and self.get_parent_window() is not None:
			self.dropdown.open(self)

	def keyboard_on_key_down(self, window, keycode, text, modifiers):
		if self.suggestion_text and keycode[1] == 'tab':
			self.insert_text(self.suggestion_text + ' ')
			return True
		return super(SuTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)
