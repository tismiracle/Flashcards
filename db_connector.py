import sqlite3
from tkinter import messagebox

class Sql_db:

    def __init__(self):
        self.connect_db()
        self.create_db_if_not_exists()
        
    def connect_db(self):
        self.mydb = sqlite3.connect('flashcards.db3')
        self.mycursor = self.mydb.cursor()

    def create_db_if_not_exists(self):
        self.mydb.commit()
        # self.mycursor.execute("USE flashcards;")
        self.mydb.commit()
        self.mycursor.execute("""        CREATE TABLE IF NOT EXISTS flashcards_examples (
            Row_ID int auto_increment
                primary key,
            WORD varchar(255),
            MEANING varchar(255),
            NOTE varchar(255)
            )"""
        )
        self.mydb.commit()

    def insert_to_db(self, word, meaning, note):
        command = f"INSERT INTO flashcards_examples (WORD, MEANING, NOTE) VALUES ('{word}','{meaning}', '{note}');" 
        self.mycursor.execute(command)
        self.mydb.commit()
                

    def get_from_db(self, column, table):
        
        self.mycursor.execute(f"SELECT {column} FROM {table};")
        myresult = self.mycursor.fetchall()
        return myresult

    def remove_from_db(self, word, meaning, note):
        self.mycursor.execute(f"DELETE FROM flashcards_examples WHERE WORD = '{word}' AND MEANING = '{meaning}' and NOTE = '{note}';")
        self.mydb.commit()

    def edit_db(self, word_before, meaning_before, note_before, word, meaning, note):
        self.mycursor.execute(f"SELECT WORD, MEANING, NOTE FROM flashcards_examples WHERE WORD='{word}' AND MEANING='{meaning}' AND NOTE='{note};'")
        self.mydb.commit()
        self.mycursor.execute(f"UPDATE flashcards_examples SET WORD = '{word}', MEANING = '{meaning}', NOTE = '{note}' WHERE WORD='{word_before}' AND MEANING='{meaning_before}' AND NOTE='{note_before}';")
        self.mydb.commit()


    def check_len_of_db(self):
        self.connect_db()
        self.mycursor.execute("SELECT COUNT(WORD) AS amount FROM flashcards_examples;")
        records_amount = self.mycursor.fetchall()
        print(records_amount)
        return records_amount

    def search_from_db(self, search_var, filter_values):
        self.connect_db()
        searched_vars = []
        word_variables = None
        meaning_variables = None
        note_variables = None
        if filter_values.get("word_filter_var") == 1:
            self.mycursor.execute("SELECT *" + "FROM flashcards_examples WHERE WORD LIKE (?)", ("%" + search_var + "%",))
            word_variables = self.mycursor.fetchall()
        if filter_values.get("meaning_filter_var") == 1:
            self.mycursor.execute("SELECT *" + "FROM flashcards_examples WHERE MEANING LIKE (?)", ("%" + search_var + "%",))
            meaning_variables = self.mycursor.fetchall()
        if filter_values.get("note_filter_var") == 1:
            self.mycursor.execute("SELECT *" + "FROM flashcards_examples WHERE NOTE LIKE (?)", ("%" + search_var + "%",))
            note_variables = self.mycursor.fetchall()


        if not word_variables == None:
            for item in word_variables:
                searched_vars.append(item)
        if not meaning_variables == None:
            for item in meaning_variables:
                searched_vars.append(item)
        if not note_variables == None:
            for item in note_variables:
                searched_vars.append(item)

        return searched_vars


