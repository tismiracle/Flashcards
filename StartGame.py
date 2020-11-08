import tkinter
from tkinter import ttk
import random
from db_connector import Sql_db

class Start(Sql_db):
    def __init__(self, window, menu_layout):
        self.window = window
        # self.app = app
        self.menu_layout = menu_layout
        self.connect_db()
        self.myresult = self.get_from_db("*", "flashcards_examples")
        
        #random.shuffle(self.myresult)
        self.i = 0
        self.correct = True
        self.correct_counter = 0
        self.window.clear_window()
        self.render_game_ui()
            
    def render_game_ui(self):
        
        
        window_height = self.window.app.winfo_height()
        locked_frame = tkinter.Frame(self.window.app, height = window_height//2)
        not_correct_frame = tkinter.Frame(self.window.app, height=window_height//3)
        entry_frame = tkinter.Frame(self.window.app)

        
        word = tkinter.Label(locked_frame, text=f"Meaning:{self.myresult[self.i][2]}", font="Arial 24")
        note = tkinter.Label(locked_frame, text=f"Note:{self.myresult[self.i][3]}", font="Arial 24")

        self.answer = tkinter.Entry(entry_frame, font="Arial 24")
        back_button = tkinter.Button(entry_frame, text="Back", comman=lambda: self.goto_main())
        self.skip_button = tkinter.Button(entry_frame, text="Skip", command=lambda: self.skip_flashcard())
        next_button = tkinter.Button(entry_frame, text="Next", command=lambda: [self.check_answer(self.i)])

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
            

    def check_answer(self, i):
        
        self.answer_check = self.answer.get()
        if self.answer_check == self.myresult[i][1]:
            if self.correct:
                self.correct_counter += 1
            print("poprawne")
            self.i += 1
            if self.i >= len(self.myresult):
                self.window.clear_window()
                self.congratulations()

            else:
                self.window.clear_window()
                self.render_game_ui()
                self.correct = True
               
            
        else:
            self.correct = False      
            self.not_correct.pack()

    def skip_flashcard(self):
        if self.i + 1 >= len(self.myresult):
            self.window.clear_window()
            self.congratulations()
        else:
            self.i += 1
            self.window.clear_window()
            self.render_game_ui()

    def goto_main(self):
        
        self.menu_layout.render_buttons()
        self.menu_layout.grid_buttons()
        self.menu_layout.create_label()


            
    def congratulations(self):
        first = "Perfect!"
        second = "Very good!"
        third = "Nice!"
        fourth = "Not bad!"
        fifth = "Could be better"
        sixth = "Really bad..."
        score = self.correct_counter/len(self.myresult)
        congrats = tkinter.Label(self.window.app, text="Congratulations!", font="Arial 30")
        congratulations_label = tkinter.Label(self.window.app, text=f"You've answered on: {self.correct_counter}/{len(self.myresult)} flashcards correctly at the first time!", wraplength=400, justify='center', font="Arial 16")
        continue_button = tkinter.Button(self.window.app, command=lambda: [self.window.clear_window(), self.goto_main()])
        if score == 1:
            continue_button.configure(text=first)
        elif score >= 0.9 and score < 1:
            continue_button.configure(text=second)
        elif score >= 0.8 and score < 0.9:
            continue_button.configure(text=third)
        elif score >= 0.5 and score < 0.8:
            continue_button.configure(text=fourth) 
        elif score >= 0.4 and score < 0.5:
            continue_button.configure(text=fifth)  
        elif score < 0.4:
            continue_button.configure(text=sixth)               
        congrats.pack()
        congratulations_label.pack()
        continue_button.pack(fill='x')
