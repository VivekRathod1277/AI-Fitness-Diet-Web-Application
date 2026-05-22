import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
import json
import random
import sqlite3

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

def get_weekly_diet(goal, diet_type):
    options = {
        'fat loss': {
            'veg': {
                'breakfast': ['Oats with berries', 'Moong Dal Chilla', 'Smoothie Bowl', 'Besan Poha', 'Greek Yogurt with Nuts'],
                'lunch': ['Quinoa Salad', 'Paneer & Veggie Wrap', 'Lentil Soup with Brown Rice', 'Soya Chunks Stir-fry', 'Mixed Bean Salad'],
                'dinner': ['Roasted Vegetables', 'Paneer Tikka with Salad', 'Dal Khichdi (Light)', 'Vegetable Clear Soup', 'Mushroom Sauté']
            },
            'eggitarian': {
                'breakfast': ['Boiled Eggs & Toast', 'Egg White Omelet', 'Scrambled Eggs with Spinach', 'Protein Pancakes', 'Poached Eggs on Rye'],
                'lunch': ['Grilled Chicken Salad', 'Egg Curry (Light)', 'Tuna/Egg Wrap', 'Baked Fish with Greens', 'Turkey Breast Sandwich'],
                'dinner': ['Chicken Stir-fry', 'Omelet with Veggies', 'Grilled Chicken & Broccoli', 'Egg Bhurji (No Butter)', 'Salmon with Asparagus']
            }
        },
        'muscle gain': {
            'veg': {
                'breakfast': ['Paneer Paratha', 'Protein Smoothie with Oats', 'Peanut Butter Toast & Milk', 'Sprouted Salad & Paneer', 'Tofu Scramble'],
                'lunch': ['Dal Makhani & Brown Rice', 'Paneer Butter Masala (Mod) & Roti', 'Soya Chunk Pulao', 'Chickpea Curry & Quinoa', 'Rajma Chawal'],
                'dinner': ['Paneer Bhurji & Roti', 'Lentil Pasta', 'Tofu & Veggie Stir-fry', 'Stuffed Mushrooms & Paneer', 'Vegetable Stew & Bread']
            },
            'eggitarian': {
                'breakfast': ['Whole Eggs Omelet (3-4 eggs)', 'Chicken Sausage & Eggs', 'French Toast with Honey', 'Egg & Cheese Sandwich', 'Protein Oats with Egg Whites'],
                'lunch': ['Chicken Breast & Rice', 'Egg Fried Rice (High Protein)', 'Beef/Chicken Burrito', 'Grilled Fish & Sweet Potato', 'Lamb Chops & Veggies'],
                'dinner': ['Steak & Mashed Potatoes', 'Chicken Pasta', 'Grilled Salmon & Rice', 'Scrambled Eggs & Avocado Toast', 'Turkey Burger (No Bun)']
            }
        }
    }

    # Default to maintenance if not found
    pool = options.get(goal.lower(), options['fat loss']).get(diet_type.lower(), options['fat loss']['veg'])
    
    weekly_plan = {}
    for i in range(1, 8):
        weekly_plan[f"Day {i}"] = {
            'breakfast': random.choice(pool['breakfast']),
            'lunch': random.choice(pool['lunch']),
            'dinner': random.choice(pool['dinner'])
        }
    return weekly_plan

def _ex(name, sets, reps, rest, notes=''):
    return {'name': name, 'sets': sets, 'reps': reps, 'rest': rest, 'notes': notes}

