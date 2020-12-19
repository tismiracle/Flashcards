import tkinter
from tkinter import ttk
import random
from db_connector import Sql_db

class Start_game(Sql_db):
    flashcard_num = 0
    correct = True
    correct_counter = 0

    def __init__(self, flashcards_list_instance, window, language):
        self.flashcards_list_instance = flashcards_list_instance
        self.language = language
        self.window = window
        self.connect_db()
        self.list_of_flashcards = self.get_from_db("*", "flashcards_examples", self.language)        
            
    def render_game_ui(self):
        #there's a bug in which when you chose All flashcards game doesnt work
        self.list_of_flashcards = self.get_from_db("*", "flashcards_examples", self.language)

        window_height = self.window.app.winfo_height()
        locked_frame = tkinter.Frame(self.window.app, height = window_height//2)
        not_correct_frame = tkinter.Frame(self.window.app, height=window_height//3)
        entry_frame = tkinter.Frame(self.window.app)

        
        word = tkinter.Label(locked_frame, text=f"Meaning: {self.list_of_flashcards[self.flashcard_num][2]}", font="Arial 24")
        note = tkinter.Label(locked_frame, text=f"Note: {self.list_of_flashcards[self.flashcard_num][3]}", font="Arial 24")

        self.answer = tkinter.Entry(entry_frame, font="Arial 24")
        back_button = tkinter.Button(entry_frame, text="Back", comman=lambda: self.flashcards_list_instance.treeview())
        self.skip_button = tkinter.Button(entry_frame, text="Skip", command=lambda: self.skip_flashcard())
        next_button = tkinter.Button(entry_frame, text="Next", command=lambda: self.next_button_function())

        self.not_correct = tkinter.Label(not_correct_frame, text="Incorrect answer", fg="red")    

        word.pack(fill='x', expand=True)
        note.pack(fill='x', expand=True)

        self.answer.pack(fill='x', expand=True, side='top')

        back_button.pack(fill='x', expand=True, side='left')
        self.skip_button.pack(fill='x', expand=True, side='left')
        next_button.pack(fill='x', expand=True, side='right')

        locked_frame.pack(expand=True)
        not_correct_frame.pack(expand=True)
        entry_frame.pack()
            
    def check_if_correct(self):
        # print(self.list_of_flashcards)
        if self.answer_check == self.list_of_flashcards[self.flashcard_num][1]:
            if self.correct:
                self.correct_counter += 1
            self.flashcard_num += 1
            self.check_if_the_end()
        else:
            self.correct = False      
            self.not_correct.pack()

    def check_if_the_end(self):        
        if self.flashcard_num >= len(self.list_of_flashcards):
            self.window.clear_window()
            self.congratulations()
        else:
            self.window.clear_window()
            self.render_game_ui()
            self.correct = True

    def next_button_function(self):        
        self.answer_check = self.answer.get()
        self.check_if_correct()

    def skip_flashcard(self):
        if self.flashcard_num + 1 >= len(self.list_of_flashcards):
            self.window.clear_window()
            self.congratulations()
        else:
            self.flashcard_num += 1
            self.window.clear_window()
            self.render_game_ui()


    def calculate_score(func):
        def inner(self):
            self.score = self.correct_counter/len(self.list_of_flashcards)
            func(self)
        return inner
    
    def game_endscreen_ui(self):
        self.congrats_label = tkinter.Label(self.window.app, text="That's all!", font="Arial 30")
        self.score_info_label = tkinter.Label(self.window.app, text=f"You've answered on: {self.correct_counter}/{len(self.list_of_flashcards)} flashcards correctly at the first time", wraplength=400, justify='center', font="Arial 16")
        self.continue_button = tkinter.Button(self.window.app, command=lambda: [self.window.clear_window(), self.flashcards_list_instance.treeview()])

    def pack_game_endscreen_ui(self):
        self.congrats_label.pack()
        self.score_info_label.pack()
        self.continue_button.pack(fill='x')

    def get_button_answer_depending_on_score(self):
        first = "Perfect!"
        second = "Very good!"
        third = "Nice!"
        fourth = "Not bad!"
        fifth = "Could be better"
        sixth = "Really bad..."

        if self.score == 1:
            self.continue_button.configure(text=first)
        elif self.score >= 0.9 and self.score < 1:
            self.continue_button.configure(text=second)
        elif self.score >= 0.8 and self.score < 0.9:
            self.continue_button.configure(text=third)
        elif self.score >= 0.5 and self.score < 0.8:
            self.continue_button.configure(text=fourth) 
        elif self.score >= 0.4 and self.score < 0.5:
            self.continue_button.configure(text=fifth)  
        elif self.score < 0.4:
            self.continue_button.configure(text=sixth) 


    @calculate_score
    def congratulations(self):
        self.game_endscreen_ui()
        self.get_button_answer_depending_on_score()
        self.pack_game_endscreen_ui()
