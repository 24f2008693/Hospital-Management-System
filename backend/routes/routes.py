from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
from models import Patient, Doctor, Appointment, db

api_bp = Blueprint('api', __name__)

# ---------- Patients ----------
@api_bp.route('/patients/<int:pid>', methods=['PUT'])
def update_patient(pid):
	p = Patient.query.get_or_404(pid)
	data = request.get_json() or {}
	p.name = data.get('name', p.name)
	p.dob = data.get('dob', p.dob)
	p.phone = data.get('phone', p.phone)
	p.email = data.get('email', p.email)
	p.address = data.get('address', p.address)
	db.session.commit()
	return jsonify(p.to_dict())

@api_bp.route('/patients/<int:pid>', methods=['DELETE'])
def delete_patient(pid):
	p = Patient.query.get_or_404(pid)
	db.session.delete(p)
	db.session.commit()
	return jsonify({'result': True})

# ---------- Doctors ----------
@api_bp.route('/doctors', methods=['GET'])
def list_doctors():
	docs = Doctor.query.all()
	return jsonify([d.to_dict() for d in docs])

@api_bp.route('/doctors', methods=['POST'])
def create_doctor():
	data = request.get_json() or {}
	if not data.get('name'):
		return jsonify({'error': 'name is required'}), 400
	d = Doctor(
		name=data.get('name'),
		specialization=data.get('specialization'),
		phone=data.get('phone'),
		email=data.get('email')
	)
	db.session.add(d)
	db.session.commit()
	return jsonify(d.to_dict()), 201

# ---------- Appointments ----------
@api_bp.route('/appointments', methods=['GET'])
def list_appointments():
	appts = Appointment.query.order_by(Appointment.scheduled_at).all()
	return jsonify([a.to_dict() for a in appts])

@api_bp.route('/appointments', methods=['POST'])
def create_appointment():
	data = request.get_json() or {}
	try:
		scheduled_at = datetime.fromisoformat(data.get('scheduled_at'))
	except Exception:
		return jsonify({'error': 'scheduled_at must be ISO datetime string'}), 400

	if not data.get('patient_id') or not data.get('doctor_id'):
		return jsonify({'error': 'patient_id and doctor_id required'}), 400

	a = Appointment(
		patient_id=data.get('patient_id'),
		doctor_id=data.get('doctor_id'),
		scheduled_at=scheduled_at,
		status=data.get('status', 'scheduled'),
		notes=data.get('notes')
	)
	db.session.add(a)
	db.session.commit()
	return jsonify(a.to_dict()), 201