from plates import app, db
from flask import render_template, request, redirect, url_for, session
from sqlalchemy import text
# Brute force
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(
    get_remote_address, app=app, default_limits=["20 per day", "50 per hour"]
)
@app.route('/')
def index():
    cookie = request.cookies.get('name')
    return render_template('index.html', cookie=cookie)

@app.route('/index')
def index_page():
    cookie = request.cookies.get('name')
    return render_template('index.html', cookie=cookie)

@app.route('/plate', methods=['GET', 'POST'])
def plate():
    cookie = request.cookies.get('name')
    id = request.args.get('id')
    abbr = request.args.get('kuerzel')
    print(abbr)
    if abbr:
        print(f"Searching for: {abbr}")
        qstmt = text("SELECT * FROM gerplates WHERE kuerzel = :abbr")
        print(qstmt)
        result = db.session.execute(qstmt, {'abbr': abbr})
        items = result.fetchall()
        print(result)
        return render_template('plate.html', abbr=abbr, items=items, cookie=cookie)
    return render_template('plate.html', cookie=cookie)

@app.route('/plates', methods=['GET', 'POST'])
def plates():
    cookie = request.cookies.get('name')
    print(">>>>>>>platespage", cookie)
    if not request.cookies.get('name'):
        return redirect(url_for('index'))
    qstmt = text("SELECT * FROM gerplates")
    res = db.session.execute(qstmt)
    items = res.fetchall()
    return render_template('plates.html', items=items, cookie=cookie)

@app.route('/delPlates', methods=['GET', 'POST'])
def delPlates():
    if not request.cookies.get('name'):
        return redirect(url_for('index'))
    kuerzel = request.form.get('kuerzel')
    print(f"Try to delete {kuerzel}")
    if request.method == 'POST':
        try:
            qstmt = text("DELETE FROM gerplates WHERE kuerzel= :kuerzel")
            res = db.session.execute(qstmt, {"kuerzel": kuerzel})
            db.session.commit()
            print(f"Deleted '{res.rowcount}' Entrys where kuerzel= {kuerzel} ")
        except Exception as e:
            print(f"Error Del entry {e}")
            db.session.rollback()

    return redirect(url_for('plates'))

@app.route('/addPlate', methods=['GET', 'POST'])
def addPlate_page():
    cookie = request.cookies.get('name')
    if request.method == 'POST':
        kuerzel = request.form.get('kuerzel')
        city = request.form.get('city')
        bundesland = request.form.get('bundesland')
        country = request.form.get('country')
        print(kuerzel, city, bundesland, country)

        if kuerzel is None or isinstance(kuerzel, str) is False or len(kuerzel) < 1:
            print("Kuerzel is wrong")
            return render_template('addPlate.html', cookie=cookie)
        if city is None or isinstance(city, str) is False or len(city) < 1:
            print("City is wrong")
            return render_template('addPlate.html', cookie=cookie)
        if bundesland is None or isinstance(bundesland, str) is False or len(bundesland) < 1:
            return render_template('addPlate.html', cookie=cookie)
        if country is None or isinstance(country, str) is False or len(country) < 1:
            print("Country is wrong")
            return render_template('addPlate.html', cookie=cookie)

        qstmt = text("SELECT * FROM gerplates WHERE kuerzel= :kuerzel")
        print(qstmt)
        res = db.session.execute(qstmt, {'kuerzel': kuerzel})
        kurz = res.fetchall()

        if kurz:
            print("Kuerzel exists")
            return render_template('plates.html', cookie=cookie)
        else:
            qstmt = text("INSERT INTO gerplates (kuerzel, city, bundesland, country) VALUES (:kuerzel, :city, :bundesland, :country)")
            res = db.session.execute(qstmt, {'kuerzel': kuerzel, 'city': city, 'bundesland': bundesland, 'country': country})
            db.session.commit()

            if res.rowcount > 0:
                resp = redirect('/plates')
                return resp
            else:
                print('Something went wrong... I can feel it... again')
    return render_template('addPlate.html', cookie=cookie)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'GET':
        lastName = request.args.get('lastName')
        firstName = request.args.get('firstName')
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')

        if firstName is None or isinstance(firstName,str) is False or len(firstName) < 2:
            print('Somthings worng with your firstName')
            return render_template('register.html', cookie=None)
        if lastName is None or isinstance(lastName,str) is False or len(lastName) < 2:
            print('Somthings worng with your lastName')
            return render_template('register.html', cookie=None)
        if username is None or isinstance(username,str) is False or len(username) < 2:
            print('Somthings worng with your username')
            return render_template('register.html', cookie=None)
        if email is None or isinstance(email,str) is False or len(email) < 2:
            print('Somthings worng with your email')
            return render_template('register.html', cookie=None)
        if password is None or isinstance(password,str) is False or len(password) < 2:
            print('Somthings worng with your password')
            return render_template('register.html', cookie=None)

        qstmt = f"SELECT * FROM plateusers WHERE username ='{username}'"
        print(qstmt)
        res = db.session.execute(text(qstmt))
        user = res.fetchall()

        if user:
            print('User already exists')
            return render_template('register.html', cookie=None)
        else:
            qstmt = f"INSERT INTO plateusers (firstName, lastName, username, email, password) VALUES ('{firstName}', '{lastName}', '{username}', '{email}', '{password}')"
            res = db.session.execute(text(qstmt))
            db.session.commit()

            if res.rowcount > 0:
                resp = redirect('/login')
                return resp
            else:
                print('Something went wrong... I can feel it')
    return render_template('register.html', cookie=None)


@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def login_page():
    if request.method == 'POST':
        username = request.form.get('Username')
        password = request.form.get('Password')

        if username is None or isinstance(username,str) is False or len(username) < 1:
            print("Something with username is wrong 1")
            return render_template('login.html')

        if password is None or isinstance(password,str) is False or len(password) < 1:
            print("Something with password is wrong 2")
            return render_template('login.html')

        qstmt = f"SELECT * FROM plateusers WHERE username = :username AND password = :password;" # Query Statement
        print(f"qstmt: {qstmt}")
        result = db.session.execute(text(qstmt), {'username' :username, 'password' : password})
        user = result.fetchall()

        if not user:
            print("Something wrong 3")
            return render_template('login.html')

        resp = redirect('/')
        resp.set_cookie('name', username,
                        samesite='Strict',
                        httponly=True)
        return resp
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    resp = redirect('/')
    resp.set_cookie('name', '', expires=0)
    return resp