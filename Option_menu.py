import tkinter
from language_db import Language_db


class Option_menu:
    def __init__(self, main_window):
        self.main_window = main_window


    def define_language_option(self):
        self.language_option = tkinter.OptionMenu(self.lang_option_frm, self.variable, *self.language_list)

    def pack_language_option(self):   
        self.language_option.pack(side='left')

    def get_langs_from_sql(self):
        self.language_list = ["Default"]
        self.variable = tkinter.StringVar(self.main_window.app)
        languages_sql = Language_db()
        langs_list = languages_sql.get_languages()
        for lang in langs_list:
            self.language_list.append(lang[0])

        self.variable.set(self.language_list[0])


    def option_frame(self):
        self.lang_option_frm = tkinter.Frame(self.frame_to_put_in)

    def pack_option_frame(self):
        self.lang_option_frm.pack(side='bottom')

    def add_language_button(self):
        self.add_button = tkinter.Button(self.lang_option_frm, text="New lang")
    
    def pack_add_language_button(self):
        self.add_button.pack(side='right')

    def display_widget(self, frame_to_put_in):
        self.frame_to_put_in = frame_to_put_in
        self.option_frame()
        self.get_langs_from_sql()
        self.define_language_option()
        self.add_language_button()
        self.pack_option_frame()
        self.pack_add_language_button()
        self.pack_language_option()


class Add_language_window:
    def __init__(self):
        self.language_window = tkinter.Toplevel()

    def add_lanugage_button(self):
        self.add_lang = tkinter.Button(self.language_window, text="Add language")

    def cancel_button(self):
        self.cancel = tkinter.Button

        



    