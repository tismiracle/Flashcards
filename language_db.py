import sqlite3

class Language_db:

    def __init__(self):
        self.connect_db()
        self.create_db_if_not_exists()
        
    def connect_db(self):
        self.mydb = sqlite3.connect('languages.db3')
        self.mycursor = self.mydb.cursor()

    def create_db_if_not_exists(self):
        self.mycursor.execute("""CREATE TABLE IF NOT EXISTS languages (
            LANGUAGE varchar(255) UNIQUE);""")
        self.mydb.commit()
    
    def insert_new_language(self, language):
        self.mycursor.execute(f"""INSERT INTO languages (LANGUAGE) VALUES ('{language}');""")
        self.mydb.commit()

    def get_languages(self):
        self.mycursor.execute("""SELECT * FROM languages;""")
        records = self.mycursor.fetchall()
        return records

