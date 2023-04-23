from flask import Flask, render_template, url_for, request, flash, g, session, redirect

import sqlite3


app = Flask(__name__)
#app.config['SECRET_KEY'] = 'SomethingWhatNo1CanGuess!'


def get_db():
#połączenie z bazą danych gymrent.db
    if not hasattr(g, 'sqlite_db'): #Metoda hasattr() zwraca wartość true, jeśli obiekt ma podany atrybut nazwany
        conn = sqlite3.connect('data/gymrent.db')
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
    return g.sqlite_db

@app.teardown_appcontext
#zakończenie połączenia z bazą danych
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/', methods=['GET','POST'])
#strona początkowa
def home():
    if request.method == 'GET':
        return render_template('home_page.html')
    else:
        miastoInput = ''
        if 'miastoInput' in request.form:
            miastoInput = request.form['miastoInput']
            if miastoInput == '':
                wyniki = ['0']
                return render_template('home_page.html', miastoInput='Brak wyszukiwań', wyniki = wyniki) 
            else:
                db = get_db()
                sql_command1 = 'select count(city) from gyms where city=?;'
                sql_command2 = 'select street,price from gyms where city=?;'
                cur1 = db.execute(sql_command1, [miastoInput])
                cur2 = db.execute(sql_command2, [miastoInput])
                wyniki = cur1.fetchall()
                hale = cur2.fetchall()

                return render_template('home_page.html', miastoInput=miastoInput, wyniki=wyniki, hale=hale)


@app.route('/rejestracja', methods=['GET','POST'])
def rejestracja():
    if request.method == 'GET':
        return render_template('register_page.html')
    else:
        email = request.form['inputEmail4']
        password = request.form['inputPassword4']
        password = password.encode('utf-8')
        name = request.form['inputName']
        surname = request.form['inputSurname']
        city = request.form['inputCity']
        street = request.form['inputAddress']
        number = request.form['inputNr']
        userType = request.form['flexRadioDefault']
        db = get_db()
        sql_command = 'select email from user where email = ?;'
        cur = db.execute(sql_command, [email])
        uzytkownik = cur.fetchall()
        if uzytkownik:
            return render_template('register_page.html')
        else:
            sql_command2 = 'insert into user(email,password,name,surname,city,street,number,userType) values(?,?,?,?,?,?,?,?);'
            db.execute(sql_command2, [email,'hashedPassword',name,surname,city,street,number,userType])
            db.commit()
            return render_template('log_page.html')


@app.route('/logowanie', methods=['GET','POST'])
def logowanie():
    if request.method == 'GET':
        return render_template('log_page.html')
    else:
        email = request.form['exampleInputEmail1']
        password = request.form['exampleInputPassword1']
        db = get_db()
        sql_command = 'select password,userType from user where email = ?;'
        cur = db.execute(sql_command, [email])
        hasla = cur.fetchall()
        if hasla:
            for haslo in hasla:
                # if bcrypt.checkpw(password.encode('utf-8'),haslo[0]):
                    if haslo[1] == 0:
                        return render_template('user_page1.html', email=email)
                    else:
                        return render_template('user_page2.html', email=email)
                # else:
                    # return render_template('log_page.html')
        else:
            return render_template('log_page.html')



@app.route('/user1', methods=['GET','POST'])
def user():
    if request.method == 'GET':
        return render_template('user_page1.html')
    else:
        miastoInput = ''
        if 'miastoInput' in request.form:
            miastoInput = request.form['miastoInput']
            if miastoInput == '':
                wyniki = ['0']
                return render_template('user_page1.html', miastoInput='Brak wyszukiwań', wyniki = wyniki) 
            else:
                db = get_db()
                sql_command1 = 'select count(city) from gyms where city=?;'
                sql_command2 = 'select street,price from gyms where city=?;'
                cur1 = db.execute(sql_command1, [miastoInput])
                cur2 = db.execute(sql_command2, [miastoInput])
                wyniki = cur1.fetchall()
                hale = cur2.fetchall()

                return render_template('user_page1.html', miastoInput=miastoInput, wyniki=wyniki, hale=hale)

@app.route('/user2', methods=['GET','POST'])
def add():
    if request.method == 'GET':
        return render_template('user_page2.html')
    else:
        city = request.form['inputCity']
        street = request.form['inputAdres']
        price = request.form['inputPrice']
        email = request.form['inputEmail']
        db = get_db()
        sql_command = 'insert into gyms(city,street,price,userID) values(?,?,?,?);'
        sql_command2 = 'select city,street,price from gyms where userID=?;'
        db.execute(sql_command, [city,street,price,email])
        cur = db.execute(sql_command2, [email])
        wyniki = cur.fetchall()
        db.commit()
        return render_template('user_page2.html', wyniki=wyniki, email=email)


if __name__ == '__main__':
    app.run()
    