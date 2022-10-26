from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from os import walk
from kivy.core.audio import SoundLoader
from kivy import platform
from kivy.properties import Clock
from kivy.graphics import Color, Ellipse, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.uix.progressbar import ProgressBar
#from jnius import autoclass
import os

class MainWidget(RelativeLayout):
    files = []
    dir_to_search = ""
    MUSIC = False
    b = None
    playing_music_dir = ""
    playing_music = None
    is_music_playing = False
    music_volume = 20
    create_playlist = False
    playlist_songs_internal = []
    playlist_object = None
    item_list = None
    added_playlist_songs = []
    active_button = None
    current_playlist_song = 0
    changing_music = False
    music_length_label = ""
    music_length = 0
    music_current_position = 0
    circular_progressBar = None
    playlist_Item = None
    current_playlist_item = None

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        if(platform == "android"):
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            
        else:
            self.dir_to_search = "Music/"

        #self.theme_cls.primary_palette = "Gray"
        #self.theme_cls.accent_palette = "Red"

    def on_toggle_button_state(self, widget):
        if widget.state == "normal":
            self.create_playlist = False
        else:
            self.reset_information()
            self.playlist_object = self.ids.main_grid.ids.playlist_view.ids.playlist_songs
            self.create_playlist = True

            self.MUSIC = not self.create_playlist
            if(platform == "android"):
                self.dir_to_search = os.path.join(os.getenv('EXTERNAL_STORAGE'), 'Music/')
            self.list_all_files()
            self.load_content()

    def list_all_files(self):
        for (dirpath, dirnames, filenames) in walk(self.dir_to_search):
            self.files.extend(filenames)
            break

    def load_content(self):
        for i in range(0,len(self.files)):
            fileName = str(self.files[i][0:self.files[i].find('.')])
            filename_extension = self.files[i]
            if(self.create_playlist):
                self.b=ToggleButton(value=i, text=fileName, size_hint=(None,None), size=(dp(100),dp(120)))
                self.b.bind(on_press = self.add_to_playlist)
                self.item_list.add_widget(self.b)
            else:
                self.b=Button(text=str(fileName), size_hint=(None,None), size=(dp(100),dp(120)))
                if(self.MUSIC):
                    self.b.bind(on_press = self.play_sound)
                self.item_list.add_widget(self.b)

            internal_song = (fileName, filename_extension)
            self.playlist_songs_internal.append(internal_song)

    def reset_information(self):
        print("reset information")
        self.files = []
        self.item_list = self.ids.main_grid.ids.scroll_view.ids.items_list
        self.item_list.clear_widgets()
        self.music_current_position = 0
        Clock.unschedule(self.status_update)
        self.MUSIC = False

    def play_sound(self, instance):
        if self.create_playlist:
            if(self.is_music_playing):
                Clock.unschedule(self.status_update)
                self.music_current_position = 0
                self.playing_music.stop()

            self.is_music_playing = True
            self.playing_music_dir = self.dir_to_search + self.find_music_in_playlist(instance)
            self.playing_music = SoundLoader.load(self.playing_music_dir)

            if(self.music_volume > 1):
                self.music_volume = self.music_volume / 100

            if (self.active_button != None):
                self.active_button.background_color = [1,1,1,1]
            
            self.active_button = instance
            self.active_button.background_color = [1,0,0,1]

            self.playing_music.volume = self.music_volume
            self.playing_music.play()
            self.current_playlist_item = instance.parent
            Clock.schedule_interval(self.status_update, 1)

    def status_update(self, instance):
        print("status_update")
        status = self.playing_music.status
        if status == 'stop':
            self.changing_music = True
        elif status == 'play':
            if(self.music_current_position < self.playing_music.length):
                self.music_current_position += 1 
                self.current_playlist_item.set_circular_progressbar_value(self.music_current_position)
        else:
            print("Music Ended")

    def add_to_playlist(self, instance):
        song = Button(text=instance.text, size_hint=(0.8,None), size=(dp(100),dp(50))) 
        song.bind(on_press = self.play_sound)
        playlist_progress_bar = ProgressBar(size_hint=(0.2,None),size=(dp(100),dp(50)))

        new_playlist_Item = PlaylistItem()
        new_playlist_Item.add_button(song)
        new_playlist_Item.add_progressbar(playlist_progress_bar) 
        self.playlist_object.add_widget(new_playlist_Item)

        print("playlist_Item added to main object: " + str(self.playlist_object.children))

    def find_music_in_playlist(self, instance):
        for i in range(0,len(self.playlist_songs_internal)):
            if(self.playlist_songs_internal[i][0] == instance.text):
                self.current_playlist_song = i
                return self.playlist_songs_internal[i][1]
    
    def on_slider_value(self, widget):
        self.music_volume = int(widget.value)/100
        if(self.is_music_playing):
            self.playing_music.volume = self.music_volume

