from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from database import Database
import subprocess
import os
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.clock import Clock
from database import Database
import subprocess
import os

Window.size = (368, 640)


class Login(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.db = Database()
        global sm 
        sm = ScreenManager()
        sm.add_widget(Builder.load_file("splash.kv"))
        sm.add_widget(Builder.load_file("login.kv"))
        return sm
    
    def on_start(self):
        Clock.schedule_once(self.login, 5)
        
    def login(self, *args):  
        sm.current = "login" 
        
    def validate_login(self):
       
        username = self.root.get_screen("login").ids.Username.text
        password = self.root.get_screen("login").ids.Password.text
        
        if not username or not password:
            self.root.get_screen("login").ids.error_label.text = "Empty username or password"
            return
        
        if self.db.check_user(username, password):
            subprocess.Popen(["python", "main.py"])
            os._exit(0)
        else:
            self.root.get_screen("login").ids.error_label.text = "Invalid credentials"

    def validate_signup(self):
       
        username = self.root.get_screen("login").ids.Username.text
        password = self.root.get_screen("login").ids.Password.text
        
        if not username or not password:
            self.root.get_screen("login").ids.error_label.text = "Empty username or password"
            return
        
        signup_successful = self.db.signup(username, password)
        if signup_successful:
            self.root.get_screen("login").ids.error_label.text = "Signup successful"
        else:
            self.root.get_screen("login").ids.error_label.text = "Username already exists"
        

if __name__=="__main__":
    Login().run()