
from db_connector import Sql_db
import tkinter
from tkinter import ttk
import csv
import os

class Flashcards_List_Functions():
    db_connector = Sql_db()

    def pass_to_remove_from_db(self):

        item_to_delete = self.tree.selection()
        for item in item_to_delete:
            item = self.tree.item(item)
            _word = item["values"][0]

            _meaning = item["values"][1]

            _note = item["values"][2]

            self.db_connector.remove_from_db( _word, _meaning, _note)
        


        self.scrollbar.destroy()
        self.tree.destroy()
        self.create_treeview()


    def load_flashcards(self):
        db_records = self.db_connector.get_from_db("*","flashcards_examples")
        return db_records



    def export_to_csv(self):
        
        table = self.db_connector.get_from_db("*", "flashcards_examples")
        print(table)
        with open("flashcards.csv", "w") as csvfile_write:
            csv_writer = csv.writer(csvfile_write, delimiter=",")
            for words in table:
                csv_writer.writerow(words[1:])  #doing it because the first record in list is None. I'll change it later.
    
    def load_from_csv(self):
        print(self.tree)
        from tkinter import filedialog
        my_filetype = [('CSV file', '.csv')]

        csv_file = filedialog.askopenfilename(parent=self.window.app,
                                    initialdir=os.getcwd(),
                                    title="Please select a file:",
                                    filetypes=my_filetype)

        print(csv_file)

        with open(csv_file, "r") as myfile:
            csv_reader = csv.reader(myfile, delimiter=",")
            for row in csv_reader:
                self.db_connector.insert_to_db(row[0],row[1],row[2])

        self.window.clear_window()
        self.treeview()


    #needed to be implemented
    def search_db(self, search):
        word_table = self.db_connector.get_from_db("*", "flashcards_examples")
        pass


        


#################################################################################################################################
from Flashcards_Adder import Flashcards_Adder
from Flashcards_Editor import Flashcards_Editor

class Flashcards_List(Flashcards_List_Functions):


    def __init__(self, window, menu_layout):
        self.menu_layout = menu_layout
        self.window = window
        self.flashcards_adder = Flashcards_Adder(self, window)
        self.flashcards_editor = Flashcards_Editor(self, window)
        self.treeview()
  
#Do edycji!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def goto_main(self):
        self.menu_layout.render_buttons()
        self.menu_layout.grid_buttons()
        self.menu_layout.create_label()



    def create_treeview_buttons(self):
        window_width = self.window.app.winfo_width()

        button_frame = tkinter.Frame(self.window.app)

        self.add = tkinter.Button(button_frame, text="Add", command=lambda: self.flashcards_adder.goto_flashcards_adder())
        self.add.pack(fill="both", expand=True)

        self.edit = tkinter.Button(button_frame, text="Edit", command=lambda: self.edit_record())
        self.edit.pack(fill="both", expand=True)

        self.remove = tkinter.Button(button_frame, text="Remove", command=lambda: self.pass_to_remove_from_db())
        self.remove.pack(fill="both", expand=True)

        self.export_to_csv_button = tkinter.Button(button_frame, text="Export to CSV", command=lambda: self.export_to_csv())
        self.export_to_csv_button.pack(fill='both', expand=True)

        self.load_from_csv_button = tkinter.Button(button_frame, text="Load from CSV", command=lambda: self.load_from_csv())
        self.load_from_csv_button.pack(fill='both', expand=True)


        self.back = tkinter.Button(button_frame, text="Back", command=lambda: self.goto_main())
        self.back.pack(fill="both", expand = True)

        self.create_search_entry()
        self.pack_search_entry()
        button_frame.pack(side="right", fill='both')

        


    def treeview(self):
        self.treeframe = tkinter.Frame(self.window.app)
        self.create_treeview()
        self.create_treeview_buttons()
        self.treeframe.pack(side="left", fill="both", expand=True)

    def create_search_entry(self):
        self.search_entry_frame = tkinter.Frame(self.window.app)


        self.search_entry = tkinter.Entry(self.search_entry_frame)
        self.search_button = tkinter.Button(self.search_entry_frame, text="Search")

    def pack_search_entry(self):
        self.search_entry.pack(side="left", fill="both", expand=True)
        self.search_button.pack(side="left", fill="x", expand=True)
        self.search_entry_frame.pack(side="top", fill="x")


    def create_treeview(self):

        self.tree = ttk.Treeview(self.treeframe, selectmode="extended")

        self.scrollbar = tkinter.Scrollbar(self.treeframe, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.tree["columns"]=("word","meaning","note")
        self.tree.column("#0", width=0, minwidth=0, stretch=tkinter.NO)
        self.tree.column("word",width=10, minwidth=1, stretch=tkinter.YES)
        self.tree.column("meaning",width=10, minwidth=1)
        self.tree.column("note",width=10, minwidth=1, stretch=tkinter.YES)


        self.tree.heading("word", text="Word",anchor=tkinter.W)
        self.tree.heading("meaning", text="Meaning",anchor=tkinter.W)
        self.tree.heading("note", text="Note",anchor=tkinter.W)



        for value, x in enumerate(self.load_flashcards()):
            self.tree.insert(parent="", index=value, values=(f"{x[1]}",f"{x[2]}",f"{x[3]}"))

        self.tree.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="both", side="right")
        

        
    def edit_record(self):
        

        items_to_edit = self.tree.item(self.tree.selection())

        self.window.clear_window()
        print(items_to_edit)

        self.flashcards_editor.goto_flashcards_editor(items_to_edit)
        
        





