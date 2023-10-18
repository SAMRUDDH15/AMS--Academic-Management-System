from extensions import db
from flask import jsonify, Flask, request
from flask import Blueprint
from datetime import datetime

generateotp_bp = Blueprint('generateotp', __name__)


class otptable(db.Model):
    __table_args__ = {'extend_existing': True}  # Add this line

    id = db.Column(db.Integer, primary_key=True)
    otp = db.Column(db.String(6), nullable=False)
    subject = db.Column(db.String(50), nullable=True)
    section = db.Column(db.String(10), nullable=False)
    generated_time = db.Column(db.DateTime, nullable=False, default=datetime.now())



# Define the generate_otp route
@generateotp_bp.route('/store-otp', methods=['POST'])
def store_otp():
    data = request.json
    otp = data.get('otp')
    subject = data.get('subject')
    section = data.get('section')

    # Perform necessary operations to store the OTP and values
    # For example, you can store them in a database

    new_otp = otptable(otp=otp, subject=subject, section=section)
    db.session.add(new_otp)
    db.session.commit()

    print(f"OTP: {otp}")
    print(f"Subject: {subject}")
    print(f"Section: {section}")

    return jsonify({'message': 'OTP stored successfully.'}), 200


if __name__ == '__main__':
    app.run(debug=True)
