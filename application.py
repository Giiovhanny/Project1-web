import os

from flask import Flask, session,render_template, redirect, url_for, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
user=None

@app.route("/home", methods=['POST','GET'])
def home():
    error=None
    value1=str(request.form.get('value'))
    value2=request.form.get('value2')
    value2="'"+'%'+str(value2)+'%'+"'"

    txt= 'select * from book where '+ value1+ ' similar to ' + value2
    print(value1,value2)
    if request.method == 'POST':
        books=db.execute(txt,{}).fetchall()
        db.commit()
        #return render_template("books.html", books=books)
        if books:
            
            return render_template("books.html", books=books,error=error)
        else:
            error="They are no match!"
            return render_template("books.html", books=books,error=error)


    return render_template('index.html', error=error)


@app.route("/home/<book_isbn>",methods=['POST','GET'])
def book(book_isbn):
    """Lists details about a single flight."""
    rate=request.form.get('rate')
    review=request.form.get('review')
    global user
    print(rate, review,user,book_isbn )
    if request.method == 'POST':
        try:
            db.execute('insert into RateBook (isbn,usuario,rate,review) values (:isbn,:user,:rate,:review)', {'isbn':book_isbn,'user':user, 'rate':rate, 'review':review})
            print("We did it")
            db.commit()
            return render_template("succes.html", message="The rate was uploaded")
        except ValueError:
            error='You already rate this book'
            return render_template("error.html", message=error)

    print(book_isbn)
    book = db.execute("SELECT * FROM book WHERE isbn = :id", {"id": str(book_isbn)}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "p7LinRAWJk3A4nnlSb1Ig", "isbns": "9781632168146"})
    if book is None:
        return render_template("error.html", message="No such book.")
    else:
        return render_template("book.html", book=book,res=res.json())


@app.route('/', methods=['POST','GET'])
def login():
    error = None
    nombre = request.form.get('username')
    contrasena = request.form.get('password')
    if request.method == 'POST':
        p=db.execute('select name, password from usuarios where name = :username and password = :contra', {'username':nombre, 'contra':contrasena}).fetchall()
        db.commit()
        if p:
            for row in p:
                print(row.name,row.password)
                if nombre == row.name or contrasena == row.password:
                    global user
                    user=nombre
                    return redirect(url_for('home'))
                else:
                    error = 'Invalid Credentials. Please try again.'
                    return render_template('login.html', error=error)
        else :
            error = 'Invalid Credentials. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html', error=error)

@app.route('/register', methods=['POST','GET'])
def register():
    error=None
    if request.method == 'POST':
        if request.form.get('usernamer') != None and request.form.get('psw')!= None:
            newname=None
            newpass=None
            newname=request.form.get('usernamer')
            newpass=request.form.get('psw')
            p=db.execute('select * from usuarios where name = :nombre', {'nombre':newname}).fetchall()
            db.commit()
            if p:
                error='The user already exists, please change your username'
                return render_template('register.html', error=error)
            else:
                db.execute('insert into usuarios (name, password) values (:nombre,:pass)', {'nombre':newname, 'pass':newpass})
                db.commit()
                return render_template('login.html', error=error)




    return render_template('register.html', error=error)
