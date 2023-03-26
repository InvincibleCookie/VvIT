from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="qewrytuoip",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html', insert_login='', insert_password='')


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == '':
                return render_template('login.html', insert_password=password, empty_login=True)
            elif password == '':
                return render_template('login.html', insert_login=username, empty_password=True)
            try:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('account.html', full_name=records[0][1], login=records[0][2],
                                       password=records[0][3])

            except IndexError:
                return render_template('login.html', not_in_base=True)
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name == '' or login == '' or password == '':
            return render_template('registration.html', insert_name=name, insert_login=login,
                                   insert_password=password, smth_empty=True)

        cursor.execute("SELECT * FROM service.users WHERE login = %s", (login,))
        if cursor.fetchone():
            return render_template('registration.html', insert_name=name, insert_login='',
                                   insert_password=password, alrd_use=True)
        cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                       (str(name), str(login), str(password)))
        conn.commit()

        return redirect('/login/')

    return render_template('registration.html', insert_name='', insert_login='', insert_password='')


if __name__ == '__main__':
    app.run(debug=True)
