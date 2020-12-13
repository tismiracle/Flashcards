import tkinter
from db_connector import Sql_db


class Flashcards_Editor_Functions:
    db_connector = Sql_db()
    def edit_word_button_function(self):
        # items_to_edit = items_to_edit
        self.word_before = self.items_to_edit['values'][0]
        self.meaning_before = self.items_to_edit['values'][1]
        self.note_before = self.items_to_edit['values'][2]
        
        self.send_edited_to_db()
        self.clear_entries()
        self.changes_applied_visible()

    def changes_applied_visible(self):
        self.change_info.configure(text="Changes applied")

    def send_edited_to_db(self):
        print(self.window.app.winfo_children())
        _edited_word = self.word_entry.get()
        _edited_meaning = self.meaning_entry.get()
        _edited_note = self.note_entry.get()

        self.db_connector.edit_db(self.word_before, self.meaning_before, self.note_before, _edited_word, _edited_meaning, _edited_note)

    def goto_flashcards_list(self):
        self.window.clear_window()
        self.flashcards_list_instance.treeview()
        self.option_menu.variable.set(self.language_chosen)
        self.refresh_treeview()

    def clear_entries(self):
        self.word_entry.delete(0, 'end')
        self.meaning_entry.delete(0, 'end')
        self.note_entry.delete(0, 'end')



class Flashcards_Editor(Flashcards_Editor_Functions):
    db_connector = Sql_db()

    def __init__(self, flashcards_list_instance, window, option_menu, language_chosen, refresh_treeview):
        self.flashcards_list_instance = flashcards_list_instance
        self.refresh_treeview = refresh_treeview
        self.option_menu = option_menu
        self.language_chosen = language_chosen
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

        self.edit_word = tkinter.Button(text="Edit", command=lambda: self.edit_word_button_function())
        # items_to_edit['values'][0], items_to_edit['values'][1], items_to_edit['values'][2]


        self.word_entry.insert(0, f"{self.items_to_edit['values'][0]}")

        self.meaning_entry.insert(0, f"{self.items_to_edit['values'][1]}")

        self.note_entry.insert(0, f"{self.items_to_edit['values'][2]}")
        
    def pack_layout(self):
        self.word_label.pack(fill='both', expand=True)
        self.word_entry.pack(fill='both', expand=True)
        self.meaning_label.pack(fill='both', expand=True)
        self.meaning_entry.pack(fill='both', expand=True)
        self.note_label.pack(fill='both', expand=True)
        self.note_entry.pack(fill='both', expand=True)

        self.back.pack(fill='both', expand=True, side='left')
        self.change_info.pack(fill='both', expand=True, side='left')
        self.edit_word.pack(fill='both', expand=True, side='right')
        # self.add_word.pack(fill='both', expand=True, side='left')    

    def goto_flashcards_editor(self, items_to_edit):
        self.items_to_edit = items_to_edit
        
        
        self.window.clear_window()
        self.create_labels()
        self.place_entries()
        self.create_buttons()
        self.pack_layout()