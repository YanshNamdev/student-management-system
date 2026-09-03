from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    students = Student.query.all()
    return render_template("index.html", students=students)


@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    course = request.form["course"]
    email = request.form["email"]

    student = Student(name=name, course=course, email=email)
    db.session.add(student)
    db.session.commit()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete_student(id):
    student = Student.query.get(id)

    if student:
        db.session.delete(student)
        db.session.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)