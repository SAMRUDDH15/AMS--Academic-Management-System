

from extensions import db
from flask import Blueprint, render_template, request, redirect, url_for, session
#from main import db



# Rest of the code...



login_bp = Blueprint('login', __name__, static_folder='static')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(50))  # New column for student name
    reg_number = db.Column(db.String(50))  # New column for student registration number
    subject = db.Column(db.String(50))  # New column for lecturer subject

    def check_password(self, password):
        return self.password == password

@login_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('login.success'))
    else:
        return redirect(url_for('login.login'))

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('login.success'))

    error_message = None

    if request.method == 'POST':
        username = request.form.get('loginUser')
        password = request.form.get('loginPass')

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            session['user_id'] = user.id

            if user.role == 'student':
                session['name'] = user.name
                session['reg_number'] = user.reg_number
                return redirect(url_for('login.student_portal'))  # Redirect to student portal
            elif user.role == 'lecturer':
                session['subject'] = user.subject
                return redirect(url_for('login.lecturer_portal', subjects=user.subject))

        error_message = "Invalid username or password"

    return render_template('index1.html', error_message=error_message)

@login_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('reg_number', None)
    session.pop('subject', None)
    return redirect(url_for('login.login'))

@login_bp.route('/success')
def success():
    if 'user_id' in session:
        role = User.query.get(session['user_id']).role

        if role == 'admin':
            return redirect('https://www.google.com')
        elif role == 'student':
            return redirect(url_for('login.student_portal', name=session['name'], reg_number=session['reg_number']))
        elif role == 'lecture':
            user = User.query.get(session['user_id'])
            subjects = user.subject.split(',')
            return redirect(url_for('login.lecturer_portal', subjects=subjects))

    return redirect(url_for('login.login'))

@login_bp.route('/student_portal')
def student_portal():
    if 'user_id' in session and session['reg_number'] and session['name']:
        name = session['name']
        reg_number = session['reg_number']
        return render_template('studentportal.html', name=name, reg_number=reg_number)
    else:
        return redirect(url_for('login.login'))

@login_bp.route('/lecturer_portal/<path:subjects>')
def lecturer_portal(subjects):
    subjects = subjects.strip("[]").split(", ")
    if 'user_id' in session and session['subject'] in subjects:
        session['subject'] = 'math'
        return render_template('lecture.html', subject=session['subject'])
    elif session['subject'] == 'subject2':
        return render_template('lectu.html', subject=session['subject'])
    elif session['subject'] == 'subject3':
        return render_template('lecture_subject3.html', subject=session['subject'])
    else:
        return redirect(url_for('login.login'))

