from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# Fetch all or search students
def get_students(query=None):
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if query:
        cur.execute("SELECT * FROM students WHERE name LIKE ?", ("%" + query + "%",))
    else:
        cur.execute("SELECT * FROM students")

    students = cur.fetchall()
    con.close()
    return students


@app.route("/")
def index():
    query = request.args.get("query")
    students = get_students(query)
    return render_template("index.html", students=students)


@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        con = sqlite3.connect("students.db")
        con.execute("INSERT INTO students (name, age, course) VALUES (?, ?, ?)",
                    (name, age, course))
        con.commit()
        con.close()

        flash("Student added successfully!")
        return redirect("/")

    return render_template("add_student.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    con = sqlite3.connect("students.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]

        cur.execute("UPDATE students SET name=?, age=?, course=? WHERE id=?",
                    (name, age, course, id))
        con.commit()
        con.close()
        flash("Student updated successfully!")
        return redirect("/")

    cur.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cur.fetchone()
    con.close()
    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:id>")
def delete_student(id):
    con = sqlite3.connect("students.db")
    con.execute("DELETE FROM students WHERE id=?", (id,))
    con.commit()
    con.close()
    flash("Student deleted!")
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
