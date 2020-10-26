import tkinter
from FlashcardsAdder import *
from StartGame import Start
from db_connector import Sql_db
class Window(Sql_db):

    def render_window(self):
        self.window_size = "400x400"
        self.window_size_tuple = self.window_size.split('x')
        self.window_height = int(self.window_size_tuple[1])
        self.window_width = int(self.window_size_tuple[0])
        self.app = tkinter.Tk()
        self.app.geometry(self.window_size)    

    def flashcards_adder(self):
        self.flashcards_add = FlashcardsMenu(self.app, self, self.clear_window)

    def clear_window(self):
        print("window cleared")
        _list = self.app.winfo_children()   
        for buttons in _list:
            buttons.destroy()


    
class Menu_Layout(Window):

    def __init__(self):
        super().__init__()
        self.render_window()
        self.flashcards_adder()
        self.render_buttons()
        self.grid_buttons()
        self.create_label()

    def check_start_state(self):
        records = self.check_len_of_db()
        print(records)
        if records[0][0] > 0:
            self.start.configure(state="active")
        else:
            self.start.configure(state="disabled")

        

    def render_buttons(self):
        self.clear_window()
        
        self.start = tkinter.Button(text="Start", command=lambda: [Start(self.app, self.clear_window, self)])
        self.show = tkinter.Button(text="Show all flashcards", command=lambda: [self.clear_window(), self.flashcards_add.treeview()])
        self.exit = tkinter.Button(text="Exit", command = lambda: [self.app.quit(), self.app.destroy()])

        self.check_start_state()



    def grid_buttons(self):
        _buttons = self.app.winfo_children() 
        for button in _buttons:
            button.pack(fill='both', expand=True)
            

    def create_label(self):
        self.author = tkinter.Label(text="Created by Radosław Ryłko v 0.1")
        self.author.pack()





