from flask import Blueprint, render_template, request, send_file
from extensions import db
from flask import Flask, render_template, request, send_file, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from __main__ import app


lectureattendence_bp = Blueprint('lectureattendence', __name__)


class Attendance(db.Model):
    __tablename__ = 'attendance'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), nullable=False)
    student_name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    subject_id = db.Column(db.String(50), db.ForeignKey('subject.id'), nullable=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    marked = db.Column(db.Boolean, default=False, nullable=False)


class Subject(db.Model):
    __tablename__ = 'subject'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)


@lectureattendence_bp.route('/lecturer_attendance', methods=['GET', 'POST'])
def lecturer_attendance():
    if request.method == 'POST':
        subject_id = request.form.get('subject_id')
        section = request.form.get('section')
        date = request.form.get('date')
        attendance = Attendance.query.filter_by(subject_id=subject_id, section=section, date=date).all()
        subjects = Subject.query.all()
        return render_template('lecturer_attendance.html', attendance=attendance, subjects=subjects)
    else:
        subjects = Subject.query.all()
        return render_template('lecturer_attendance.html', subjects=subjects)


@lectureattendence_bp.route('/download_attendance')
def download_attendance():
    subject_id = request.args.get('subject_id')
    section = request.args.get('section')
    date = request.args.get('date')
    attendance = Attendance.query.filter_by(subject_id=subject_id, section=section, date=date).all()

    # Prepare the CSV file content
    csv_content = "Student ID,Student Name,Section,Date\n"
    for record in attendance:
        csv_content += f"{record.student_id},{record.student_name},{record.section},{record.date}\n"

    # Create the CSV file
    filename = "attendance.csv"  # Name of the downloaded file
    filepath = os.path.join(app.root_path, filename)  # Absolute file path
    with open(filepath, 'w', newline='') as file:
        file.write(csv_content)

    # Send the file for download
    return send_file(filepath, as_attachment=True)

  


if __name__ == '__main__':
    app.run(debug=True)
