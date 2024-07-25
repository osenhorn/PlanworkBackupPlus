from kivymd.uix.screen import MDScreen


class Progresso(MDScreen):
    bar_color = ListProperty([1, 0, 100/255])
    bar_width = NumericProperty(10)
    set_value = NumericProperty(5)
    value = NumericProperty(45)
    counter = 0
    def __init__(self, **kwargs):
        super(Progresso, self).__init__(**kwargs)
        Clock.schedule_once(self.animate, 0)

    def animate(self, *args):
        Clock.schedule_interval(self.percent_counter, 1)

    def percent_counter(self, *args):
        if self.counter < self.value:
            self.counter += 1
        else:
            Clock.unschedule(self.percent_counter)