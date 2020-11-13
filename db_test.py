import random
import string
import sqlite3



alphabet = string.ascii_lowercase

mydb = sqlite3.connect('flashcards.db3')
mycursor = mydb.cursor()
word = ""
meaning = ""
note = ""
for i in range(100000):
    for i in range(1, random.randint(1, 6)):
        word = word + random.choice(alphabet)
        meaning = meaning + random.choice(alphabet)
        note = note + random.choice(alphabet)
    print(word)
    print(meaning)
    print(note)
    command = f"INSERT INTO flashcards_examples (WORD, MEANING, NOTE) VALUES ('{word}','{meaning}', '{note}');" 
    mycursor.execute(command)
    mydb.commit()
    word = ""
    meaning = ""
    note = ""
                


