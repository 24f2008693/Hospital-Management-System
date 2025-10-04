from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from extensions import db, login_manager


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password_hash = db.Column(db.String(200), nullable=False)
	role = db.Column(db.String(20), nullable=False, default='patient')
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Patient(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	dob = db.Column(db.String(20))
	phone = db.Column(db.String(20))
	email = db.Column(db.String(120))
	address = db.Column(db.String(255))
	created_at = db.Column(db.DateTime, default=datetime.utcnow)

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'dob': self.dob,
			'phone': self.phone,
			'email': self.email,
			'address': self.address,
			'created_at': self.created_at.isoformat() if self.created_at else None
		}


class Doctor(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), nullable=False)
	specialization = db.Column(db.String(120))
	phone = db.Column(db.String(20))
	email = db.Column(db.String(120))

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
			'specialization': self.specialization,
			'phone': self.phone,
			'email': self.email
		}


class Appointment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
	doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
	scheduled_at = db.Column(db.DateTime, nullable=False)
	status = db.Column(db.String(32), default='scheduled')
	notes = db.Column(db.Text)

	patient = db.relationship('Patient', backref=db.backref('appointments', lazy=True))
	doctor = db.relationship('Doctor', backref=db.backref('appointments', lazy=True))

	def to_dict(self):
		return {
			'id': self.id,
			'patient_id': self.patient_id,
			'doctor_id': self.doctor_id,
			'scheduled_at': self.scheduled_at.isoformat() if self.scheduled_at else None,
			'status': self.status,
			'notes': self.notes
		}


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
