import tkinter


class Option_menu:
    def __init__(self, main_window):
        self.main_window = main_window
        self.language_list = ['English', 'German']
        self.variable = tkinter.StringVar(self.main_window.app)
        self.variable.set(self.language_list[0])

    def define_language_option(self):
        self.language_option = tkinter.OptionMenu(self.lang_option_frm, self.variable, *self.language_list)

    def pack_language_option(self):   
        self.language_option.pack()



    def option_frame(self):
        self.lang_option_frm = tkinter.Frame(self.frame_to_put_in)

    def pack_option_frame(self):
        self.lang_option_frm.pack(side='bottom')

    def display_widget(self, frame_to_put_in):
        self.frame_to_put_in = frame_to_put_in
        self.option_frame()
        self.define_language_option()
        self.pack_option_frame()
        self.pack_language_option()

    