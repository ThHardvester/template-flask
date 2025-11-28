from flask import Blueprint, request, jsonify, render_template
from flask_login import login_user, login_required, logout_user, current_user
from extensions import db
from models import User

main_bp = Blueprint('main', __name__)

# Vistas (HTML)
@main_bp.route('/')
def login_page():
    if current_user.is_authenticated:
         return render_template('dashboard.html')
    return render_template('login.html')

@main_bp.route('/register')
def register_page():
    if current_user.is_authenticated:
         return render_template('dashboard.html')
    return render_template('register.html')

@main_bp.route('/dashboard')
@login_required
def dashboard_page():
    return render_template('dashboard.html')

# API Endpoints
@main_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No se enviaron datos'}), 400

    required_fields = ['email', 'password', 'first_name', 'last_name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Falta el campo {field}'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({'error': 'El email ya está registrado + '}+data), 400

    new_user = User(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        phone=data.get('phone', ''),
        address=data.get('address', '')
    )
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente'}), 201

@main_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Faltan credenciales'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Login exitoso', 'user': user.to_dict()}), 200
    
    return jsonify({'error': 'Email o contraseña inválidos'}), 401

@main_bp.route('/api/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout exitoso'})

@main_bp.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard_data():
    return jsonify({
        'message': 'Bienvenido a tu dashboard',
        'profile': current_user.to_dict()
    })
