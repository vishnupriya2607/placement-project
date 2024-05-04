from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Speed@2607'  
app.config['MYSQL_DB'] = 'placement_database'

mysql = MySQL(app)

@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        data = {
            'name': request.form['name'],
            'rollno': request.form['rollno'],
            'department': request.form['department'],
            'year_of_passing': request.form['year_of_passing'],
            'dob': request.form['dob'],
            'email': request.form['email'],
            'placement_willing': request.form['placement_willing'],
            'Gcpa': request.form['Gcpa']
        }

        try:
            cur = mysql.connection.cursor()
            columns = ','.join(data.keys())
            values = ','.join(["'" + value + "'" for value in data.values()])
            sql_query = f"INSERT INTO students ({columns}) VALUES ({values})"
            cur.execute(sql_query)
            mysql.connection.commit()
            cur.close()

            return 'Data added successfully'
        
        except Exception as e:
            return f'An error occurred: {str(e)}'

    return render_template('add_data.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']  
        password = request.form['password']
        loginas = request.form['loginas']  
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return 'User already exists. Please log in.'
        else:
            cur.execute("INSERT INTO login (email, password, loginas) VALUES (%s, %s, %s)", (email, password, loginas))
            mysql.connection.commit()
            if loginas == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif loginas == 'student':
                
                cur.execute("SELECT * FROM students WHERE email = %s", (email,))
                student_details = cur.fetchone()
                
                print("SQL Query:", cur.statement) 
                print("Student Details:", student_details) 

                if student_details:
                    return render_template('student_details.html', student_details=student_details)
                else:
                    return 'Student details not found'

    return render_template('signup.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        print(request.form)
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user:
            loginas = user[3]  
            if loginas == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif loginas == 'student':
                return redirect(url_for('student_details', email=email))
        else:
            return 'Invalid email or password'

    return render_template('signin.html')

@app.route('/student_details/<email>')
def student_details(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE email = %s", (email,))
    student_details = cur.fetchone()

    if student_details:
        return render_template('student_details.html', student_details=student_details)
    else:
        return 'Student details not found'

@app.route('/add_drive', methods=['GET', 'POST'])
def add_drive():
    if request.method == 'POST':
        try:
            # Extract form data
            company_name = request.form['company_name']
            company_description = request.form['company_description']
            date = request.form['date']
            eligibility_criteria = request.form['eligibility_criteria']
            
            # Handle image path
            image_path = request.form['image_path']

            # Insert data into MySQL database
            cur = mysql.connection.cursor()
            sql_query = "INSERT INTO drives (company_name, company_description, date, eligibility_criteria, image_path) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql_query, (company_name, company_description, date, eligibility_criteria, image_path))
            mysql.connection.commit()
            cur.close()

            return 'Data added successfully'
        
        except Exception as e:
            return f'An error occurred: {str(e)}'

    return render_template('add_drive.html')

@app.route('/student_dashboard')
def student_dashboard():
   
    cur = mysql.connection.cursor()
    cur.execute("SELECT company_name, company_description, date, eligibility_criteria FROM drives")
    drives = cur.fetchall()
    cur.close()

    
    drives_list = []
    for drive in drives:
        drive_dict = {
            'company_name': drive[0],
            'company_description': drive[1],
            'date': drive[2],
            'eligibility_criteria': drive[3]
        }
        drives_list.append(drive_dict)
    return render_template('student_dashboard.html', drives=drives_list)


@app.route('/companies')
def companies():
    return render_template('companies.html')

@app.route('/company/<company_name>')
def company_page(company_name):
    return render_template(f"{company_name}.html")


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')
@app.route('/')
def profile_page():
    cur = mysql.connection.cursor()
    cur.execute('SELECT name, rollno, department, email, year_of_passing, dob, SSLC, HSC, diploma, UG, PG, Backlog_History, Current_Backlogs, place, work FROM students WHERE email="sugantha.22cse@kongu.edu"')
    data = cur.fetchone()  
    cur.close()
    
    return render_template('Profile.html', data=data)


@app.route('/contact')
def alumni():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM alumni")
    alumni_data = cursor.fetchall()
    cursor.close()
    return render_template('Contact.html', alumni_data=alumni_data)

@app.route('/update', methods=['POST'])
def update_profile():
    if request.method == 'POST':
        name = request.form['name']
        roll_no = request.form['roll_no']
        department = request.form['department']
        email = request.form['email']
        year_of_passing = request.form['year_of_passing']
        date_of_birth = request.form['date_of_birth']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE students SET name = %s, rollno = %s, department = %s, email = %s, year_of_passing = %s, dob = %s where email='sugantha.22cse@kongu.edu'", (name, roll_no, department, email, year_of_passing, date_of_birth))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/')
    
@app.route('/update_academic', methods=['POST'])
def update_academic():
    if request.method == 'POST':
        sslc = request.form['SSLC']
        hsc = request.form['hsc']
        diploma = request.form['diploma']
        ug = request.form['ug']
        pg = request.form['pg']
        backlog_history = request.form['backlog_history']
        current_backlogs = request.form['current_backlogs']
        place = request.form['place']
        work = request.form['work']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE students SET SSLC = %s, HSC = %s, Diploma = %s, UG = %s, PG = %s, Backlog_History = %s, Current_Backlogs = %s, place = %s, work = %s WHERE email = 'sugantha.22cse@kongu.edu'", (sslc, hsc, diploma, ug, pg, backlog_history, current_backlogs, place, work))
        mysql.connection.commit()
        cur.close()
        
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
