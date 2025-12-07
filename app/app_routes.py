from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import or_
from app.app_init import db
from app.app_models import User, Doctor, Patient, Appointment, Treatment, Department
from app.app_forms import (
    LoginForm, RegisterForm, AddDoctorForm, BookAppointmentForm,
    TreatmentForm, UpdateProfileForm, SearchForm
)




main = Blueprint('main', __name__)




# ==================== Authentication Routes ====================



@main.route('/')
@main.route('/home')
def home():
    """Landing page with animations"""
    if current_user.is_authenticated:
        # If already logged in, redirect to appropriate dashboard
        if current_user.role == 'admin':
            return redirect(url_for('main.admin_dashboard'))
        elif current_user.role == 'doctor':
            return redirect(url_for('main.doctor_dashboard'))
        else:
            return redirect(url_for('main.patient_dashboard'))
    
    return render_template('landing_page.html')



@main.route('/login', methods=['GET', 'POST'])
def login():
    """Login route for all users"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')
    
    return render_template('login.html', form=form)




@main.route('/register', methods=['GET', 'POST'])
def register():
    """Patient registration route"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Create new user
        user = User(name=form.name.data, email=form.email.data, role='patient')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()
        
        # Create patient profile
        patient = Patient(user_id=user.id)
        db.session.add(patient)
        db.session.commit()
        
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('main.login'))
    
    return render_template('register.html', form=form)




@main.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))




# ==================== Admin Routes ====================




@main.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    # Get statistics
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    total_appointments = Appointment.query.count()
    upcoming_appointments = Appointment.query.filter(
        Appointment.date >= datetime.now().date(),
        Appointment.status == 'Booked'
    ).count()
    
    stats = {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'upcoming_appointments': upcoming_appointments,
        'gettotaldoctors': total_doctors,
        'gettotalpatients': total_patients,
        'gettotalappointments': total_appointments,
        'getupcomingappointments': upcoming_appointments
    }
    
    return render_template('admin_dashboard.html', stats=stats)




@main.route('/admin/doctors')
@login_required
def manage_doctors():
    """List all doctors"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    doctors = Doctor.query.all()
    return render_template('admin_doctors.html', doctors=doctors)




@main.route('/admin/doctor/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    """Add new doctor"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    form = AddDoctorForm()
    if form.validate_on_submit():
        # Create user and set provided password
        user = User(name=form.name.data, email=form.email.data, role='doctor')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()


        # Create doctor profile
        doctor = Doctor(user_id=user.id, specialization=form.specialization.data)
        db.session.add(doctor)
        db.session.commit()


        flash(f'Doctor {form.name.data} added successfully!', 'success')
        return redirect(url_for('main.manage_doctors'))
    
    return render_template('admin_add_doctor.html', form=form)




@main.route('/admin/doctor/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(doctor_id):
    """Edit doctor information"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    form = AddDoctorForm()


    if form.validate_on_submit():
        # Update name and specialization
        doctor.user.name = form.name.data
        doctor.specialization = form.specialization.data


        db.session.commit()
        flash('Doctor information updated successfully!', 'success')
        return redirect(url_for('main.manage_doctors'))


    elif request.method == 'GET':
        form.name.data = doctor.user.name
        form.specialization.data = doctor.specialization
    
    return render_template('admin_edit_doctor.html', form=form, doctor=doctor)




@main.route('/admin/doctor/delete/<int:doctor_id>')
@login_required
def delete_doctor(doctor_id):
    """Delete doctor"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    user = doctor.user
    db.session.delete(doctor)
    db.session.delete(user)
    db.session.commit()
    
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('main.manage_doctors'))




@main.route('/admin/doctor/<int:doctor_id>/patients')
@login_required
def doctor_patients(doctor_id):
    """View all patients assigned to a doctor"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    doctor = Doctor.query.get_or_404(doctor_id)
    # Get all appointments for this doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).all()
    
    return render_template('admin_doctor_patients.html', doctor=doctor, appointments=appointments)




@main.route('/admin/patients')
@login_required
def manage_patients():
    """List all patients"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    # Show all patients
    patients = Patient.query.all()
    return render_template('admin_patients.html', patients=patients)




@main.route('/admin/patient/delete/<int:patient_id>')
@login_required
def delete_patient(patient_id):
    """Delete patient"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    patient = Patient.query.get_or_404(patient_id)
    user = patient.user
    db.session.delete(patient)
    db.session.delete(user)
    db.session.commit()
    
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('main.manage_patients'))




@main.route('/admin/appointments')
@login_required
def manage_appointments():
    """View all appointments"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    appointments = Appointment.query.all()
    return render_template('admin_appointments.html', appointments=appointments)




