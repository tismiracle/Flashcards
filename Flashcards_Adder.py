import tkinter
from db_connector import Sql_db
from tkinter import messagebox


class Flashcards_Adder_Functions:
    db_connector = Sql_db()

    # def create_buttons(self):
    #     self.back = tkinter.Button(text="Go back", command =lambda: self.goto_main()) #do edycji. Trzeba zmienić żeby wracało do listy flashcardów
    #     self.add_word = tkinter.Button(text="Add word", command = lambda: self.add_word_button_function())

    def add_word_button_function(self):
        self.pass_to_add_to_db()
        self.clear_entries()
        self.changes_applied_visible()

    def pass_to_add_to_db(self):
        
        _word = self.word_entry.get()
        _meaning = self.meaning_entry.get()
        _note = self.note_entry.get()
        if _note == "":
            _note = "-"
        print(_word, _meaning, _note)
        self.db_connector.insert_to_db(self.language_chosen, _word, _meaning, _note)

    def clear_entries(self):
        self.word_entry.delete(0, 'end')
        self.meaning_entry.delete(0, 'end')
        self.note_entry.delete(0, 'end')

    def changes_applied_visible(self):
        self.change_info.configure(text="Changes applied")

    def goto_flashcards_list(self):
        self.window.clear_window()
        self.flashcards_list_instance.treeview()
        self.option_menu.variable.set(self.language_chosen)
        self.refresh_treeview()



class Flashcards_Adder(Flashcards_Adder_Functions):
    def __init__(self, flashcards_list_instance, window, option_menu, language_chosen, refresh_treeview):
        self.flashcards_list_instance = flashcards_list_instance
        self.refresh_treeview = refresh_treeview
        self.option_menu = option_menu
        self.language_chosen = language_chosen
        print(self.language_chosen)        
        
        self.window = window
        
        

    def place_entries(self):
        self.word_entry = tkinter.Entry(self.window.app, font=('Arial 24'))
        self.meaning_entry = tkinter.Entry(self.window.app, font=('Arial 24'))
        self.note_entry = tkinter.Entry(self.window.app, font=('Arial 24'))

    def create_labels(self):
        self.change_info = tkinter.Label(text="Waiting for changes")
        self.word_label = tkinter.Label(self.window.app, text="Word")
        self.meaning_label = tkinter.Label(self.window.app, text="Meaning")
        self.note_label = tkinter.Label(self.window.app, text="Note")


    def create_buttons(self):
        self.back = tkinter.Button(text="Go back", command =lambda: self.goto_flashcards_list())
        self.add_word = tkinter.Button(text="Add word", command = lambda: self.add_word_button_function())

    def pack_layout(self):
        self.word_label.pack(fill='both', expand=True)
        self.word_entry.pack(fill='both', expand=True)
        self.meaning_label.pack(fill='both', expand=True)
        self.meaning_entry.pack(fill='both', expand=True)
        self.note_label.pack(fill='both', expand=True)
        self.note_entry.pack(fill='both', expand=True)

        self.back.pack(fill='both', expand=True, side='left')
        self.change_info.pack(fill='both', expand=True, side='left')
        self.add_word.pack(fill='both', expand=True, side='left')    

    def goto_flashcards_adder(self):
        self.window.clear_window()
        self.create_labels()
        self.place_entries()
        self.create_buttons()
        self.pack_layout()