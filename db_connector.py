import mysql.connector
import sqlite3

class Sql_db:
    def connect_db(self):
        # self.mydb = mysql.connector.connect(
        #     host="localhost",
        #     user="root",
        #     password="root"
        # )
        self.mydb = sqlite3.connect('flashcards')
        self.mycursor = self.mydb.cursor()

    def create_db(self):
        # self.mycursor.execute("CREATE DATABASE IF NOT EXISTS flashcards;")
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
        params = (word, meaning, note)
        command = f"INSERT INTO flashcards_examples (WORD, MEANING, NOTE) VALUES ('{word}','{meaning}', '{note}');"
        self.mycursor.execute(str(command))
        self.mydb.commit()

    def get_from_db(self, column, table):
        # self.mycursor.execute("USE flashcards;")
        self.mydb.commit()
        self.mycursor.execute(f"SELECT {column} FROM {table};")

        myresult = self.mycursor.fetchall()
        return myresult

    def remove_from_db(self, word, meaning, note):
        self.mycursor.execute(f"DELETE FROM flashcards_examples WHERE WORD = '{word}' AND MEANING = '{meaning}' and NOTE = '{note}';")
        self.mydb.commit()

    def check_len_of_db(self):
        self.connect_db()
        self.mycursor.execute("SELECT COUNT(WORD) AS amount FROM flashcards_examples;")
        records_amount = self.mycursor.fetchall()
        print(records_amount)
        return records_amount
        #end

                
