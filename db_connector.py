import mysql.connector

class Sql_db:
    def connect_db(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root"
        )
        self.mycursor = self.mydb.cursor()

    def create_db(self):
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS flashcards;")
        self.mydb.commit()
        self.mycursor.execute("USE flashcards;")
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
        command = "INSERT INTO flashcards_examples (WORD, MEANING, NOTE) VALUES (%s, %s, %s);"
        self.mycursor.execute(command, (word, meaning, note))
        self.mydb.commit()

    def get_from_db(self, column, table):
        self.mycursor.execute("USE flashcards;")
        self.mydb.commit()
        self.mycursor.execute(f"SELECT {column} FROM {table};")

        myresult = self.mycursor.fetchall()
        return myresult

    def remove_from_db(self, word, meaning, note):
        self.mycursor.execute(f"DELETE FROM flashcards_examples WHERE WORD = '{word}' AND MEANING = '{meaning}' and NOTE = '{note}';")

                
