
from db_connector import Sql_db
import tkinter
from tkinter import ttk



class FlashcardsMenu(Sql_db):
    def __init__(self, window, menu, clear_window):
        print("FlashcardsMenu initialized")
        self.clear_window = clear_window
        self.menu = menu
        self.window = window
        self.connect_db()
        self.create_db()
        self.mycursor = self.mydb.cursor()
        self.tree_buttons = False
        self.edit_var = False

    def add_to_db(self):
        _word = self.word_entry.get()
        _meaning = self.meaning_entry.get()
        _note = self.note_entry.get()
        print(_word, _meaning, _note)
        self.insert_to_db(_word, _meaning, _note)
        


    def goto_main(self):

        self.menu.render_buttons()
        self.menu.grid_buttons()
        self.menu.create_label()


    def create_buttons(self):
        self.back = tkinter.Button(text="Go back", command =lambda: self.goto_main())
        self.add_word = tkinter.Button(text="Add word", command = lambda: [self.add_to_db(), self.refresh(), self.changes_applied_visible()])
        self.change_info = tkinter.Label(text="Waiting for changes")
        #width=width//3


    def changes_applied_visible(self):
        self.change_info.configure(text="Changes applied")

    def create_labels(self):
        self.word = tkinter.Label(self.window, text="Word")
        self.meaning = tkinter.Label(self.window, text="Meaning")
        self.note = tkinter.Label(self.window, text="Note")


    def place_entries(self):
        self.word_entry = tkinter.Entry(self.window, font=('Arial 24'))
        self.meaning_entry = tkinter.Entry(self.window, font=('Arial 24'))
        self.note_entry = tkinter.Entry(self.window, font=('Arial 24'))
        print(self.window)

    def pack_layout(self):
        self.word.pack(fill='both', expand=True)
        self.word_entry.pack(fill='both', expand=True)
        self.meaning.pack(fill='both', expand=True)
        self.meaning_entry.pack(fill='both', expand=True)
        self.note.pack(fill='both', expand=True)
        self.note_entry.pack(fill='both', expand=True)

        self.back.pack(fill='both', expand=True, side='left')
        self.change_info.pack(fill='both', expand=True, side='left')
        self.add_word.pack(fill='both', expand=True, side='left')
        

    def clear_entries(self):
        self.word_entry.delete(0, 'end')
        self.meaning_entry.delete(0, 'end')
        self.note_entry.delete(0, 'end')


    def goto_flashcards_adder(self):
        self.edit_var = False
        self.clear_window()
        self.create_labels()
        self.place_entries()
        self.create_buttons()
        self.pack_layout()


    def create_treeview_buttons(self):
        window_width = self.window.winfo_width()
        button_frame = tkinter.Frame(self.window, width = int(window_width*0.25))
        self.add = tkinter.Button(button_frame, text="Add", command=lambda: [self.goto_flashcards_adder()])
        self.add.pack(fill="both", expand=True)

        self.edit = tkinter.Button(button_frame, text="Edit", command=lambda: self.edit_record())
        self.edit.pack(fill="both", expand=True)

        self.remove = tkinter.Button(button_frame, text="Remove", command=lambda: self.pass_to_remove())
        self.remove.pack(fill="both", expand=True)

        self.back = tkinter.Button(button_frame, text="Back", command=lambda: self.goto_main())

        self.back.pack(fill="both", expand = True)
        button_frame.pack(side="right")


    def treeview(self):
        self.treeframe = tkinter.Frame(self.window)
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


        self.myresult = self.get_from_db("*","flashcards_examples")
        for value, x in enumerate(self.myresult):
            self.tree.insert(parent="", index=value, values=(f"{x[1]}",f"{x[2]}",f"{x[3]}"))
        self.tree.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="both", side="right")


    def pass_to_remove(self):
        item_to_delete = self.tree.item(self.tree.focus())
        print(item_to_delete)
        _word = item_to_delete["values"][0]

        _meaning = item_to_delete["values"][1]

        _note = item_to_delete["values"][2]

        self.remove_from_db( _word, _meaning, _note)
        self.myresult = self.mydb.commit()
        self.scrollbar.destroy()
        self.tree.destroy()
        self.create_treeview()

    def edit_record(self):
        item_to_edit = self.tree.item(self.tree.focus())
        self.clear_window()
        self.goto_flashcards_adder()

        self.add_word.destroy()
        self.edit_word = tkinter.Button(text="Edit", command=lambda: [self.send_edited_to_db(item_to_edit['values'][0], item_to_edit['values'][1], item_to_edit['values'][2]), self.refresh(), self.changes_applied_visible()])
        self.edit_word.pack(fill='both', expand=True, side='right')


        self.edit_var = True

        self.word_entry.insert(0, f"{item_to_edit['values'][0]}")

        self.meaning_entry.insert(0, f"{item_to_edit['values'][1]}")

        self.note_entry.insert(0, f"{item_to_edit['values'][2]}")

         
    def send_edited_to_db(self, word_before, meaning_before, note_before):
        print(self.window.winfo_children())
        _edited_word = self.word_entry.get()
        _edited_meaning = self.meaning_entry.get()
        _edited_note = self.note_entry.get()

        self.edit_db(word_before, meaning_before, note_before, _edited_word, _edited_meaning, _edited_note)



    def refresh(self):
        # self.clear_window()
        self.clear_entries()
