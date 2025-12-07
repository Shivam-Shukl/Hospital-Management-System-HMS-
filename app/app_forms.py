from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.app_models import User


class LoginForm(FlaskForm):
    """Form for user login"""
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email format")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required")
    ])


class RegisterForm(FlaskForm):
    """Form for patient registration"""
    name = StringField('Full Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=3, message="Name must be at least 3 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email format")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=6, message="Password must be at least 6 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Confirm password is required"),
        EqualTo('password', message="Passwords must match")
    ])

    def validate_email(self, field):
        """Check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered. Please login instead.")


class AddDoctorForm(FlaskForm):
    """Form for admin to add a new doctor"""
    name = StringField('Doctor Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=3, message="Name must be at least 3 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email format")
    ])
    specialization = SelectField('Specialization', validators=[
        DataRequired(message="Specialization is required")
    ], choices=[
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedics', 'Orthopedics'),
        ('pediatrics', 'Pediatrics'),
        ('dermatology', 'Dermatology'),
        ('general', 'General Medicine'),
        ('psychiatry', 'Psychiatry'),
    ])
    password = PasswordField('Password', validators=[
        DataRequired(message="Password is required"),
        Length(min=6, message="Password must be at least 6 characters")
    ])

    def validate_email(self, field):
        """Check if email already exists"""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


class EditDoctorForm(AddDoctorForm):
    """Form for editing doctor - password optional."""
    # override validators to make password optional during edit
    password = PasswordField('Password', validators=[
        Length(min=0, message="Password must be at least 6 characters")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('password', message="Passwords must match")
    ])

    def validate_email(self, field):
        # allow same email for the current user; detailed check should happen in route
        existing = User.query.filter_by(email=field.data).first()
        # do not raise here; route will handle conflicts if needed
        return


class BookAppointmentForm(FlaskForm):
    """Form for patient to book an appointment"""
    doctor_id = SelectField('Select Doctor', validators=[
        DataRequired(message="Please select a doctor")
    ], coerce=int)
    date = DateField('Appointment Date', validators=[
        DataRequired(message="Date is required")
    ], format='%Y-%m-%d')
    time = TimeField('Appointment Time', validators=[
        DataRequired(message="Time is required")
    ], format='%H:%M')
    reason = TextAreaField('Reason for Visit', validators=[
        DataRequired(message="Please provide a reason"),
        Length(min=10, message="Reason must be at least 10 characters")
    ])


class TreatmentForm(FlaskForm):
    """Form for doctor to record treatment/diagnosis"""
    diagnosis = TextAreaField('Diagnosis', validators=[
        DataRequired(message="Diagnosis is required"),
        Length(min=10, message="Diagnosis must be at least 10 characters")
    ])
    prescription = TextAreaField('Prescription', validators=[
        DataRequired(message="Prescription is required"),
        Length(min=5, message="Prescription must be at least 5 characters")
    ])
    notes = TextAreaField('Additional Notes', validators=[
        Length(min=0, max=500, message="Notes must be less than 500 characters")
    ])


class UpdateProfileForm(FlaskForm):
    """Form for users to update their profile"""
    name = StringField('Full Name', validators=[
        DataRequired(message="Name is required"),
        Length(min=3, message="Name must be at least 3 characters")
    ])
    email = StringField('Email', validators=[
        DataRequired(message="Email is required"),
        Email(message="Invalid email format")
    ])

    def validate_email(self, field):
        """Check if email is already used by another user"""
        from flask_login import current_user
        if User.query.filter(User.email == field.data, User.id != current_user.id).first():
            raise ValidationError("Email already in use by another account.")


class SearchForm(FlaskForm):
    """Form for searching doctors or patients"""
    search_query = StringField('Search', validators=[
        DataRequired(message="Search query is required")
    ])
    search_by = SelectField('Search By', validators=[
        DataRequired(message="Please select a search category")
    ], choices=[
        ('name', 'Name'),
        ('specialization', 'Specialization'),
        ('email', 'Email')
    ])