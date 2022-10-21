from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.metrics import dp

class MainWidget(RelativeLayout):
     def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

class StackLayoutView(StackLayout):
    def __init__(self, **kwargs):
        super(StackLayoutView, self).__init__(**kwargs)
        #self.orientation="lr-bt"
        for i in range(1,101):

            b=Button(text=str(i), size_hint=(None,None), size=(dp(100),dp(100)))
            self.add_widget(b)

class BookShelfApp(App):
    pass

BookShelfApp().run()