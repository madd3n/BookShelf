from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from os import walk
from kivy.core.audio import SoundLoader

class MainWidget(RelativeLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

    files = []
    dir_to_search = ""
    MUSIC = False
    b = None
    playing_music_dir = ""
    playing_music = None
    is_music_playing = False
    music_volume = 20
    def load_button_pressed(self):
        self.reset_information()
        self.dir_to_search = self.ids.main_grid.ids.text_input_txt.text
        self.list_all_files()
        self.load_content()
    
    def load_image_button_pressed(self):
        self.reset_information()
        self.dir_to_search = "Images/"
        self.list_all_files()
        self.load_content()
        
    def load_music_button_pressed(self):
        self.reset_information()
        self.dir_to_search = "Music/"
        self.MUSIC = True
        self.list_all_files()
        self.load_content()
    
    def list_all_files(self):
        for (dirpath, dirnames, filenames) in walk(self.dir_to_search):
            self.files.extend(filenames)
            break

    def load_content(self):
        for i in range(0,len(self.files)):
            self.b=Button(text=str(self.files[i]), size_hint=(None,None), size=(dp(100),dp(120)))

            if(self.MUSIC):
                self.b.bind(on_press = self.play_sound)
            
            self.ids.main_grid.ids.scroll_view.ids.items_list.add_widget(self.b)

    def reset_information(self):
        self.files = []
        self.ids.main_grid.ids.scroll_view.ids.items_list.clear_widgets()
        self.MUSIC = False

    def play_sound(self, instance):
        if(self.is_music_playing):
            self.playing_music.stop()

        self.is_music_playing = True
        self.playing_music_dir = self.dir_to_search + instance.text
        self.playing_music = SoundLoader.load(self.playing_music_dir)

        if(self.music_volume > 1):
            self.music_volume = self.music_volume / 100

        self.playing_music.volume = self.music_volume
        self.playing_music.play()
        
    
    def on_slider_value(self, widget):
        print(int(widget.value))
        self.music_volume = int(widget.value)/100
        if(self.is_music_playing):
            self.playing_music.volume = self.music_volume

class GridLayoutExample(StackLayout):
    pass

class StackLayoutView(StackLayout):
    def __init__(self, **kwargs):
        super(StackLayoutView, self).__init__(**kwargs)
    
class BookShelfApp(App):
    pass

BookShelfApp().run()