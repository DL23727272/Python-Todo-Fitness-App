from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconLeftWidget, IconRightWidget
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.label import Label
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
import uuid
from database import Database
from kivy.core.window import Window

import subprocess
import os

class TaskBoddy(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = Database()
        self.mydialog = None

    def build(self):
        self.screen = Builder.load_file("main.kv")
        self.load_data()
        return self.screen

    def load_data(self):
        self.alldata = self.db.get_all_todos()
        for todo in self.alldata:
            self.add_todo_to_screen(todo)

    def addnewtodo(self, value):
        if value:
            todo_id = self.db.add_todo(value)
            self.add_todo_to_screen({"id": todo_id, "value": value})
        self.screen.ids.inputtodo.text = ""

    def add_todo_to_screen(self, todo):
        todo_id, value = todo["id"], todo["value"]
        todo_list = self.screen.ids.todo_list
        todo_item = OneLineAvatarIconListItem(
            IconLeftWidget(icon="pencil", on_release=lambda x: self.editbtn(todo_id, value)),
            IconRightWidget(icon="delete", on_release=lambda x: self.deletebtn(todo_id)),
            id=todo_id,
            text=value,
        )
        todo_list.add_widget(todo_item)

    def editbtn(self, todo_id, value):
        self.editcontent = MDTextField(hint_text="update name", mode="fill")
        self.mylayout = MDBoxLayout(
            orientation="vertical",
            size_hint_y=0.8,
            height=300
        )
        self.mylayout.add_widget(Label(text="edit data"))
        if not self.mydialog:
            self.dialog = MDDialog(
                title="edit data",
                type="custom",
                size_hint=(0.8, None),
                height=300,
                content_cls=self.mylayout,
                buttons=[
                    MDFlatButton(
                        text="save",
                        text_color="red",
                        on_release=lambda x: self.savenow(todo_id, self.editcontent.text)
                    )
                ]
            )
            self.mydialog = True
        self.dialog.content_cls.add_widget(self.editcontent)
        self.dialog.open()


    def savenow(self, todo_id, new_value):
        self.db.update_todo(todo_id, new_value)
        self.update_todo_in_screen(todo_id, new_value)
        self.notif = Snackbar(
            font_size=30,
            bg_color=(0, 0, 1, 1)
        )

        self.dialog.dismiss()
        self.notif.open()

    def update_todo_in_screen(self, todo_id, new_value):
        todo_list = self.screen.ids.todo_list
        for child in todo_list.children:
            if child.id == todo_id:
                child.text = new_value

    def deletebtn(self, todo_id):
        self.db.delete_todo(todo_id)
        self.remove_todo_from_screen(todo_id)

    def remove_todo_from_screen(self, todo_id):
        todo_list = self.screen.ids.todo_list
        for child in todo_list.children:
            if child.id == todo_id:
                todo_list.remove_widget(child)
                
    def logout_button(self):
            subprocess.Popen(["python", "login.py"])
            os._exit(0)
  
if __name__ == "__main__":
    Window.size = (368, 640)
    TaskBoddy().run()
