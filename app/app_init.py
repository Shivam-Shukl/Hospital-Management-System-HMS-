from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')

    # Ensure instance folder exists and store DB inside it to avoid confusion
    os.makedirs(app.instance_path, exist_ok=True)
    db_path = os.path.join(app.instance_path, 'hospital.db').replace('\\', '/')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Register blueprints
    from app.app_routes import main
    app.register_blueprint(main)
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.app_models import User
        return User.query.get(int(user_id))
    
    # Create tables and seed data
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        from app.app_models import User, Department
        
        if not User.query.filter_by(role='admin').first():
            admin = User(name='Admin', email='admin@hospital.com', role='admin')
            admin.set_password('admin@123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin user created: admin@hospital.com / admin@123")
        
        # Create default departments if not exists
        if Department.query.count() == 0:
            departments = [
                Department(name='Cardiology', description='Heart and cardiovascular diseases'),
                Department(name='Neurology', description='Nervous system disorders'),
                Department(name='Orthopedics', description='Bones and joints'),
                Department(name='Pediatrics', description='Child healthcare'),
                Department(name='Dermatology', description='Skin disorders'),
                Department(name='General Medicine', description='General medical care'),
                Department(name='Psychiatry', description='Mental health'),
            ]
            db.session.add_all(departments)
            db.session.commit()
            print("✓ Default departments created")
    
    return app