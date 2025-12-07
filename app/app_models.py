from app.app_init import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


class User(db.Model, UserMixin):
    """User model - base for admin, doctor, patient"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'admin', 'doctor', 'patient'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    doctor = db.relationship('Doctor', backref='user', uselist=False, cascade='all, delete-orphan')
    patient = db.relationship('Patient', backref='user', uselist=False, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches hashed password"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.name} ({self.role})>'


class Department(db.Model):
    """Department/Specialization model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # Relationship
    doctors = db.relationship('Doctor', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department {self.name}>'


class Doctor(db.Model):
    """Doctor model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))
    specialization = db.Column(db.String(50), nullable=False)
    license_number = db.Column(db.String(50), unique=True)
    phone = db.Column(db.String(15))
    availability = db.Column(db.String(100))  # JSON or comma-separated days
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    treatments = db.relationship('Treatment', backref='doctor', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Doctor {self.user.name} ({self.specialization})>'


class Patient(db.Model):
    """Patient model"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))  # Male, Female, Other
    phone = db.Column(db.String(15))
    address = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')
    treatments = db.relationship('Treatment', backref='patient', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Patient {self.user.name}>'


class Appointment(db.Model):
    """Appointment model"""
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.Text)  # Reason for visit
    status = db.Column(db.String(20), default='Booked')  # Booked, Completed, Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    treatment = db.relationship('Treatment', backref='appointment', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Appointment {self.patient.user.name} -> {self.doctor.user.name} on {self.date}>'


class Treatment(db.Model):
    """Treatment/Medical record model"""
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointment.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Treatment for Appointment {self.appointment_id}>'