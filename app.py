from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///assignments.db"
db = SQLAlchemy(app)

class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    grade = db.Column(db.String(1), nullable=True)
    state = db.Column(db.String(10), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=True)
    updated_at = db.Column(db.DateTime, nullable=False)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

class Principal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

@app.route("/principal/assignments", methods=["GET"])
def get_principal_assignments():
    principal_id = request.headers.get("X-Principal").get("principal_id")
    assignments = Assignment.query.filter_by(state="SUBMITTED").all()
    return jsonify({"data": [{"id": a.id, "content": a.content, "grade": a.grade, "state": a.state} for a in assignments]})

@app.route("/principal/teachers", methods=["GET"])
def get_principal_teachers():
    principal_id = request.headers.get("X-Principal").get("principal_id")
    teachers = Teacher.query.all()
    return jsonify({"data": [{"id": t.id, "user_id": t.user_id} for t in teachers]})

@app.route("/principal/assignments/grade", methods=["POST"])
def grade_assignment():
    principal_id = request.headers.get("X-Principal").get("principal_id")
    payload = request.get_json()
    assignment_id = payload.get("id")
    grade = payload.get("grade")
    assignment = Assignment.query.get(assignment_id)
    if assignment:
        assignment.grade = grade
        db.session.commit()
        return jsonify({"data": {"id": assignment.id, "content": assignment.content, "grade": assignment.grade, "state": assignment.state}})
    return jsonify({"error": "Assignment not found"}), 404