@main.route('/admin/search', methods=['GET', 'POST'])
@login_required
def admin_search():
    """Search patients or doctors"""
    if current_user.role != 'admin':
        flash('Access denied. Admin only.', 'danger')
        return redirect(url_for('main.home'))
    
    form = SearchForm()
    results = []
    
    if form.validate_on_submit():
        search_query = form.search_query.data
        search_by = form.search_by.data
        
        if search_by == 'doctor_name':
            doctors = Doctor.query.join(User).filter(
                User.name.ilike(f'%{search_query}%')
            ).all()
            results = doctors
        elif search_by == 'specialization':
            doctors = Doctor.query.filter(
                Doctor.specialization.ilike(f'%{search_query}%')
            ).all()
            results = doctors
        elif search_by == 'patient_name':
            patients = Patient.query.join(User).filter(
                User.name.ilike(f'%{search_query}%')
            ).all()
            results = patients
    
    return render_template('admin_search.html', form=form, results=results)




# ==================== Doctor Routes ====================




@main.route('/doctor/dashboard', methods=['GET', 'POST'])
@login_required
def doctor_dashboard():
    """Enhanced Doctor dashboard with all features"""
    if current_user.role != 'doctor':
        flash('Access denied. Doctor only.', 'danger')
        return redirect(url_for('main.home'))
    
    doctor = current_user.doctor
    
    # Handle patient history update
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        diagnosis = request.form.get('diagnosis')
        prescription = request.form.get('prescription')
        notes = request.form.get('notes')
        
        if not patient_id or not diagnosis or not prescription:
            flash('Please fill in all required fields.', 'danger')
        else:
            try:
                # Get the patient's latest appointment
                patient = Patient.query.get(patient_id)
                latest_appointment = Appointment.query.filter_by(
                    patient_id=patient_id,
                    doctor_id=doctor.id
                ).order_by(Appointment.date.desc(), Appointment.time.desc()).first()
                
                if not latest_appointment:
                    flash('No appointment found for this patient.', 'danger')
                else:
                    # Create or update treatment record
                    treatment = Treatment(
                        appointment_id=latest_appointment.id,
                        patient_id=patient_id,
                        doctor_id=doctor.id,
                        diagnosis=diagnosis,
                        prescription=prescription,
                        notes=notes
                    )
                    db.session.add(treatment)
                    db.session.commit()
                    flash(f'Patient history updated successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error updating patient history: {str(e)}', 'danger')
    
    today = datetime.now().date()
    
    # Get today's appointments
    today_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date == today,
        Appointment.status == 'Booked'
    ).all()
    
    # Get assigned patients
    patients = db.session.query(Patient).join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().all()
    
    # Get upcoming appointments (next 7 days)
    upcoming_date = today + timedelta(days=7)
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date >= today,
        Appointment.date <= upcoming_date,
        Appointment.status == 'Booked'
    ).order_by(Appointment.date, Appointment.time).all()
    
    return render_template('doctor_dashboard.html',
                          doctor_name=doctor.user.name,
                          today_appointments=today_appointments,
                          patients=patients,
                          upcoming_appointments=upcoming_appointments)




@main.route('/doctor/appointments')
@login_required
def doctor_appointments():
    """View all doctor's appointments"""
    if current_user.role != 'doctor':
        flash('Access denied. Doctor only.', 'danger')
        return redirect(url_for('main.home'))
    
    doctor = current_user.doctor
    appointments = Appointment.query.filter_by(doctor_id=doctor.id).all()
    
    return render_template('doctor_appointments.html', appointments=appointments)




