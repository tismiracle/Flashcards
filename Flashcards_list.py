
from db_connector import Sql_db
import tkinter
from tkinter import ttk


class Flashcards_List_Functions():
    db_connector = Sql_db()

    def __init__(self):
        self.db_connector.connect_db()
        self.db_connector.create_db_if_not_exists()

    def pass_to_add_to_db(self):
        _word = self.word_entry.get()
        _meaning = self.meaning_entry.get()
        _note = self.note_entry.get()
        print(_word, _meaning, _note)
        self.db_connector.insert_to_db(_word, _meaning, _note)

    def pass_to_remove_from_db(self):
        item_to_delete = self.tree.item(self.tree.focus())

        _word = item_to_delete["values"][0]

        _meaning = item_to_delete["values"][1]

        _note = item_to_delete["values"][2]

        self.db_connector.remove_from_db( _word, _meaning, _note)

        self.scrollbar.destroy()
        self.tree.destroy()
        self.create_treeview()

         
    def send_edited_to_db(self, word_before, meaning_before, note_before):
        print(self.window.app.winfo_children())
        _edited_word = self.word_entry.get()
        _edited_meaning = self.meaning_entry.get()
        _edited_note = self.note_entry.get()

        self.db_connector.edit_db(word_before, meaning_before, note_before, _edited_word, _edited_meaning, _edited_note)

    def load_flashcards(self):
        db_records = self.db_connector.get_from_db("*","flashcards_examples")
        return db_records

    def clear_entries(self):
        self.word_entry.delete(0, 'end')
        self.meaning_entry.delete(0, 'end')
        self.note_entry.delete(0, 'end')

    def add_word_button_function(self):
        self.pass_to_add_to_db()
        self.clear_entries()
        self.changes_applied_visible()

    def edit_word_button_function(self, edited_word, edited_meaning, edited_note):
        self.send_edited_to_db(edited_word, edited_meaning, edited_note)
        self.clear_entries()
        self.changes_applied_visible()

#################################################################################################################################

class Flashcards_List(Flashcards_List_Functions):
    # tree_buttons = False
    # edit_var = False

    def __init__(self, window, menu_layout):
        super().__init__()
        self.menu_layout = menu_layout
        self.window = window
  

    def goto_main(self):
        self.menu_layout.render_buttons()
        self.menu_layout.grid_buttons()
        self.menu_layout.create_label()


    def create_buttons(self):
        self.back = tkinter.Button(text="Go back", command =lambda: self.goto_main())
        self.add_word = tkinter.Button(text="Add word", command = lambda: self.add_word_button_function())
        


    def changes_applied_visible(self):
        self.change_info.configure(text="Changes applied")

    def create_labels(self):
        self.change_info = tkinter.Label(text="Waiting for changes")
        self.word_label = tkinter.Label(self.window.app, text="Word")
        self.meaning_label = tkinter.Label(self.window.app, text="Meaning")
        self.note_label = tkinter.Label(self.window.app, text="Note")


    def place_entries(self):
        self.word_entry = tkinter.Entry(self.window.app, font=('Arial 24'))
        self.meaning_entry = tkinter.Entry(self.window.app, font=('Arial 24'))
        self.note_entry = tkinter.Entry(self.window.app, font=('Arial 24'))

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
        # self.edit_var = False
        self.window.clear_window()
        self.create_labels()
        self.place_entries()
        self.create_buttons()
        self.pack_layout()


    def create_treeview_buttons(self):
        window_width = self.window.app.winfo_width()

        button_frame = tkinter.Frame(self.window.app)

        self.add = tkinter.Button(button_frame, text="Add", command=lambda: self.goto_flashcards_adder())
        self.add.pack(fill="both", expand=True)

        self.edit = tkinter.Button(button_frame, text="Edit", command=lambda: self.edit_record())
        self.edit.pack(fill="both", expand=True)

        self.remove = tkinter.Button(button_frame, text="Remove", command=lambda: self.pass_to_remove_from_db())
        self.remove.pack(fill="both", expand=True)

        self.export_to_csv = tkinter.Button(button_frame, text="Export to CSV")
        self.export_to_csv.pack(fill='both', expand=True)


        self.back = tkinter.Button(button_frame, text="Back", command=lambda: self.goto_main())
        self.back.pack(fill="both", expand = True)
        button_frame.pack(side="right")


    def treeview(self):
        self.treeframe = tkinter.Frame(self.window.app)
        self.create_treeview()
        self.create_treeview_buttons()
        self.treeframe.pack(side="left", fill="both", expand=True)

    def create_treeview(self):
        self.tree = ttk.Treeview(self.treeframe)

        self.scrollbar = tkinter.Scrollbar(self.treeframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree["columns"]=("one","two","three")
        self.tree.column("#0", width=0, minwidth=0, stretch=tkinter.NO)
        self.tree.column("one",width=10, minwidth=1, stretch=tkinter.YES)
        self.tree.column("two",width=10, minwidth=1)
        self.tree.column("three",width=10, minwidth=1, stretch=tkinter.YES)

        self.tree.heading("one", text="Word",anchor=tkinter.W)
        self.tree.heading("two", text="Meaning",anchor=tkinter.W)
        self.tree.heading("three", text="Note",anchor=tkinter.W)



        for value, x in enumerate(self.load_flashcards()):
            self.tree.insert(parent="", index=value, values=(f"{x[1]}",f"{x[2]}",f"{x[3]}"))

        self.tree.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="both", side="right")
        

        
    def edit_record(self):
        item_to_edit = self.tree.item(self.tree.focus())

        self.window.clear_window()
        self.goto_flashcards_adder()

        self.add_word.destroy()

        self.edit_word = tkinter.Button(text="Edit", command=lambda: self.edit_word_button_function(item_to_edit['values'][0], item_to_edit['values'][1], item_to_edit['values'][2]))

        self.edit_word.pack(fill='both', expand=True, side='right')


        # self.edit_var = True

        self.word_entry.insert(0, f"{item_to_edit['values'][0]}")

        self.meaning_entry.insert(0, f"{item_to_edit['values'][1]}")

        self.note_entry.insert(0, f"{item_to_edit['values'][2]}")



