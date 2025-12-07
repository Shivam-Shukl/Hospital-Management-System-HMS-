# 🏥 Hospital Management System (HMS)

A comprehensive, production-ready web application for managing hospital operations, patient care, appointments, and medical records with role-based access control.

**Live Demo:** [https://hms-etvm.onrender.com/](https://hms-etvm.onrender.com/)

---

## ✨ Features

### 👨‍⚕️ Admin Panel
- 📊 Dashboard with real-time statistics
- 👥 Complete doctor management (Add, Edit, Delete)
- 👤 Patient management and oversight
- 📅 View all appointments across the hospital
- 🔍 Advanced search functionality

### 👨‍⚕️ Doctor Portal
- 📋 Personal dashboard with today's appointments
- 👥 Assigned patients list
- 📅 Appointment management
- 📝 Record treatment and medical notes
- 📊 Access patient medical history

### 👨‍💼 Patient Portal
- 🔍 Search doctors by specialization
- 📅 Book appointments with available doctors
- 📋 View appointment history
- 📝 Access personal medical records
- ⚙️ Edit personal profile

### 🔐 Security & Access Control
- Secure password hashing (Werkzeug)
- CSRF protection on all forms
- Role-based access control (Admin, Doctor, Patient)
- Session-based authentication (Flask-Login)
- SQL injection prevention (SQLAlchemy ORM)

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 2.3.0
- **Database:** SQLite (Dev) / PostgreSQL (Production)
- **ORM:** SQLAlchemy 3.0.5
- **Authentication:** Flask-Login 0.6.2
- **Forms:** WTForms 3.0.1 with Flask-WTF
- **Server:** Gunicorn 20.1.0

### Frontend
- **HTML5 & Jinja2** Templates
- **CSS:** Bootstrap 5.3.0
- **Icons:** Font Awesome 6.4.0
- **Responsive Design** with Mobile-first approach

### Deployment
- **Platform:** Render
- **Database:** PostgreSQL on Render
- **Environment:** Python 3.x

---

## 📁 Project Structure

```
hospital-management-system/
├── app/
│   ├── app_init.py              # Flask initialization & config
│   ├── app_models.py            # Database models (6 models)
│   ├── app_forms.py             # Form validation (7 forms)
│   ├── app_routes.py            # All routes (50+ endpoints)
│   ├── templates/               # HTML templates (17 files)
│   │   ├── base.html
│   │   ├── landing_page.html
│   │   ├── admin/               # Admin templates
│   │   ├── doctor/              # Doctor templates
│   │   └── patient/             # Patient templates
│   └── static/
│       ├── css/style.css
│       ├── js/script.js
│       └── images/
├── app.py                       # Main entry point
├── requirements.txt             # Python dependencies
├── Procfile                     # Render deployment config
├── .env.example                 # Environment variables template
├── .gitignore
└── README.md                    # This file
```

---

## 🗄️ Database Models

### User (Base Authentication)
- Email, Password (hashed), Name, Role (admin/doctor/patient)

### Doctor
- User reference, Specialization, Appointments list

### Patient
- User reference, Medical history, Appointments & Treatments

### Appointment
- Patient, Doctor, Date, Time, Reason, Status (Booked/Completed/Cancelled)

### Treatment
- Appointment, Diagnosis, Prescription, Medical notes

### Department
- Department names and descriptions

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
```

5. **Edit .env with your settings**
```env
SECRET_KEY=your-very-secure-random-key-here
FLASK_ENV=development
DATABASE_URL=sqlite:///hms.db
```

6. **Run the application**
```bash
python app.py
```

7. **Access the application**
```
http://localhost:5000
```

---

## 📝 Test Credentials

### Admin Account
- **Email:** admin@hms.com
- **Password:** admin123
- **Role:** Administrator

### Doctor Account
- **Email:** doctor@hms.com
- **Password:** doctor123
- **Specialization:** Cardiology

### Patient Account
- **Email:** patient@hms.com
- **Password:** patient123

---

## 🔄 User Workflows

### Patient Booking Appointment
1. Register or Login
2. Go to Search Doctors
3. Filter by specialization
4. Click "Book Appointment"
5. Select date and time
6. Submit booking
7. View in "My Appointments"

### Doctor Recording Treatment
1. Login as Doctor
2. View appointments in dashboard
3. Click appointment to complete
4. Fill diagnosis, prescription, notes
5. Submit treatment
6. Status updates to "Completed"

### Admin Managing System
1. Login as Admin
2. View dashboard statistics
3. Add new doctors (Admin Panel)
4. Delete patients if needed
5. Search for specific users
6. Monitor all appointments

---

## 📊 Key Routes

### Authentication
```
GET/POST  /              → Landing page
GET/POST  /login         → Login
GET/POST  /register      → Patient registration
GET       /logout        → Logout
```

### Admin Dashboard
```
GET       /admin/dashboard       → Statistics
GET       /admin/doctors         → Doctor list
GET/POST  /admin/doctor/add      → Add doctor
GET       /admin/patients        → Patient list
GET       /admin/appointments    → All appointments
GET/POST  /admin/search          → Search
```

### Doctor Dashboard
```
GET       /doctor/dashboard                → Overview
GET       /doctor/appointments             → My appointments
GET/POST  /doctor/appointment/<id>/complete→ Complete appointment
GET       /doctor/patients                 → My patients
GET       /doctor/patient/<id>/history     → Patient history
```

### Patient Dashboard
```
GET       /patient/dashboard           → Overview
GET/POST  /patient/search-doctors      → Search doctors
GET/POST  /patient/book-appointment    → Book appointment
GET       /patient/appointments        → My appointments
GET       /patient/medical-history     → Medical records
GET/POST  /patient/profile/edit        → Edit profile
```

---

## 🌐 Deployment on Render

### Step-by-Step Deployment Guide

1. **Push to GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

2. **Create Render Account**
   - Visit [render.com](https://render.com)
   - Sign up with GitHub

3. **Create PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Choose free tier
   - Copy connection string

4. **Create Web Service**
   - Click "New +" → "Web Service"
   - Select your GitHub repository
   - Configure:
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `gunicorn app:app`

5. **Add Environment Variables**
   - SECRET_KEY: Generate using `python -c "import secrets; print(secrets.token_hex(32))"`
   - DATABASE_URL: Paste PostgreSQL connection string
   - FLASK_ENV: `production`

6. **Deploy**
   - Click "Deploy"
   - Monitor logs for errors
   - Access your live app!

---

## 🔐 Security Features

✅ **Password Security:** Werkzeug hashing with salt  
✅ **CSRF Protection:** Flask-WTF tokens on all forms  
✅ **Session Management:** Secure Flask-Login sessions  
✅ **Role-Based Access:** Route decorators for authorization  
✅ **SQL Injection Prevention:** SQLAlchemy parameterized queries  
✅ **Input Validation:** WTForms validators  
✅ **HTTPS Ready:** For production deployment  

---

## 🎨 UI/UX Features

- 📱 **Fully Responsive:** Mobile, tablet, desktop
- 🎯 **Intuitive Navigation:** Role-based menu
- ✨ **Modern Design:** Bootstrap 5 + custom CSS
- 🚀 **Smooth Animations:** Page transitions
- 🌙 **Dark Mode Support:** Eye-friendly interface
- ♿ **Accessible:** WCAG compliant

---

## 📦 Dependencies

```
Flask==2.3.0                    # Web framework
Flask-SQLAlchemy==3.0.5        # ORM
Flask-Login==0.6.2             # Authentication
Flask-WTF==1.1.1               # CSRF protection
WTForms==3.0.1                 # Form handling
python-dotenv==1.0.0           # Environment variables
gunicorn==20.1.0               # Production server
psycopg2-binary==2.9.6         # PostgreSQL driver
```

See `requirements.txt` for complete list.

---

## 🐛 Troubleshooting

### Login Issues
- Check email/password in database
- Verify SECRET_KEY is set
- Clear browser cookies

### Database Errors
- Verify DATABASE_URL format
- Check PostgreSQL is running
- Run migrations if needed

### 404 Routes
- Check route definitions in `app_routes.py`
- Verify templates exist in correct folders
- Restart Flask server

### Static Files Not Loading
- Check `static/` folder structure
- Verify CSS/JS file paths
- Clear browser cache

---

## 👥 Role Permissions Matrix

| Feature | Admin | Doctor | Patient |
|---------|-------|--------|---------|
| View Dashboard | ✅ | ✅ | ✅ |
| Manage Doctors | ✅ | ❌ | ❌ |
| Manage Patients | ✅ | ❌ | ❌ |
| Book Appointment | ❌ | ❌ | ✅ |
| Complete Appointment | ❌ | ✅ | ❌ |
| View All Appointments | ✅ | ❌ | ❌ |
| View Medical Records | ✅ | ✅ | ✅ |
| Record Treatment | ❌ | ✅ | ❌ |
| Search Users | ✅ | ❌ | ❌ |

---

## 📈 Project Statistics

- **Total Python Files:** 5 core files
- **HTML Templates:** 17 files
- **API Routes:** 50+ endpoints
- **Database Models:** 6 models
- **Form Classes:** 7 forms
- **Security Layers:** 6 implementations
- **Lines of Code:** 3000+

---

## 🔄 Git Workflow

```bash
# Clone repository
git clone https://github.com/yourusername/hospital-management-system.git

# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "Add feature description"

# Push to GitHub
git push origin feature/your-feature-name

# Create Pull Request on GitHub
```

---


## 🚧 Future Enhancements

- [ ] Email notifications for appointments
- [ ] SMS reminders
- [ ] Prescription delivery integration
- [ ] Video consultation support
- [ ] Advanced analytics & reporting
- [ ] Mobile app (React Native)
- [ ] AI-powered appointment suggestions
- [ ] Payment gateway integration
- [ ] Multi-language support
- [ ] Two-factor authentication

---


## 👨‍💻 Authors

- **Developer:** Shivam Shukla
- **Idea:** Shivansh Shukla

---

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Bootstrap for responsive design framework
- Font Awesome for beautiful icons
- Render for hosting platform

---


## 🌟 Star This Project

If you find this project useful, please give it a ⭐ on GitHub!

---

**Made with ❤️ for better hospital management**
