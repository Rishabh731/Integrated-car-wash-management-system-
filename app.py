import MySQLdb.cursors
from flask import Flask, redirect, render_template, session, request, flash, url_for
from flask_mysqldb import MySQL
from datetime import datetime
from config import password
import re


app = Flask(__name__)
app.config['SECRET_KEY'] = "--------"
app.config['MYSQL_DB'] = "carwash_db2"
app.config['MYSQL_HOST'] = "localhost"app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    current_day = datetime.now().strftime("%Y-%m-%d")
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        carmake = request.form['carmake']
        cartype = request.form['cartype']
        regnumber = request.form['regnumber']
        branch = request.form['branch']
        service = request.form['service']
        date = request.form['date']
        time = request.form['time']
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Wrong Email")
        elif re.match(r'\D', phone):
            flash('Wrong phone number')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("INSERT INTO reservations VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                firstname, lastname, email, phone, carmake, cartype, regnumber, branch, service, date, time))
            mysql.connection.commit()
            flash("Order placed with Success!")
    return render_template("reservations.html", current_day=current_day)


@app.route('/view_reservation', methods=['GET', 'POST'])
def view_reservation():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        regnumber = request.form['regnumber']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM reservations WHERE firstname=%s AND lastname=%s AND regnumber=%s",
                       (firstname, lastname, regnumber))
        candidate = cursor.fetchone()

        if candidate:
            return render_template('view_reservation.html', candidate=candidate)
        else:
            flash('Candidate not found')
    return render_template('view_reservation_form.html')


@app.route('/registered_users')
def registered_users():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM reservations")
    users = cursor.fetchall()
    return render_template("registered_users.html", users=users)


@app.route('/deregister', methods=['GET', 'POST'])
def deregister():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        regnumber = request.form['regnumber']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("DELETE FROM reservations WHERE firstname=%s AND lastname=%s AND regnumber=%s", (
            firstname, lastname, regnumber))
        mysql.connection.commit()
        flash("User deregistered successfully!")
    return render_template("deregister.html")


if __name__ == '__main__':
    app.run(debug=True)