class GridLayoutExample(StackLayout):
    pass

class StackLayoutView(StackLayout):
    pass

class PlaylistStakerView(StackLayout):
    pass

class PlaylistItem(StackLayout):
    playlist_button = None
    playlist_progressbar = None

    def __init__(self,  **kwargs):
        super(PlaylistItem, self).__init__(**kwargs)
        #self.parent = parent
        self.size_hint=(1,0.1)

    def add_button(self, instance):
        self.playlist_button = instance
        self.add_widget(self.playlist_button)

    def add_progressbar(self, instance):
        print("add_progressbar: " + str(instance))
        self.playlist_progressbar = instance
        self.add_circular_progressbar()
        self.add_widget(instance)

    def add_circular_progressbar(self):
        print("add_circular_progressbar")
        # Set constant for the bar thickness
        self.playlist_progressbar.thickness = 10
        # Create a direct text representation
        self.playlist_progressbar.label = CoreLabel(text=self.get_music_time(0), font_size=self.playlist_progressbar.thickness+5)
        # Initialise the texture_size variable
        self.playlist_progressbar.texture_size = None
        # Refresh the text
        self.refresh_circular_progressbar_text()
        # Redraw on innit
        self.draw_circular_progressbar()

    def draw_circular_progressbar(self):
        with self.playlist_progressbar.canvas:
            print("draw_circular_progressbar")
            # Empty canvas instructions
            self.playlist_progressbar.canvas.clear()
            # Draw no-progress circle
            Color(0.26, 0.26, 0.26)
            Ellipse(pos=self.playlist_progressbar.pos, size=self.playlist_progressbar.size)

            # Draw progress circle, small hack if there is no progress (angle_end = 0 results in full progress)
            Color(0, 1, 0)
            Ellipse(pos=self.playlist_progressbar.pos, size=self.playlist_progressbar.size,
                    angle_end=(0.001 if self.playlist_progressbar.value_normalized == 0 else self.playlist_progressbar.value_normalized*360))

            # Draw the inner circle (colour should be equal to the background)
            Color(0, 0, 0)
            Ellipse(pos=(self.playlist_progressbar.pos[0] + self.playlist_progressbar.thickness / 2, self.playlist_progressbar.pos[1] + self.playlist_progressbar.thickness / 2),
                    size=(self.playlist_progressbar.size[0] - self.playlist_progressbar.thickness, self.playlist_progressbar.size[1] - self.playlist_progressbar.thickness))

            Color(1, 1, 1, 1)
            Rectangle(texture=self.playlist_progressbar.label.texture, size=self.playlist_progressbar.texture_size,
                  pos=(self.playlist_progressbar.size[0] / 2 - self.playlist_progressbar.texture_size[0] / 2 + self.playlist_progressbar.pos[0], 
                        self.playlist_progressbar.size[1] / 2 - self.playlist_progressbar.texture_size[1] / 2 + self.playlist_progressbar.pos[1]))

    def refresh_circular_progressbar_text(self):
        self.playlist_progressbar.label.refresh()
        self.playlist_progressbar.texture_size = list(self.playlist_progressbar.label.texture.size)

    def set_circular_progressbar_value(self, value):
        self.playlist_progressbar.value = value
        self.playlist_progressbar.label.text = self.get_music_time(value)
        self.refresh_circular_progressbar_text()
        self.draw_circular_progressbar()
    
    def get_music_time(self, seconds):
        minutes = seconds // 60
        seconds %= 60
        return "%02i:%02i" % (minutes, seconds)
  
class BookShelfApp(App):
    pass

if __name__ == "__main__":
    BookShelfApp().run()