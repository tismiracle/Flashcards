import tkinter
from Flashcards_list import *
from StartGame import Start_game
from db_connector import Sql_db


class Window():
    window_size = "400x400"

    def create_tk_instance(self):
        self.app = tkinter.Tk()

    def clear_window(self): 
        print("window cleared")
        _list = self.app.winfo_children()   
        for buttons in _list:
            buttons.destroy()

    def render_window(self):
        self.create_tk_instance()
        self.app.geometry(self.window_size)
    

#######################################################################################################################
    
class Menu_Layout():

    def __init__(self):
        self.window = Window()
        self.db_connector = Sql_db()
    
    def create_flashcards_list_menu_instance(self):
        self.flashcards_list_menu_instance = Flashcards_List(self.window, self)


    def check_state_of_start_button(self):
        records = self.db_connector.check_len_of_db()
        if records[0][0] > 0:
            self.start.configure(state="active")
        else:
            self.start.configure(state="disabled")

           

    def create_label(self):
        self.author = tkinter.Label(text="Created by Radoslaw Rylko")
        self.author.pack()

    def start_program(self):
        self.window.render_window()

        self.create_flashcards_list_menu_instance()
        self.window.app.mainloop()








