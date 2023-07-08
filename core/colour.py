from kivy.graphics import Rectangle
from kivy.uix.relativelayout import RelativeLayout

from core.card import p_size, img_p
from core.datapath import *


class Colours(RelativeLayout):
    def __init__(self, card=(100, 100), owner="", per=1, **kwargs):
        super(Colours, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.owner = owner
        self.card = card
        self.per = per
        self.colour_i = {}
        self.colours = ["y", "g", "r", "b"]
        self.colour_t = {}
        self.colour = ""
        self.ordered = False

        self.img_blank = f"atlas://{img_in}/other/blank"
        self.img_none = f"atlas://{img_in}/other/none"
        self.img_c = {"y": f"atlas://{img_in}/other/y", "g": f"atlas://{img_in}/other/g", "r": f"atlas://{img_in}/other/r", "b": f"atlas://{img_in}/other/b"}

        for c in self.colours:
            self.colour_t[c] = False

        with self.canvas:
            power_b = (img_p[0] * p_size * self.per, img_p[1] * p_size * self.per)
            space = (card[1] - power_b[1] * len(self.colours)) / 5
            for i in range(len(self.colours)):
                self.colour_i[str(i)] = Rectangle(source=self.img_blank, size=(power_b[1], power_b[1]), pos=((space + power_b[1]) * i - space / 2, 0))

            self.size = (card[1], power_b[1])
            self.height = power_b[1]
            self.width = card[1]

    def hide(self):
        with self.canvas:
            for i in range(len(self.colours)):
                self.colour_i[str(i)].source = self.img_blank

    def show(self):
        with self.canvas:
            for i in range(len(self.colour)):
                if self.colour_t[self.colour[i]]:
                    self.colour_i[str(i)].source = self.img_c[self.colour[i]]

    def update_colour(self, colours):
        for c in self.colour_t:
            self.colour_t[c] = False
        self.colour = ""

        for c in colours:
            self.colour_t[c[0].lower()] = True
            if not self.ordered:
                self.colour += c[0].lower()
        if self.ordered:
            for c in self.colours:
                if c in colours:
                    self.colour += c
        self.hide()
        self.show()
