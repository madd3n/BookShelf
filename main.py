from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '600')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from os import walk
from kivy.core.audio import SoundLoader
from kivy import platform
from android.permissions import request_permissions, Permission
from kivy.properties import Clock
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


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        
    def on_toggle_button_state(self, widget):
        if widget.state == "normal":
            self.create_playlist = False
        else:
            self.reset_information()
            self.playlist_object = self.ids.main_grid.ids.playlist_view.ids.playlist_songs
            self.create_playlist = True

    def load_music_button_pressed(self):
        self.reset_information()

        if(platform == "android"):
            
            request_permissions([Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE])
            self.dir_to_search = os.path.join(os.getenv('EXTERNAL_STORAGE'), 'Music')
        else:
            self.dir_to_search = "Music/"

        self.MUSIC = not self.create_playlist
        self.list_all_files()
        self.load_content()
    
    def list_all_files(self):
        for (dirpath, dirnames, filenames) in walk(self.dir_to_search):
            self.files.extend(filenames)
            break

    def load_content(self):
        for i in range(0,len(self.files)):
            if(self.create_playlist):
                fileName = str(self.files[i][0:self.files[i].find('.')])
                filename_extension = self.files[i]
                self.b=ToggleButton(text=fileName, size_hint=(None,None), size=(dp(100),dp(120)))
                self.b.bind(on_press = self.add_to_playlist)

                internal_song = (fileName, filename_extension)
                self.playlist_songs_internal.append(internal_song)
                self.item_list.add_widget(self.b)
            else:
                self.b=Button(text=str(self.files[i]), size_hint=(None,None), size=(dp(100),dp(120)))
                if(self.MUSIC):
                    self.b.bind(on_press = self.play_sound)
                self.item_list.add_widget(self.b)

    def reset_information(self):
        self.files = []
        self.item_list = self.ids.main_grid.ids.scroll_view.ids.items_list
        self.item_list.clear_widgets()
        self.MUSIC = False

    def play_sound(self, instance):
        if(self.is_music_playing):
            self.playing_music.stop()

        self.is_music_playing = True
        self.playing_music_dir = self.dir_to_search + self.find_music_in_playlist(instance)
        self.playing_music = SoundLoader.load(self.playing_music_dir)

        self.playing_music.bind(on_play=self.status_update)
        self.playing_music.bind(on_stop=self.status_update)
        Clock.schedule_interval(self.status_update, .1)

        if(self.music_volume > 1):
            self.music_volume = self.music_volume / 100

        if (self.active_button != None):
            self.active_button.background_color = [1,1,1,1]
        
        self.active_button = instance
        self.active_button.background_color = [1,0,0,1]

        self.playing_music.volume = self.music_volume
        self.playing_music.play()

    def status_update(self, instance):
        status = self.playing_music.status
        if status == 'stop' and not self.changing_music:
            self.changing_music = True
            print('User Stopped')
        elif status == 'play':
            s = ''
            #self.user_stopped = False
        else:
            print('End of stream')

    def add_to_playlist(self, instance):
        song = Button(text=instance.text, size_hint=(1,None), size=(dp(100),dp(50)))
        song.bind(on_press = self.play_sound)
        self.playlist_object.add_widget(song)

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
    def __init__(self, **kwargs):
        super(StackLayoutView, self).__init__(**kwargs)
    
class BookShelfApp(App):
    pass

if __name__ == "__main__":
    BookShelfApp().run()