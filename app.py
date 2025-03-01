from flask import Flask, render_template, request, flash, session,redirect, url_for, jsonify, make_response
import sqlite3 
# from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash

  
app = Flask(__name__) 
app.secret_key = 'your_secret_key'  
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=30)
connect = sqlite3.connect('database.db') 
connect.execute( 'CREATE TABLE IF NOT EXISTS EMPLOYEES (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT, email TEXT, designation TEXT, ctc TEXT, phone TEXT)') 
connect.execute( 'CREATE TABLE IF NOT EXISTS USERS (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, email TEXT, isActive BOOLEAN DEFAULT 1)') 
        
# connect.execute('DROP TABLE IF EXISTS USER')
def delete_record(record_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id=?', (record_id,))
    conn.commit()
    conn.close()
    flash('Record Deleted successfully!', 'success')

def get_record_by_id(record_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE id=?', (record_id,))
    record = cursor.fetchone()
    conn.close()
    return record

def update_record(id, name, email, designation, ctc, phone):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE employees
        SET name=?, email=?, designation=?, ctc=?, phone=?
        WHERE id=?
    ''', (name, email, designation, ctc, phone, id))
    conn.commit()
    conn.close()

def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256')

def verify_password(hashed_password, plain_password):
    return check_password_hash(hashed_password, plain_password)

@app.route('/') 
@app.route('/login', methods=['GET','POST'])
def login():
  
    if request.method == 'POST' and 'username' not in session:
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT username, password FROM USERS WHERE username=?', (username,))
        record = cursor.fetchone()
        conn.close()
        if record and  verify_password(record[1], password):
            session['username'] = record[0]
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid username or password')  
    else:
        if  request.method == 'GET' and 'username' in session:  
             return redirect(url_for('index'))
        return render_template('login.html')
        

@app.route('/home') 
def index(): 
    if 'username' in session:
        return render_template("index.html")
    return render_template('login.html', msg='Please login first')


@app.route('/add', methods=['GET', 'POST']) 
def add(): 
    if "username" in session:
        if request.method == 'POST': 
            name = request.form['name'] 
            email = request.form['email'] 
            designation = request.form.get('designation') 
            ctc = request.form['ctc'] 
            phone = request.form['phone']
            edit_mode = request.form.get('editMode', 'false')
            if edit_mode == 'true':
                record_id = int(request.form['recordId'])
                connect = sqlite3.connect("database.db")  
                cursor = connect.cursor()
                cursor.execute('SELECT * FROM EMPLOYEES WHERE id=?', (record_id,))
                data = cursor.fetchone()
                if data:
                    update_record(record_id, name, email, designation, ctc, phone)
                    flash(f'{name} record updated successfully!', 'success')
                else:
                    flash('No Record found', 'error')
                    return redirect(url_for('getAllEmployee'))
            else: 
                connect = sqlite3.connect("database.db")  
                cursor = connect.cursor()
                cursor.execute('SELECT * FROM EMPLOYEES')
                data = cursor.fetchall()
                emailList = []
                for a in data:
                    emailList.append(a[2])
                if email not in emailList:   
                    cursor.execute("INSERT INTO EMPLOYEES (name,email,designation,ctc,phone) VALUES (?,?,?,?,?)", (name, email, designation, ctc, phone)) 
                    connect.commit()
                    connect.close()
                    flash(f'{name} added successfully!', 'success')
                else:
                    flash('Duplicate Record found', 'error')
                    return render_template('add.html') 
            return redirect(url_for('getAllEmployee')) 
        else: 
            return render_template('add.html') 
    return render_template('login.html', msg='Please login first')
    

@app.route('/getAllEmployee') 
def getAllEmployee(): 
    if "username" in session:
        connect = sqlite3.connect('database.db') 
        cursor = connect.cursor() 
        cursor.execute('SELECT * FROM EMPLOYEES')  
        data = cursor.fetchall()
        connect.close()
        return render_template("allEmployee.html", data=data)
    return render_template('login.html', msg='Please login first') 


@app.route('/edit/<int:record_id>')
def edit(record_id):
    if "username" in session:
        record = get_record_by_id(record_id)
        if record:
            return render_template('edit.html', record=record)
        else:
            flash(f"No record associated with this id: {record_id}", 'error')
            return redirect(url_for('index'))
    return render_template('login.html', msg='Please login first')


@app.route('/delete/<int:record_id>')
def delete(record_id):
    if "username" in session:
        record = get_record_by_id(record_id)
        if record:
            delete_record(record_id)
            return redirect(url_for('getAllEmployee'))
        else:
            flash(f"No record associated with this id: {record_id}", 'error')
            return redirect(url_for('index'))
    return render_template('login.html', msg='Please login first')


@app.route('/get_user_details')
def get_user_details():
    if "username" in session:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT* FROM USERS WHERE username=?', (session['username'],))
        user_details = cursor.fetchone()
        conn.close()
        return jsonify(user_details)
    return render_template('login.html', msg='Please login first')


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT* FROM USERS WHERE username=?', (username,))
        data = cursor.fetchone()
        if data:
             flash('Username already exists', 'error')
        else:
            hashed_password = hash_password(password)
            cursor.execute('INSERT INTO USERS (username, password) VALUES (?,?)', (username, hashed_password))
            conn.commit()
            conn.close()
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/updateUser', methods=['GET', 'POST']) 
def updateUser():
    if "username" in session:
        if request.method == 'GET':
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, password FROM USERS WHERE username=?', (session['username'],))
            record = cursor.fetchone()
            conn.close()
            return render_template('changePassword.html', record=record)
     
        if request.method == 'POST':
            userId = request.form['userId']
            newPassword = request.form['newPassword']
            oldPassword = request.form['oldPassword']
            confirmPassword = request.form['confirmPassword']
            hashNewPassword = hash_password(newPassword)
            # hashOldPassword = hash_password(oldPassword)
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, password FROM USERS WHERE username=?', (session['username'],))
            rec = cursor.fetchone()
            print("-------------------->",verify_password(rec[2], oldPassword))
            if rec and verify_password(rec[2], oldPassword):
                if newPassword != confirmPassword :
                    flash("New and confirm password not matched", 'error')
                    return render_template('changePassword.html', record=rec)
                elif newPassword == oldPassword:
                    flash("Old and new password can not same", 'error')
                    return render_template('changePassword.html', record=rec)
                else:
                    cursor.execute('UPDATE USERS SET password=? WHERE id=?', (hashNewPassword, userId))
                    conn.commit()
                    conn.close()
                    flash('Password updated successfully!', 'success')
                    session.pop("username", None)
                    return redirect(url_for('login'))
            else:
                flash("Old Password Is Incorrect", 'error')
                conn = sqlite3.connect('database.db')
                cursor = conn.cursor()
                cursor.execute('SELECT id, username, password FROM USERS WHERE id=?', (userId,))
                record = cursor.fetchone()
                conn.close()
                return render_template('changePassword.html', record=record)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop("username", None)
    return redirect(url_for('login'))

def search_employee(search_query):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM EMPLOYEES WHERE id=?", (search_query,))
        employee_by_id = cursor.fetchone()
        if employee_by_id:
            return [employee_by_id]

        cursor.execute("SELECT * FROM EMPLOYEES WHERE email=?", (search_query,))
        employee_by_email = cursor.fetchone()
        if employee_by_email:
            return [employee_by_email]

        cursor.execute("SELECT * FROM EMPLOYEES WHERE name LIKE ?", (f"%{search_query}%",))
        employees_by_name = cursor.fetchall()
        return employees_by_name

    except Exception as e:
        print(e)
        return None

    finally:
        conn.close()

@app.route('/search', methods=['GET'])
def search():
    if "username" in session:
        search_query = request.args.get('searchEmp', '')
        print("----->",search_query)
        data = search_employee(search_query)
        if not data:
            flash('No records found for the search query.', 'error')
        return render_template('allEmployee.html', data=data)
    return render_template('login.html', msg='Please login first')

@app.route('/holidayList', methods=['GET'])
def holidayList():
    if "username" in session:
        return render_template('holidayList.html')
    return render_template('login.html', msg='Please login first')


if __name__ == '__main__': 
    app.run(debug=True) 