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

    def show_list_button_commands(self):
        self.window.clear_window()
        self.create_flashcards_list_menu_instance()
        # self.flashcards_list_menu_instance.treeview()
        # self.flashcards_list_menu_instance.create_search_entry()
        # self.create_flashcards_list_menu_instance.pack_search_entry()

    def start_button_commands(self):
        Start_game(self.window, self)

    def exit_button_commands(self):
        self.window.app.quit()
        self.window.app.destroy()
        

    def render_buttons(self):
        self.window.clear_window()

        self.show_list = tkinter.Button(text="Show all flashcards", command=lambda: self.show_list_button_commands())        
        self.start = tkinter.Button(text="Start", command=lambda: self.start_button_commands())
        self.exit = tkinter.Button(text="Exit", command = lambda: self.exit_button_commands())

        self.check_state_of_start_button()



    def grid_buttons(self):
        #do zmiany
        _buttons = self.window.app.winfo_children() 
        for button in _buttons:
            button.pack(fill='both', expand=True)
            

    def create_label(self):
        self.author = tkinter.Label(text="Created by Radosław Ryłko")
        self.author.pack()

    def start_program(self):
        self.window.render_window()
        self.create_flashcards_list_menu_instance()
        self.render_buttons()
        self.grid_buttons()
        self.create_label()
        self.window.app.mainloop()








