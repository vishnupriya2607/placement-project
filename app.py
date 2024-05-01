from flask import Flask, render_template, request, redirect, url_for,session
from flask_mysqldb import MySQL
app = Flask(__name__, template_folder="../client/templates")
# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Speed@2607'  # Change this to your MySQL password
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
            'email': request.form['email']
        }

        try:
            # Connect to the database
            cur = mysql.connection.cursor()

            # Construct and execute the SQL query
            columns = ','.join(data.keys())
            values = ','.join(["'" + value + "'" for value in data.values()])
            sql_query = f"INSERT INTO students ({columns}) VALUES ({values})"
            cur.execute(sql_query)

            # Commit changes and close cursor
            mysql.connection.commit()
            cur.close()

            return 'Data added successfully'
        
        except Exception as e:
            return f'An error occurred: {str(e)}'

    return render_template('add_data.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']  # Corrected field name to 'email'
        password = request.form['password']
        loginas = request.form['loginas']  # Get loginas value from form

        # Check if the user already exists in the database
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s", (email,))
        existing_user = cur.fetchone()

        if existing_user:
            return 'User already exists. Please log in.'
        else:
            # Insert new user into the database
            cur.execute("INSERT INTO login (email, password, loginas) VALUES (%s, %s, %s)", (email, password, loginas))
            mysql.connection.commit()

            # Redirect the user to the appropriate dashboard based on their role
            if loginas == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif loginas == 'student':
                # Fetch student details from the students table based on email
                cur.execute("SELECT * FROM students WHERE email = %s", (email,))
                student_details = cur.fetchone()
                
                print("SQL Query:", cur.statement)  # Print SQL query for debugging
                print("Student Details:", student_details)  # Print student details for debugging

                if student_details:
                    # Render the student dashboard template with the fetched student details
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

        # Check if the email and password match in the login table
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM login WHERE email = %s AND password = %s", (email, password))
        user = cur.fetchone()

        if user:
            # If user exists, determine the role (admin or student)
            loginas = user[3]  # Assuming the role is stored in the third column
            
            if loginas == 'admin':
                return redirect(url_for('admin_dashboard'))
            elif loginas == 'student':
                # Fetch student details from the students table based on email
                cur.execute("SELECT * FROM students WHERE email = %s", (email,))
                student_details = cur.fetchone()
                
                if student_details:
                    # Render the student details template with the fetched student details
                    return render_template('student_details.html', student_details=student_details)
                else:
                    return 'Student details not found'
        else:
            return 'Invalid email or password'

    return render_template('signin.html')

@app.route('/add_drive', methods=['GET', 'POST'])
def add_drive():
    if request.method == 'POST':
        data = {
            'company_name': request.form['company_name'],
            'company_description': request.form['company_description'],
            'date': request.form['date'],
            'eligibility_criteria': request.form['eligibility_criteria']
        }
        try:
            # Connect to the database
            cur = mysql.connection.cursor()

            # Construct and execute the SQL query with parameterized values
            sql_query = "INSERT INTO drives (company_name, company_description, date, eligibility_criteria) VALUES (%s, %s, %s, %s)"
            cur.execute(sql_query, (data['company_name'], data['company_description'], data['date'], data['eligibility_criteria']))

            # Commit changes and close cursor
            mysql.connection.commit()
            cur.close()

            return 'Data added successfully'
        
        except Exception as e:
            return f'An error occurred: {str(e)}'

    return render_template('add_drive.html')
@app.route('/student_dashboard')
def student_dashboard():
    # Fetch drives from the database
    cur = mysql.connection.cursor()
    cur.execute("SELECT company_name, company_description, date, eligibility_criteria FROM drives")
    drives = cur.fetchall()
    cur.close()

    # Convert each tuple to a dictionary for easier access in the template
    drives_list = []
    for drive in drives:
        drive_dict = {
            'company_name': drive[0],
            'company_description': drive[1],
            'date': drive[2],
            'eligibility_criteria': drive[3]
        }
        drives_list.append(drive_dict)

    # Display drives in the student dashboard template
    return render_template('student_drive.html', drives=drives_list)

@app.route('/admin_dashboard')
def admin_dashboard():
    # Admin dashboard logic
    # For example, provide options to schedule new placement drives and manage company details
    return render_template('admin_dashboard.html')
          

if __name__ == '__main__':
    app.run(debug=True)
