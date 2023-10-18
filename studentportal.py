from flask import Blueprint, render_template, redirect, url_for
from flask import Flask, render_template, session, request, redirect






studentportal_bp = Blueprint('studentportal', __name__)

@studentportal_bp.route('/')
def index():
    return render_template('studentportal.html')

@studentportal_bp.route('/enter_otp')
def otp_page():
    return render_template('enterotp.html')

@studentportal_bp.route('/view_attendance')
def student_attendance():
    if 'user_id' in session and session['reg_number'] and session['name']:
        reg_number = session['reg_number']
        return render_template('student_attendance.html', reg_number=reg_number)
    else:
        return redirect(url_for('login.login'))



