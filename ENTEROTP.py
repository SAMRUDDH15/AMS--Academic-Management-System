from datetime import datetime
from flask import Blueprint, jsonify, request, session
from extensions import db

enterotp_bp = Blueprint('enterotp', __name__)

class Student(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    register_number = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)

class Subject(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=True)

class Attendance(db.Model):
    __table_args__ = {'extend_existing': True}  # Add this line

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    subject_id = db.Column(db.String(50), db.ForeignKey('subject.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    marked = db.Column(db.Boolean, nullable=False)

  

class otptable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String(6), nullable=False)
    subject = db.Column(db.String(50), nullable=True)
    section = db.Column(db.String(10), nullable=False)
    generated_time = db.Column(db.DateTime, nullable=False, default=datetime.now())




@enterotp_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    otp = request.form.get('otp')
    subject = request.form.get('subject')
    section = request.form.get('section')

    reg_number = session.get('reg_number')  # Assuming registration number is stored in the session

    # Retrieve the student from the Student table based on registration number
    student = Student.query.filter_by(register_number=reg_number).first()
    if not student:
        response = {'message': 'Invalid student'}
        return jsonify(response)

    # Retrieve the subject from the Subject table
    if subject:
        subject_record = Subject.query.filter_by(name=subject).first()
        if not subject_record:
            response = {'message': 'Invalid subject'}
            return jsonify(response)

    # Mark the attendance for the corresponding student in the database
    attendance = Attendance(
        student_id=student.register_number,  # Store registration number in student_id column
        student_name=student.name,  # Store name of the student
        subject_id=subject_record.id if subject_record else None,
        date=datetime.now().date(),
        time=datetime.now().time(),
        section=section,
        marked=True
    )

    db.session.add(attendance)
    db.session.commit()

    # Prepare the response with student, department, and subject details
    response = {
        'message': 'Attendance marked successfully',
        'student_name': student.name,
        'department': student.department,
        'subject': subject_record.name if subject_record else None
    }

    return jsonify(response)

