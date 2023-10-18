

from flask import Blueprint, render_template, redirect, url_for

lecture_bp = Blueprint('lecture', __name__, url_prefix='/lecture')

@lecture_bp.route('/lect')
def lecture_index():
    return render_template('lecture.html')

@lecture_bp.route('/generate_otp', methods=['GET', 'POST'])
def generate_otp():
    # Add your OTP generation logic here
    return redirect(url_for('lecture.otp_page'))

@lecture_bp.route('/view_attendance')
def view_attendance():
    return redirect(url_for('lecture.attendance_page'))

@lecture_bp.route('/otp_page')
def otp_page():
    return render_template('generate_otp.html')

@lecture_bp.route('/attendance_page')
def attendance_page():
    return render_template('attendance.html')
