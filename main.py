import kivy
from kivy.app import App

from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.config import ConfigParser
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image, CoreImage
from kivy.uix.scrollview import ScrollView
import sqlite3
import io

def read_sqlite_table():
    dbAll = []
    try:
        sqlite_connection = sqlite3.connect('data.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = """SELECT * FROM Student_Data WHERE par=?"""
        args = (-1,)
        cursor.execute(sqlite_select_query, args)
        dbAll = cursor.fetchall()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)

    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
    return dbAll


class MyGrid(BoxLayout):
    def __init__(self, **kwargs):
        
        super(MyGrid, self).__init__(**kwargs)
        self.orientation="vertical"
        self.contend_scroll_view = GridLayout(size_hint_y=None,row_default_height=60)
        self.contend_scroll_view.bind(minimum_height=self.contend_scroll_view.setter('height'))
        self.contend_scroll_view.cols = 1
        
        db = read_sqlite_table()
        
        textinput = TextInput(text='',
                              multiline=False, size_hint=(0.5, None))
        textinput.bind(on_text_validate=self.on_enter)
        self.contend_scroll_view.add_widget(textinput)
        for row in db:
            submit = Button(text=row[2], font_size=20, size_hint=(0.5, None), background_color=(0, 0, 1, 1))
            submit.id = row[0]
            submit.b = False
            submit.bind(on_press=self.pressed)
            self.contend_scroll_view.add_widget(submit)
        self.contend_scroll_view.prev_ids = [-1]
        self.scroll_view = ScrollView()
        self.scroll_view.add_widget(self.contend_scroll_view)
        self.add_widget(self.scroll_view)

    def on_enter(self, t):
        # clear grid
        self.contend_scroll_view.clear_widgets()
        self.contend_scroll_view.l = 0

        dbAll = []
        self.contend_scroll_view.prev_ids = [-1]

        textinput = TextInput(text=t.text,
                              multiline=False, size_hint=(0.5, None))
        textinput.bind(on_text_validate=self.on_enter)
        self.contend_scroll_view.add_widget(textinput)
        try:
            sqlite_connection = sqlite3.connect('data.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            sqlite_select_query = """SELECT * FROM Student_Data WHERE title LIKE ? AND img_blob IS NOT NULL"""
            args = ("%" + t.text + "%",)
            cursor.execute(sqlite_select_query, args)
            dbAll = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
        for row in dbAll:
            data = io.BytesIO(row[3])
            img = CoreImage(data, ext="png").texture

            widget = Image(size_hint=(1, None))
            widget.size=(500,300)
            widget.texture = img
            self.contend_scroll_view.add_widget(widget)
        back = Button(text="Back", font_size=20, size_hint=(0.5, None), background_color=(0, 0, 1, 1))
        back.b = True
        back.bind(on_press=self.pressed)
        self.contend_scroll_view.add_widget(back)


    def read_id(id):
        dbAll = []
        try:
            sqlite_connection = sqlite3.connect('data.db')
            cursor = sqlite_connection.cursor()
            print("Подключен к SQLite")
            sqlite_select_query = """SELECT * FROM Student_Data WHERE par=? """
            args = (id,)
            cursor.execute(sqlite_select_query, args)
            dbAll = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("Соединение с SQLite закрыто")
        return dbAll

    def pressed(self, instance):
        # clear grid
        self.contend_scroll_view.clear_widgets()
        self.contend_scroll_view.l = 0

        if instance.b == False:
            self.contend_scroll_view.prev_ids.append(instance.id)
        if len(self.contend_scroll_view.prev_ids) == 0:
            self.contend_scroll_view.prev_ids = [-1]
        elif instance.b == True:
            self.contend_scroll_view.prev_ids.pop()
        # print(self.prev_ids)
        textinput = TextInput(text='',
                              multiline=False, size_hint=(0.5, None))
        textinput.bind(on_text_validate=self.on_enter)
        self.contend_scroll_view.add_widget(textinput)
        if instance.b:
            try:
                instance.id = self.contend_scroll_view.prev_ids.pop()
            except:
                instance.id = -1
        db = MyGrid.read_id(instance.id)  # get button's child
        if len(db) > 0 and db[0][3] != None:
            data = io.BytesIO(db[0][3])
            img = CoreImage(data, ext="png").texture
            widget = Image(size_hint=(1, None))
            widget.size=(500,300)
            widget.texture = img
            self.contend_scroll_view.add_widget(widget)
        else:
            for row in db:
                submit = Button(
                    text=row[2], font_size=20, size_hint=(0.5, None), background_color=(0, 0, 1, 1))
                submit.id = row[0]
                submit.b = False
                submit.bind(on_press=self.pressed)
                self.contend_scroll_view.add_widget(submit)
        if instance.id != -1:
            back = Button(text="Back", font_size=20, size_hint=(0.5, None), background_color=(0, 0, 1, 1))
            back.b = True
            back.bind(on_press=self.pressed)
            self.contend_scroll_view.add_widget(back)


class Depot(App):
    def __init__(self, **kvargs):
        super(Depot, self).__init__(**kvargs)
        self.config = ConfigParser()

    def get_application_config(self):
        return super(Depot, self).get_application_config(
            '{}/%(appname)s.ini'.format(self.directory))

    def build(self):
        self.icon = 'myicon.png'
        return MyGrid()


if __name__ == "__main__":
    Depot().run()
