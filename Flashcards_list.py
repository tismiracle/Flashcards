#items_to_edit
from db_connector import Sql_db
import tkinter
from tkinter import ttk
import csv
import os
from StartGame import Start_game

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
            csv_writer = csv.writer(csvfile_write)
            for words in table:
                csv_writer.writerow(words[1:])  #doing it because the first record in list is None. I'll change it later.
                #csv_writer.
    
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
            csv_reader = csv.reader(myfile)
            for row in csv_reader:
                self.db_connector.insert_to_db(row[0],row[1],row[2])

        self.window.clear_window()
        self.treeview()


    #needed to be implemented
    def search(self):
        self.search_mode = True
        filter_values = self.get_states_of_filters()

        var = self.search_entry.get()
        print(var)
        self.searched_flashcards = self.db_connector.search_from_db(var, filter_values)
        print(self.searched_flashcards)
        #żeby wyszukiwało należy to uruchomić
        self.render_to_treeview()


    def get_states_of_filters(self):
        filter_values = {}
        filter_values["word_filter_var"] = self.word_filter_var.get()
        filter_values["meaning_filter_var"] = self.meaning_filter_var.get()
        filter_values["note_filter_var"] = self.note_filter_var.get()

        return filter_values
        

    def exit_button_commands(self):
        self.window.app.quit()
        self.window.app.destroy()

    def start_game(self):
        self.window.clear_window()
        self.start_game_instance.render_game_ui()
 
#################################################################################################################################
from Flashcards_Adder import Flashcards_Adder
from Flashcards_Editor import Flashcards_Editor

class Flashcards_List(Flashcards_List_Functions):

    search_mode = False
    def __init__(self, window, menu_layout):
        self.menu_layout = menu_layout
        self.window = window
        self.flashcards_adder = Flashcards_Adder(self, window)
        self.flashcards_editor = Flashcards_Editor(self, window)
        self.start_game_instance = Start_game(self, self.window)

        self.treeview()

  
    def create_menubar(self):
        self.menubar = tkinter.Menu(self.window.app)

    def create_menus(self):
        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.editmenu = tkinter.Menu(self.menubar, tearoff=0)
    def menu_commands(self):
        self.filemenu.add_command(label="Start", command=lambda: self.start_game())

        self.filemenu.add_command(label="Exit", command=self.window.app.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

    def pack_menubar(self):
        self.create_menubar()
        self.create_menus()
        self.menu_commands()
        self.window.app.config(menu=self.menubar)

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


        self.exit = tkinter.Button(button_frame, text="Exit", command=lambda: self.exit_button_commands())
        self.exit.pack(fill="both", expand = True)

        self.create_search_entry()
        self.pack_search_entry()
        button_frame.pack(side="right", fill='both')

        


    def treeview(self):
        self.window.clear_window()

        self.pack_menubar()

        self.treeframe = tkinter.Frame(self.window.app)
        self.create_treeview()
        self.create_treeview_buttons()
        self.treeframe.pack(side="left", fill="both", expand=True)


    def create_searching_filters(self):
        self.filters_frame = tkinter.Frame(self.window.app)

        self.filter_label = tkinter.Label(self.filters_frame, text="Filters:")

        self.word_filter_var = tkinter.IntVar()
        self.meaning_filter_var = tkinter.IntVar()
        self.note_filter_var = tkinter.IntVar()

        self.word_filter = tkinter.Checkbutton(self.filters_frame, text="Word", variable=self.word_filter_var)
        self.meaning_filter = tkinter.Checkbutton(self.filters_frame, text="Meaning", variable=self.meaning_filter_var)
        self.note_filter = tkinter.Checkbutton(self.filters_frame, text="Note", variable=self.note_filter_var)

    def pack_filters(self):
        self.create_searching_filters()

        self.filter_label.pack(side="left", fill="both", expand=True)
        self.word_filter.pack(side="left", fill="both", expand=True)
        self.meaning_filter.pack(side="left", fill="both", expand=True)
        self.note_filter.pack(side="left", fill="both", expand=True)
        self.filters_frame.pack()

    def create_search_entry(self):
        self.search_entry_frame = tkinter.Frame(self.window.app)

        self.search_entry = tkinter.Entry(self.search_entry_frame)
        self.search_button = tkinter.Button(self.search_entry_frame, text="Search", command=lambda: self.search())
        self.refresh_button = tkinter.Button(self.search_entry_frame, text="Refresh", command=lambda: self.refresh_treeview())

    def pack_search_entry(self):
        self.search_entry.pack(side="left", fill="both", expand=True)
        self.search_button.pack(side="left", fill="x", expand=True)
        self.refresh_button.pack(side="right", fill="x", expand=True)
        self.search_entry_frame.pack(side="top", fill="x")
        self.pack_filters()


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

        # for value, x in enumerate(self.load_flashcards()):
        #     self.tree.insert(parent="", index=value, values=(f"{x[1]}",f"{x[2]}",f"{x[3]}"))
        self.render_to_treeview()
        self.tree.pack(fill="both", expand=True, side="left")
        self.scrollbar.pack(fill="both", side="right")


    def render_to_treeview(self):
        self.tree.delete(*self.tree.get_children())
        if self.search_mode == False:
            all_flashcards = self.load_flashcards()
            print("loading all flashcards")
            for value, x in enumerate(all_flashcards):
                self.tree.insert(parent="", index=value, values=(f"{x[1]}",f"{x[2]}",f"{x[3]}"))
        else:
            all_flashcards = self.searched_flashcards
            for value, x in enumerate(all_flashcards):
                self.tree.insert(parent="", index=value, values=(f"{x[1]}",f"{x[2]}",f"{x[3]}"))
        self.search_mode = False

    def refresh_treeview(self):
        print("I do something")
        self.search_mode = False
        self.render_to_treeview()

    def edit_record(self):
        

        items_to_edit = self.tree.item(self.tree.selection())

        self.window.clear_window()
        print(items_to_edit)

        self.flashcards_editor.goto_flashcards_editor(items_to_edit)

        
        





