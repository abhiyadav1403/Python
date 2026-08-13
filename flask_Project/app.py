from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# connect the database
def get_db():
    conn = sqlite3.connect('Student.db')
    # cursor=connect.cursor()
    conn.row_factory=sqlite3.Row
    return conn

# create database
def create_table():
    conn = get_db()

    conn.execute('''
                CREATE TABLE IF NOT EXISTS students(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                course TEXT NOT NULL
                )    
    ''')

    conn.commit()
    conn.close()



# Home page -show students

@app.route('/')
def index():
    conn = get_db()

    students = conn.execute(
        'SELECT * FROM students'
    ).fetchall()

    conn.close()

    return render_template('index.html', students=students)


# Add students
@app.route('/add', methods=['GET','POST'])
def add_student():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = get_db()

        conn.execute(
            'INSERT INTO students (name, email, course) VALUES (?,?,?) ',
            (name, email, course)
        )

        conn.commit()
        conn.close()

        return redirect("/")
    
    return render_template('add_student.html')

# Update the students.
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):

    conn = get_db()

    # get student
    student = conn.execute(
        'select * from students where id =?',
        (id,)
    ).fetchone()

    #  if student doesn't exist

    if student is None:
        conn.close()
        return 'Student not found ', 404

    # update student
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn.execute(
            'UPDATE students set name = ?, email = ?, course= ? where id = ?',
            (name, email, course,id)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn.close()

    return render_template('update_student.html', student= student)


# delete student

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = get_db()
    conn.execute(
        'DELETE FROM students WHERE id = ?',
        (id,)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))




if __name__ == "__main__":
    create_table()
    app.run(debug=True)
