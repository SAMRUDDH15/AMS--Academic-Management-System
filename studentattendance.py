from flask import Blueprint, render_template, request
from extensions import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from main import app
from flask import send_file

studentattendance_bp = Blueprint('studentattendance', __name__)

class Student(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    register_number = db.Column(db.String(255), nullable=True)
    department = db.Column(db.String(255), nullable=True)

class Subject(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(255), nullable=True)

class Attendance(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    subject_id = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    marked = db.Column(db.Boolean, nullable=False)

@studentattendance_bp.route('/attendance123', methods=['GET', 'POST'])
def lecturer_attendance():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        date_type = request.form.get('date_type')
        reg_number = request.form.get('reg_number')

        if date_type == 'single_date':
            single_date = request.form.get('single_date')
            attendance = Attendance.query.filter_by(subject_id=subject_id, date=single_date, student_id=reg_number).all()
        elif date_type == 'date_range':
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            attendance = Attendance.query.filter(Attendance.subject_id == subject_id,
                                                 Attendance.date.between(start_date, end_date),
                                                 Attendance.student_id == reg_number).all()
        else:
            attendance = []

        subjects = Subject.query.all()
        return render_template('student_attendance.html', attendance=attendance, subjects=subjects, reg_number=reg_number)
    else:
        subjects = Subject.query.all()
        return render_template('student_attendance.html', subjects=subjects)





@studentattendance_bp.route('/download_studentattendance', methods=['GET'])
def download_studentattendance():
    subject_id = request.args.get('subject_id')
    date = request.args.get('date')
    reg_number = request.args.get('reg_number')

    attendance = Attendance.query.filter_by(subject_id=subject_id, date=date, student_id=reg_number).all()

    # Prepare the CSV file content
    csv_content = "Student ID,Subject,Date,Marked\n"
    for record in attendance:
        csv_content += f"{record.student_id},{record.subject_id},{record.date},{record.marked}\n"

    # Create the CSV file
    filename = "attendance.csv"  # Name of the downloaded file
    filepath = os.path.join(app.root_path, filename)  # Absolute file path
    with open(filepath, 'w', newline='') as file:
        file.write(csv_content)

    # Send the file for download
    return send_file(filepath, as_attachment=True)
