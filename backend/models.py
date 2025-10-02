from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

db = SQLAlchemy()
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash



class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, nullable=False)
	password_hash = db.Column(db.String(128), nullable=False)
	role = db.Column(db.String(32), default='user')

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def to_dict(self):
		return {'id': self.id, 'username': self.username, 'role': self.role}

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
	name = db.Column(db.String(120), nullable=False)