@main.route('/doctor/appointment/<int:appointment_id>/complete', methods=['GET', 'POST'])
@login_required
def complete_appointment(appointment_id):
    """Mark appointment as completed and add treatment"""
    if current_user.role != 'doctor':
        flash('Access denied. Doctor only.', 'danger')
        return redirect(url_for('main.home'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.doctor_id != current_user.doctor.id:
        flash('You cannot access this appointment.', 'danger')
        return redirect(url_for('main.doctor_appointments'))
    
    form = TreatmentForm()
    if form.validate_on_submit():
        # Update appointment status
        appointment.status = 'Completed'
        
        # Create treatment record
        treatment = Treatment(
            appointment_id=appointment.id,
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            diagnosis=form.diagnosis.data,
            prescription=form.prescription.data,
            notes=form.notes.data
        )
        
        db.session.add(treatment)
        appointment.treatment = treatment
        db.session.commit()
        
        flash('Appointment marked as completed and treatment recorded!', 'success')
        return redirect(url_for('main.doctor_appointments'))
    
    return render_template('doctor_complete_appointment.html', 
                          form=form, appointment=appointment)




@main.route('/doctor/patients')
@login_required
def view_doctor_patients():
    """View all patients assigned to doctor"""
    if current_user.role != 'doctor':
        flash('Access denied. Doctor only.', 'danger')
        return redirect(url_for('main.home'))
    
    doctor = current_user.doctor
    
    # Get all patients who have appointments with this doctor
    patients = db.session.query(Patient).join(Appointment).filter(
        Appointment.doctor_id == doctor.id
    ).distinct().all()
    
    return render_template('doctor_patients.html', patients=patients)




@main.route('/doctor/patient/<int:patient_id>/history')
@login_required
def patient_history(patient_id):
    """View patient's medical history"""
    if current_user.role not in ['doctor', 'admin']:
        flash('Access denied.', 'danger')
        return redirect(url_for('main.home'))
    
    patient = Patient.query.get_or_404(patient_id)
    treatments = Treatment.query.filter_by(patient_id=patient.id).all()
    
    return render_template('doctor_patient_history.html', 
                          patient=patient, treatments=treatments)




# ==================== Patient Routes ====================




@main.route('/patient/dashboard')
@login_required
def patient_dashboard():
    """Patient dashboard"""
    if current_user.role != 'patient':
        flash('Access denied. Patient only.', 'danger')
        return redirect(url_for('main.home'))
    
    patient = current_user.patient
    today = datetime.now().date()
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.date >= today,
        Appointment.status == 'Booked'
    ).order_by(Appointment.date).all()
    
    # Get departments/specializations
    departments = Department.query.all()
    
    return render_template('patient_dashboard.html', 
                          appointments=upcoming_appointments,
                          departments=departments)




@main.route('/patient/search-doctors', methods=['GET', 'POST'])
@login_required
def search_doctors():
    """Search doctors by specialization or name"""
    if current_user.role != 'patient':
        flash('Access denied. Patient only.', 'danger')
        return redirect(url_for('main.home'))
    
    form = SearchForm()
    doctors = []
    
    if form.validate_on_submit():
        search_query = form.search_query.data
        search_by = form.search_by.data
        
        if search_by == 'specialization':
            doctors = Doctor.query.filter(
                Doctor.specialization.ilike(f'%{search_query}%')
            ).all()
        elif search_by == 'name':
            doctors = Doctor.query.join(User).filter(
                User.name.ilike(f'%{search_query}%')
            ).all()
    
    return render_template('patient_search_doctors.html', form=form, doctors=doctors)




@main.route('/patient/book-appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    """Book an appointment"""
    if current_user.role != 'patient':
        flash('Access denied. Patient only.', 'danger')
        return redirect(url_for('main.home'))
    
    form = BookAppointmentForm()
    form.doctor_id.choices = [(d.id, f"{d.user.name} - {d.specialization}") 
                              for d in Doctor.query.all()]
    
    if form.validate_on_submit():
        # Check for double booking
        existing = Appointment.query.filter_by(
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            time=form.time.data
        ).first()
        
        if existing:
            flash('This time slot is already booked. Please choose another.', 'warning')
            return render_template('patient_book_appointment.html', form=form)
        
        appointment = Appointment(
            patient_id=current_user.patient.id,
            doctor_id=form.doctor_id.data,
            date=form.date.data,
            time=form.time.data,
            reason=form.reason.data,
            status='Booked'
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully!', 'success')
        return redirect(url_for('main.patient_appointments'))
    
    return render_template('patient_book_appointment.html', form=form)




@main.route('/patient/appointments')
@login_required
def patient_appointments():
    """View all patient's appointments"""
    if current_user.role != 'patient':
        flash('Access denied. Patient only.', 'danger')
        return redirect(url_for('main.home'))
    
    patient = current_user.patient
    appointments = Appointment.query.filter_by(patient_id=patient.id).all()
    
    return render_template('patient_appointments.html', appointments=appointments)




@main.route('/patient/appointment/<int:appointment_id>/cancel')
@login_required
def cancel_appointment(appointment_id):
    """Cancel appointment"""
    if current_user.role != 'patient':
        flash('Access denied. Patient only.', 'danger')
        return redirect(url_for('main.home'))
    
    appointment = Appointment.query.get_or_404(appointment_id)
    
    if appointment.patient_id != current_user.patient.id:
        flash('You cannot access this appointment.', 'danger')
        return redirect(url_for('main.patient_appointments'))
    
    appointment.status = 'Cancelled'
    db.session.commit()
    
    flash('Appointment cancelled successfully!', 'success')
    return redirect(url_for('main.patient_appointments'))




@main.route('/patient/medical-history')
@login_required
def medical_history():
    """View patient's medical history"""
    if current_user.role != 'patient':
        flash('Access denied. Patient only.', 'danger')
        return redirect(url_for('main.home'))
    
    patient = current_user.patient
    treatments = Treatment.query.filter_by(patient_id=patient.id).all()
    
    return render_template('patient_medical_history.html', treatments=treatments)




@main.route('/patient/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_patient_profile():
    """Edit patient profile"""
    if current_user.role != 'patient':
        flash('Access denied. Patient only.', 'danger')
        return redirect(url_for('main.home'))
    
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.patient_dashboard'))
    
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    
    return render_template('patient_edit_profile.html', form=form)