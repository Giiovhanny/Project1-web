import csv
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title, author,year in reader:
	#text='INSERT INTO book (isbn, title , author, year) VALUES('+str(isbn)+','+str(title)+','+str(author)+','+str(year)+')'
       	#db.execute(text,'a':4)
        db.execute("INSERT INTO book (isbn, title , author, year) VALUES (:isbn1, :title1,:author1, :year1)", {'isbn1':isbn,'title1':title,'author1':author,'year1':year})
        print(f'The book with id = {isbn}, title {title}, author = {author} and year {year} was added')
    db.commit()

if __name__ == "__main__":
    main()