def get_weekly_workout(goal):
    if goal.lower() == 'fat loss':
        plans = {
            'Day 1': {
                'type': 'HIIT Cardio', 'focus': 'Full Body Fat Burn', 'duration': '40 min', 'color': '#f43f5e',
                'exercises': [
                    _ex('Burpees', 4, '15 reps', '30s', 'Explosive jump at top, land softly'),
                    _ex('Mountain Climbers', 4, '20 each leg', '30s', 'Keep hips level, fast pace'),
                    _ex('Jumping Jacks', 3, '40 reps', '20s', 'Full arm extension overhead'),
                    _ex('High Knees', 4, '30s', '30s', 'Drive knees above waist height'),
                    _ex('Jump Rope', 3, '60s', '30s', 'Stay light on your toes'),
                ]
            },
            'Day 2': {
                'type': 'Upper Body Strength', 'focus': 'Chest, Shoulders, Triceps', 'duration': '45 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Push-ups', 4, '15 reps', '45s', 'Full ROM, chest touches floor'),
                    _ex('Pike Push-ups', 3, '12 reps', '45s', 'Targets shoulders, hips high'),
                    _ex('Tricep Dips (Chair)', 3, '12 reps', '45s', 'Elbows close to body'),
                    _ex('Diamond Push-ups', 3, '10 reps', '45s', 'Hands form a diamond shape'),
                    _ex('Plank Hold', 3, '60s', '30s', 'Straight line head to heel'),
                ]
            },
            'Day 3': {
                'type': 'Active Recovery', 'focus': 'Mobility and Flexibility', 'duration': '30 min', 'color': '#22c55e',
                'exercises': [
                    _ex('Brisk Walk', 1, '20 min', '-', 'Maintain conversational pace'),
                    _ex('Hip Flexor Stretch', 2, '60s each side', '-', 'Lunge position, push hips forward'),
                    _ex('Cat-Cow Stretch', 2, '10 reps', '-', 'Slow and controlled breathing'),
                    _ex('Pigeon Pose', 2, '60s each side', '-', 'Hold and breathe deeply'),
                    _ex("Child's Pose", 2, '60s', '-', 'Relax entire back'),
                ]
            },
            'Day 4': {
                'type': 'HIIT Cardio', 'focus': 'Speed and Agility', 'duration': '40 min', 'color': '#f43f5e',
                'exercises': [
                    _ex('Sprint Intervals', 6, '30s on / 30s off', '-', 'Max effort on, walk during off'),
                    _ex('Box Jumps', 4, '12 reps', '45s', 'Land with soft knees, step down'),
                    _ex('Lateral Shuffles', 4, '30s', '30s', 'Stay low, quick feet'),
                    _ex('Jump Squats', 4, '15 reps', '45s', 'Explode upward, land quietly'),
                    _ex('Plank to Downdog', 3, '10 reps', '30s', 'Controlled transition'),
                ]
            },
            'Day 5': {
                'type': 'Lower Body Strength', 'focus': 'Glutes, Quads, Hamstrings', 'duration': '45 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Bodyweight Squats', 4, '20 reps', '45s', 'Knees track over toes, depth below parallel'),
                    _ex('Reverse Lunges', 3, '12 each leg', '45s', 'Back knee hovers above floor'),
                    _ex('Glute Bridges', 4, '20 reps', '30s', 'Squeeze glutes at top, hold 1s'),
                    _ex('Wall Sit', 3, '60s', '45s', 'Thighs parallel to floor'),
                    _ex('Calf Raises', 3, '20 reps', '30s', 'Full extension at top, pause'),
                ]
            },
            'Day 6': {
                'type': 'Full Body Circuit', 'focus': 'Endurance and Strength', 'duration': '50 min', 'color': '#f97316',
                'exercises': [
                    _ex('Burpee + Push-up', 4, '10 reps', '45s', 'Add push-up at the bottom of each burpee'),
                    _ex('Squat + Overhead Press', 3, '12 reps', '45s', 'Use dumbbells or water bottles'),
                    _ex('Renegade Row', 3, '10 each side', '45s', 'Keep hips square to floor'),
                    _ex('Jumping Lunges', 3, '10 each leg', '45s', 'Explosive switch, land softly'),
                    _ex('Plank + Shoulder Tap', 3, '10 each side', '30s', 'Minimal hip rotation'),
                ]
            },
            'Day 7': {
                'type': 'Rest Day', 'focus': 'Recovery', 'duration': '-', 'color': '#94a3b8',
                'exercises': [
                    _ex('Complete Rest', 1, '-', '-', 'Let your muscles repair and grow'),
                    _ex('Optional Light Walk', 1, '20-30 min', '-', 'Fresh air, low intensity only'),
                    _ex('Foam Rolling', 1, '10-15 min', '-', 'Focus on sore muscle groups'),
                ]
            },
        }
    elif goal.lower() == 'muscle gain':
        plans = {
            'Day 1': {
                'type': 'Chest and Triceps', 'focus': 'Upper Body Push', 'duration': '60 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Bench Press', 4, '8-10 reps', '90s', 'Full ROM, controlled descent, drive through chest'),
                    _ex('Incline Dumbbell Press', 3, '10-12 reps', '75s', 'Elbows at 45 degrees, squeeze at top'),
                    _ex('Cable Chest Fly', 3, '12-15 reps', '60s', 'Slight bend in elbows, feel the stretch'),
                    _ex('Tricep Rope Pushdown', 3, '12-15 reps', '45s', 'Flare hands at bottom of movement'),
                    _ex('Overhead Tricep Extension', 3, '12 reps', '45s', 'Keep elbows pointing forward'),
                ]
            },
            'Day 2': {
                'type': 'Back and Biceps', 'focus': 'Upper Body Pull', 'duration': '60 min', 'color': '#06b6d4',
                'exercises': [
                    _ex('Deadlift', 4, '6-8 reps', '120s', 'Neutral spine, drive through heels'),
                    _ex('Pull-ups / Lat Pulldown', 3, '8-10 reps', '90s', 'Full extension at bottom'),
                    _ex('Seated Cable Row', 3, '10-12 reps', '75s', 'Pull elbows back, squeeze scapula'),
                    _ex('Dumbbell Bicep Curl', 3, '12 reps', '60s', 'Supinate at top, no swinging'),
                    _ex('Hammer Curl', 3, '12 reps', '45s', 'Targets brachialis and forearms'),
                ]
            },
            'Day 3': {
                'type': 'Rest / Active Recovery', 'focus': 'Mobility', 'duration': '20-30 min', 'color': '#22c55e',
                'exercises': [
                    _ex('Light Walk or Cycle', 1, '20 min', '-', 'Keep heart rate low, recover actively'),
                    _ex('Thoracic Spine Stretch', 2, '60s', '-', 'Use foam roller on upper back'),
                    _ex('Lat Stretch', 2, '60s each side', '-', 'Doorframe or band stretch'),
                    _ex('Wrist and Forearm Stretch', 2, '60s', '-', 'Important after heavy pulling days'),
                ]
            },
            'Day 4': {
                'type': 'Legs', 'focus': 'Quads, Hamstrings, Glutes, Calves', 'duration': '65 min', 'color': '#f97316',
                'exercises': [
                    _ex('Barbell Squat', 4, '8-10 reps', '120s', 'Depth below parallel, chest up, brace core'),
                    _ex('Romanian Deadlift', 3, '10-12 reps', '90s', 'Hinge at hips, feel hamstring stretch'),
                    _ex('Leg Press', 3, '12-15 reps', '75s', 'Feet shoulder-width, full ROM'),
                    _ex('Leg Curl', 3, '12-15 reps', '60s', 'Slow eccentric, squeeze at top'),
                    _ex('Standing Calf Raise', 4, '15-20 reps', '45s', 'Full extension, hold 1s at top'),
                ]
            },
            'Day 5': {
                'type': 'Shoulders and Abs', 'focus': 'Deltoids and Core', 'duration': '55 min', 'color': '#a855f7',
                'exercises': [
                    _ex('Overhead Press (BB/DB)', 4, '8-10 reps', '90s', 'Full lockout overhead, no lower-back arch'),
                    _ex('Lateral Raise', 3, '12-15 reps', '60s', 'Lead with elbows, slight forward lean'),
                    _ex('Face Pull', 3, '15 reps', '45s', 'Targets rear delts and external rotators'),
                    _ex('Cable Crunch', 3, '15-20 reps', '45s', 'Round through the abs, chin to chest'),
                    _ex('Hanging Leg Raise', 3, '12 reps', '60s', 'Slow and controlled on the way down'),
                ]
            },
            'Day 6': {
                'type': 'Full Body Power', 'focus': 'Compound Strength', 'duration': '60 min', 'color': '#f43f5e',
                'exercises': [
                    _ex('Power Clean', 4, '5 reps', '120s', 'Explosive hip drive, catch in rack position'),
                    _ex('Front Squat', 3, '8 reps', '90s', 'Elbows high, upright torso'),
                    _ex('Weighted Pull-up', 3, '6-8 reps', '90s', 'Add belt weight for progression'),
                    _ex('Dumbbell Row', 3, '10 each side', '60s', 'Elbow past torso, full stretch'),
                    _ex("Farmer's Carry", 3, '30m walk', '60s', 'Heavy load, tight core, tall posture'),
                ]
            },
            'Day 7': {
                'type': 'Rest Day', 'focus': 'Recovery', 'duration': '-', 'color': '#94a3b8',
                'exercises': [
                    _ex('Complete Rest', 1, '-', '-', 'Muscles grow during recovery, not training'),
                    _ex('Protein and Nutrition Focus', 1, '-', '-', 'Hit your calorie and protein targets today'),
                    _ex('Optional Stretch / Foam Roll', 1, '15 min', '-', 'Light work only, no loading'),
                ]
            },
        }
    else:
        plans = {
            'Day 1': {
                'type': 'Moderate Cardio', 'focus': 'Aerobic Base', 'duration': '35 min', 'color': '#06b6d4',
                'exercises': [
                    _ex('Jogging', 1, '20 min', '-', 'Conversational pace, nasal breathing'),
                    _ex('Cycling', 1, '15 min', '-', 'Moderate resistance'),
                    _ex('Cool-down Walk', 1, '5 min', '-', 'Gradual heart rate drop'),
                ]
            },
            'Day 2': {
                'type': 'Upper Body', 'focus': 'Push and Pull Balance', 'duration': '40 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Push-ups', 3, '12 reps', '45s', 'Chest to floor, full range'),
                    _ex('Dumbbell Row', 3, '12 each side', '45s', 'Squeeze at top'),
                    _ex('Shoulder Press', 3, '12 reps', '45s', 'Full lockout overhead'),
                    _ex('Bicep Curl', 2, '12 reps', '30s', 'Slow and controlled'),
                    _ex('Tricep Dip', 2, '12 reps', '30s', 'Elbows stay close to body'),
                ]
            },
            'Day 3': {
                'type': 'Active Recovery', 'focus': 'Mobility', 'duration': '25 min', 'color': '#22c55e',
                'exercises': [
                    _ex('Yoga Flow', 1, '20 min', '-', 'Sun salutations and hip openers'),
                    _ex('Deep Breathing', 1, '5 min', '-', 'Box breathing for recovery'),
                ]
            },
            'Day 4': {
                'type': 'Lower Body', 'focus': 'Legs and Glutes', 'duration': '40 min', 'color': '#f97316',
                'exercises': [
                    _ex('Squats', 3, '15 reps', '45s', 'Below parallel, knees track toes'),
                    _ex('Lunges', 3, '12 each leg', '45s', 'Alternate legs, upright torso'),
                    _ex('Glute Bridge', 3, '15 reps', '30s', 'Squeeze glutes at top, hold 1s'),
                    _ex('Step-ups', 3, '12 each leg', '30s', 'Full hip extension at top'),
                    _ex('Calf Raises', 2, '20 reps', '30s', 'Single leg for more challenge'),
                ]
            },
            'Day 5': {
                'type': 'Core and Flexibility', 'focus': 'Stability', 'duration': '30 min', 'color': '#a855f7',
                'exercises': [
                    _ex('Plank', 3, '45s', '30s', 'Perfect straight line, no sagging hips'),
                    _ex('Side Plank', 3, '30s each side', '30s', 'Hip off the floor'),
                    _ex('Dead Bug', 3, '10 each side', '30s', 'Lower back pressed to floor'),
                    _ex('Bird Dog', 3, '10 each side', '30s', 'Opposite arm and leg extend'),
                    _ex('Full Body Stretch', 1, '10 min', '-', 'Hold each stretch for 30 seconds'),
                ]
            },
            'Day 6': {
                'type': 'Sports / Recreation', 'focus': 'Fun and Active', 'duration': '45+ min', 'color': '#06b6d4',
                'exercises': [
                    _ex('Football / Badminton / Swimming', 1, '45 min', '-', 'Enjoy your favourite sport'),
                    _ex('Hiking', 1, 'Optional', '-', 'Great low-impact cardio option'),
                ]
            },
            'Day 7': {
                'type': 'Rest Day', 'focus': 'Recovery', 'duration': '-', 'color': '#94a3b8',
                'exercises': [
                    _ex('Complete Rest', 1, '-', '-', 'Well-deserved rest day'),
                    _ex('Hydration Focus', 1, '-', '-', 'Drink 2.5 to 3 litres of water today'),
                ]
            },
        }
    return plans

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

            bmi = calculate_bmi(weight, height)
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = bmr * activity

            if goal.lower() == 'fat loss':
                calories = tdee - 500
            elif goal.lower() == 'muscle gain':
                calories = tdee + 300
            else:
                calories = tdee

            results = {
                'bmi': bmi,
                'calories': round(calories),
                'protein': round((calories * 0.3) / 4),
                'carbs': round((calories * 0.45) / 4),
                'fats': round((calories * 0.25) / 9),
                'weekly_diet': get_weekly_diet(goal, diet_type),
                'weekly_workout': get_weekly_workout(goal),
                'goal': goal.capitalize(),
                'weight': weight,
                'height': height
            }

            return render_template('result.html', results=results)
        except Exception as e:
            flash(f"Error in calculation: {str(e)}", "danger")
            return redirect(url_for('index'))

    # Pass saved profile to pre-fill the form
    profile = current_user if current_user.is_authenticated else None
    return render_template('index.html', profile=profile)

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
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
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
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        except Exception as e:
            flash(f'Error saving profile: {str(e)}', 'danger')
        return redirect(url_for('profile'))
    return render_template('profile.html')

if __name__ == '__main__':
    with app.app_context():
        migrate_db()   # Add new columns to existing DB if needed
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
