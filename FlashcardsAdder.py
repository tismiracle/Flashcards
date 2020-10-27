
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
        self.add_word = tkinter.Button(text="Add word", command = lambda: self.add_to_db())

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
        self.add_word.pack(fill='both', expand=True, side='right')

    def goto_flashcards_adder(self):
        self.clear_window()
        self.create_labels()
        self.place_entries()
        self.create_buttons()
        self.pack_layout()




    def create_treeview_buttons(self):
        window_width = self.window.winfo_width()
        button_frame = tkinter.Frame(self.window, width = int(window_width*0.25))
        self.add = tkinter.Button(button_frame, text="Add", command=lambda: [self.goto_flashcards_adder(), print(self.window.winfo_children())])
        self.add.pack(fill="both", expand=True)

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

