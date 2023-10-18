from flask import Flask, render_template
from extensions import db
import secrets



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/ams'

db.init_app(app) 

app.secret_key = secrets.token_hex(16)



def create_app():
    # Import the blueprints
    from login import login_bp
    from lecture_bp import lecture_bp
    from studentportal import studentportal_bp
    from ENTEROTP import enterotp_bp
    from generateotp import generateotp_bp
    from lectureattendence import lectureattendence_bp
    from studentattendance import studentattendance_bp

    # Register blueprints
    app.register_blueprint(lecture_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(studentportal_bp)
    app.register_blueprint(enterotp_bp)
    app.register_blueprint(generateotp_bp)
    app.register_blueprint(lectureattendence_bp)
    app.register_blueprint(studentattendance_bp)

    return app


@app.route('/')
def index():
    return render_template('index1.html')


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
