from kivy.uix.widget import Widget
class StackSpacer(Widget):
	def __init__(self, o=(100, 100), **kwargs):
		super(StackSpacer, self).__init__(**kwargs)
		self.size_hint = (None, None)
		self.width = o[0]
		self.height = o[1]
		self.size_o = o
		self.size = o
		self.bind(size=self._update_rect, pos=self._update_rect)
	def _update_rect(self, inst, *args):
		self.height = inst.size[1]
		self.width = inst.size[0]
