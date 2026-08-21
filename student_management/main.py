from flask import Flask, render_template, redirect, url_for, request
import sqlite3

app = Flask(__name__)

# Connect the database
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory=sqlite3.Row
    return conn

# Create the database
def create_db():
    conn=get_db_connection()

    conn.execute('''
    CREATE TABLE IF NOT EXISTS student(
    id int PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    course TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()


# Home page - show the students details

@app.route('/')
def index():
    conn=get_db_connection()

    students=conn.execute(" select * from student").fetchall()

    conn.close()

    return render_template('index.html', students=students)

# Add students
@app.route('/add', methods=['GET','POST'])
def add_student():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        course=request.form['course']

        conn= get_db_connection()

        conn.execute('''
        INSERT INTO student(name, email, course) values (?,?,?)
        ''', (name, email, course))

        conn.commit()
        conn.close()

        return redirect('/')
    return render_template('add_student.html')


# Update the student details

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn= get_db_connection()

    student = conn.execute(
        'select * from student where id =?',(id,)
    ).fetchone()

    # when not exist
    if student is None:
        conn.close()
        return 'students not exist', 404


    # edit the students

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']


        student = conn.execute('''
        update student set  name=?, email=?, course=? where id=?
        ''',( name, email,course,id))

        conn.commit()
        conn.close()

        return redirect(url_for('index'))
    conn.close()

    return render_template('edit.html', student=student)

# Delete the students 

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn=get_db_connection()

    conn.execute('''
    DELETE from student where id=?
    ''', (id,))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))






if __name__ == "__main__":
    create_db()
    app.run(debug=True)
