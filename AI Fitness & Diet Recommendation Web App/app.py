import os
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import json
import random
import sqlite3
from flask import jsonify

from utils.fitness_data import get_weekly_diet, get_weekly_workout, get_alternative_meal

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-very-secret-key-123')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# --- Models ---
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # --- Profile fields (optional, saved by user) ---
    age        = db.Column(db.Integer,   nullable=True)
    gender     = db.Column(db.String(10),  nullable=True)
    height     = db.Column(db.Float,     nullable=True)
    weight     = db.Column(db.Float,     nullable=True)
    activity   = db.Column(db.Float,     nullable=True)
    diet_type  = db.Column(db.String(20), nullable=True)
    unit_system= db.Column(db.String(10), default='metric')
    excluded_foods = db.Column(db.String(255), nullable=True) # comma separated
    records = db.relationship('FitnessRecord', backref='owner', lazy=True)

class FitnessRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    goal = db.Column(db.String(20), nullable=False)
    plan_json = db.Column(db.Text, nullable=False) # Stores diet and workout as JSON
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# --- DB Migration: safely add profile columns to existing SQLite DB ---
def migrate_db():
    """Add new profile columns to user table if they don't already exist."""
    db_path = os.path.join(app.instance_path, 'fitness.db')
    if not os.path.exists(db_path):
        return  # Fresh DB — create_all() will handle it
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(user)")
    existing_cols = {row[1] for row in cursor.fetchall()}
    new_columns = [
        ('age',       'INTEGER'),
        ('gender',    'VARCHAR(10)'),
        ('height',    'FLOAT'),
        ('weight',    'FLOAT'),
        ('activity',  'FLOAT'),
        ('diet_type', 'VARCHAR(20)'),
        ('unit_system', 'VARCHAR(10)'),
        ('excluded_foods', 'VARCHAR(255)'),
    ]
    for col_name, col_type in new_columns:
        if col_name not in existing_cols:
            cursor.execute(f'ALTER TABLE user ADD COLUMN {col_name} {col_type}')
    conn.commit()
    conn.close()

# --- Calculation Logic ---
def calculate_bmi(weight, height):
    height_m = height / 100
    return round(weight / (height_m ** 2), 1)

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    else:
        return 10 * weight + 6.25 * height - 5 * age - 161

# --- Routes ---

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            gender = request.form['gender']
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            goal = request.form['goal']
            activity = float(request.form['activity'])
            diet_type = request.form['diet_type']
            unit_system = request.form.get('unit_system', 'metric')
            
            # Convert imperial to metric for calculation
            calc_weight = weight * 0.453592 if unit_system == 'imperial' else weight
            calc_height = height * 2.54 if unit_system == 'imperial' else height

            bmi = calculate_bmi(calc_weight, calc_height)
            bmr = calculate_bmr(calc_weight, calc_height, age, gender)
            tdee = bmr * activity

            if goal.lower() == 'fat loss':
                calories = tdee - 500
            elif goal.lower() == 'muscle gain':
                calories = tdee + 300
            else:
                calories = tdee

            excluded_foods = current_user.excluded_foods if current_user.is_authenticated else ''
            
            results = {
                'bmi': bmi,
                'calories': round(calories),
                'protein': round((calories * 0.3) / 4),
                'carbs': round((calories * 0.45) / 4),
                'fats': round((calories * 0.25) / 9),
                'weekly_diet': get_weekly_diet(goal, diet_type, excluded_foods, calories),
                'weekly_workout': get_weekly_workout(goal),
                'goal': goal.capitalize(),
                'weight': weight,
                'height': height,
                'diet_type': diet_type
            }

            return render_template('result.html', results=results)
        except Exception as e:
            flash(f"Error in calculation: {str(e)}", "danger")
            return redirect(url_for('index'))

    # Pass saved profile to pre-fill the form
    profile = current_user if current_user.is_authenticated else None
    return render_template('index.html', profile=profile)

@app.route('/swap_meal', methods=['POST'])
def swap_meal():
    data = request.json
    goal = data.get('goal', 'fat loss')
    diet_type = data.get('diet_type', 'veg')
    meal_type = data.get('meal_type', 'breakfast')
    target_calories = data.get('target_calories', 2000)
    excluded_foods = current_user.excluded_foods if current_user.is_authenticated else ''
    
    new_meal = get_alternative_meal(goal, diet_type, meal_type, excluded_foods, target_calories)
    return jsonify(new_meal)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered. Please login.', 'danger')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('Username already taken. Try another.', 'danger')
            return redirect(url_for('register'))
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Check email and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/save_record', methods=['POST'])
@login_required
def save_record():
    data = request.form
    record = FitnessRecord(
        weight=float(data['weight']),
        height=float(data['height']),
        bmi=float(data['bmi']),
        calories=int(data['calories']),
        goal=data['goal'],
        plan_json=data['plan_json'], # Now sent as a pre-stringified JSON
        owner=current_user
    )
    db.session.add(record)
    db.session.commit()
    flash('Weekly Plan saved to your profile!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    records = FitnessRecord.query.filter_by(owner=current_user).order_by(FitnessRecord.date.asc()).all()
    labels = [r.date.strftime('%Y-%m-%d') for r in records]
    weights = [r.weight for r in records]
    bmis = [r.bmi for r in records]

    # Latest plan for the plan viewer
    latest_plan = None
    latest_record = None
    if records:
        latest_record = records[-1]
        try:
            latest_plan = json.loads(latest_record.plan_json)
        except Exception:
            latest_plan = None

    # Today's day key: Mon=Day1 ... Sun=Day7
    today_day = f"Day {datetime.utcnow().weekday() + 1}"

    return render_template('dashboard.html',
                           records=records[::-1],
                           labels=json.dumps(labels),
                           weights=json.dumps(weights),
                           bmis=json.dumps(bmis),
                           latest_plan=latest_plan,
                           latest_record=latest_record,
                           today_day=today_day)

@app.route('/download_pdf', methods=['POST'])
def download_pdf():
    from utils.pdf_generator import generate_pdf
    results = json.loads(request.form['results_json'])
    pdf_path = generate_pdf(results)
    return send_file(pdf_path, as_attachment=True)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            current_user.age       = int(request.form['age'])      if request.form.get('age')      else None
            current_user.gender    = request.form.get('gender')    or None
            current_user.height    = float(request.form['height']) if request.form.get('height')  else None
            current_user.weight    = float(request.form['weight']) if request.form.get('weight')  else None
            current_user.activity  = float(request.form['activity']) if request.form.get('activity') else None
            current_user.diet_type = request.form.get('diet_type') or None
            current_user.unit_system = request.form.get('unit_system') or 'metric'
            current_user.excluded_foods = request.form.get('excluded_foods') or ''
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash(f'Error saving profile: {str(e)}', 'danger')
        return redirect(url_for('profile'))
    return render_template('profile.html')

@app.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    user = current_user
    FitnessRecord.query.filter_by(owner=user).delete()
    db.session.delete(user)
    db.session.commit()
    logout_user()
    flash('Your account has been permanently deleted.', 'success')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        migrate_db()   # Add new columns to existing DB if needed
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
