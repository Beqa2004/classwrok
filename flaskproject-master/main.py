from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from newpy import blueprint

engine = create_engine("mysql+mysqlconnector://root:Beqakhitarishvili123@localhost/world", echo=True)
connection = engine.connect()
Base = declarative_base()


app = Flask(__name__)

app.register_blueprint(blueprint, url_prefix ="/courses")

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer,autoincrement=True,primary_key=True )
    name = Column(String(30) )
    age = Column(Integer)
    semester = Column(Integer)

    def __repr__(self):
        return self.name
Base.metadata.create_all(engine)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        print(request.form)
        name = request.form.get("name")
        age = request.form.get("age")
        semester = request.form.get("semester")
        print(name, age, semester)
        studnet1 = Student(name = name, age = age, semester =semester)
        with sessionmaker(bind=engine)() as session:
            session.add(studnet1)
            session.commit()
        return redirect(url_for("index"))
    with sessionmaker(bind=engine)() as session:
        students = session.query(Student).all()
        for student in students:
            print(student.name,student.age)
        print(students)
    return render_template("index.html", title="indexpafe", students=students)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html", data=[4394892,4244954,5939342,23942012], title="indexpafe")

@app.route("/students/<int:student_id>")
def student_detail(student_id):
    with sessionmaker(bind=engine)() as session:
        student = session.query(Student).get(student_id)
    print(student)
    return render_template("student_detail.html", student = student)

@app.route("/students/<int:student_id>/delete")
def delete_student(student_id):
    with sessionmaker(bind=engine)() as session:
        if request.method == "GET":
            deleted_student = session.query(Student).get(student_id)
            session.delete(deleted_student)
            session.commit()
        print(student_id)
    return redirect(url_for("index"))

@app.route("/students/<int:student_id>/update", methods = ["GET", "POST"])
def update_student(student_id):
    if request.method == "GET":
        return render_template("update.html")
    elif request.method == "POST":
        with sessionmaker(bind=engine)() as session:
            student = session.query(Student).get(student_id)
            print(student)
            print(request.form)
            student.name = request.form.get("name")
            student.age = request.form.get("age")
            student.semester = request.form.get("semester")
            session.commit()
        return redirect(url_for("student_detail", student_id = student_id ))


if __name__ == "__main__":
    app.run(debug=True)
    