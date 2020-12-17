import tkinter
from language_db import Language_db



class Option_menu:
    def __init__(self, main_window, render_to_treeview):
        self.main_window = main_window
        self.render_to_treeview = render_to_treeview



    def define_language_option(self):
        #changed line of code to update treeview automatically 
        self.language_option = tkinter.OptionMenu(self.lang_option_frm, self.variable, *self.language_list, command=lambda e: self.render_to_treeview())
        #self.language_option.bind("<Enter>", lambda e: self.render_to_treeview())
        

    def pack_language_option(self):   
        self.language_option.pack(side='left')

    def get_langs_from_sql(self):
        self.language_list = ["Default"]
        self.variable = tkinter.StringVar(self.main_window.app)
        self.languages_sql = Language_db()
        langs_list = self.languages_sql.get_languages()
        for lang in langs_list:
            self.language_list.append(lang[0])

        self.variable.set(self.language_list[0])


    def option_frame(self):
        self.lang_option_frm = tkinter.Frame(self.button_frame)

    def pack_option_frame(self):
        self.lang_option_frm.pack(side='bottom')

    def add_language_button(self):
        
        self.add_button = tkinter.Button(self.lang_option_frm, text="New lang", command=lambda: Add_language_window(self.display_widget, self.destroy_all_widgets))
        self.remove_lang = tkinter.Button(self.lang_option_frm, text="Remove lang", command=lambda:[self.languages_sql.remove_language_and_words(self.variable.get()), self.refresh_widget()])
        self.remove_lang.bind("<Button1>", print(self.variable.get()))
    def pack_add_language_button(self):
        self.add_button.pack(side='right')
        self.remove_lang.pack(side='right')

    def display_widget(self):
        # self.frame_to_put_in = frame_to_put_in
        self.option_frame()
        self.get_langs_from_sql()
        self.define_language_option()
        self.add_language_button()
        self.pack_option_frame()
        self.pack_add_language_button()
        self.pack_language_option()

    def destroy_all_widgets(self):
        self.lang_option_frm.destroy()
        self.add_button.destroy()
        self.language_option.destroy()

    def refresh_widget(self):
        self.destroy_all_widgets()
        self.display_widget()


class Add_language_window:
    def __init__(self, display_widget, destroy_all_widgets):
        self.destroy_all_widgets = destroy_all_widgets
        self.display_widget = display_widget #method for displaying optionMenu
        self.language_window = tkinter.Toplevel()
        self.render_widgets()

    def lang_entry(self):
        self.entry = tkinter.Entry(self.language_window)

    def pack_entry(self):
        self.entry.pack(side='top')
    
    def destroy_toplevel(self):
        self.language_window.destroy()

    def add_lanugage_button(self):
        self.add_lang = tkinter.Button(self.language_window, text="Add language", command=lambda: [self.insert_to_sql(), self.destroy_toplevel(), self.destroy_all_widgets(), self.display_widget()])
        #######
        self.add_lang.bind("<ButtonRelease-1>", lambda e: self.display_widget())
        
    
    def pack_add_btn(self):
        self.add_lang.pack(side='right')
        

    def cancel_button(self):
        self.cancel = tkinter.Button(self.language_window, text="Cancel", command=lambda: self.language_window.destroy())

    def pack_cancel_btn(self):
        self.cancel.pack(side='left')

    def insert_to_sql(self):
        language = self.entry.get()
        if len(language) == 0:
            tkinter.messagebox.showerror('Cannot add to database', "Please type in the name of the language")
        else:
            self.lang_sql = Language_db()
            self.lang_sql.insert_new_language(str(language))
            print("Successfuly added")

    def render_widgets(self):
        self.lang_entry()
        self.pack_entry()
        self.add_lanugage_button()
        self.pack_add_btn()
        self.cancel_button()
        self.pack_cancel_btn()


        



    
