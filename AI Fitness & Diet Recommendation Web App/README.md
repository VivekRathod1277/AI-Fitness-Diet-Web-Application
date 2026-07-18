# AI Fitness & Diet Recommendation Web App

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Open Issues](https://img.shields.io/github/issues/VivekRathod1277/AI-Fitness-Diet-Web-Application)
![Last Commit](https://img.shields.io/github/last-commit/VivekRathod1277/AI-Fitness-Diet-Web-Application)

<p align="center">
  <img src="docs/screenshots/hero_dashboard.png" alt="Dashboard Preview" width="800">
</p>

A comprehensive, personalized fitness and diet recommendation web application built with Python (Flask). This application assists users in their fitness journey by calculating essential body metrics such as BMI and BMR, and generating highly customized weekly diet and workout plans based on their unique goals, activity levels, and dietary preferences.

## 🌟 Core Features

- **User Authentication System**: Secure sign-up, login, and session management using `Flask-Login` and password hashing with `Flask-Bcrypt`.
- **Personalized User Profiles**: Users can save their body metrics (age, gender, height, weight), activity level, and dietary preferences (e.g., Vegetarian, Eggitarian) to avoid re-entering data.
- **Advanced Fitness Calculations**:
  - **BMI (Body Mass Index)** calculation.
  - **BMR (Basal Metabolic Rate)** calculation.
  - **TDEE (Total Daily Energy Expenditure)** calculation based on activity level.
  - Macro-nutrient distribution (Protein, Carbs, Fats) calculation tailored to the user's goal (Fat Loss, Maintenance, or Muscle Gain).
- **Dynamic Weekly Diet Plans**: Automatically generates a 7-day meal plan (Breakfast, Lunch, Dinner) based on the calculated caloric needs, chosen goal, and diet type.
- **Dynamic Weekly Workout Plans**: Automatically creates a 7-day workout routine complete with exercises, sets, reps, rest periods, and form cues, categorized by goal (e.g., HIIT for Fat Loss, Hypertrophy for Muscle Gain).
- **Progress Tracking (Dashboard)**: Authenticated users can save their generated plans to their profile. A visual dashboard tracks their weight and BMI progress over time.
- **PDF Export capability**: Users can download their personalized fitness and diet plans as a beautifully formatted PDF report using the `FPDF` library.

## 🛠️ Technology Stack

- **Backend Framework**: Python, Flask
- **Database**: SQLite (managed via `Flask-SQLAlchemy`)
- **Authentication**: `Flask-Login`, `Flask-Bcrypt`
- **Frontend**: HTML5, CSS3, JavaScript (Jinja2 Templating Engine)
- **PDF Generation**: `FPDF` (located in `utils/pdf_generator.py`)
- **Containerization**: Docker

## 📂 Project Structure

```text
AI Fitness & Diet Recommendation Web App/
│
├── app.py                  # Main Flask application (Routes, Models, Logic)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration for containerized deployment
├── fitness.db              # SQLite database (generated on first run)
├── .env.example            # Environment variables template
├── CONTRIBUTING.md         # Guidelines for contributing
│
├── docs/                   # Screenshots and documentation
├── static/                 # Static assets (CSS, JS, Images)
│   └── (CSS/JS files)
│
├── templates/              # HTML templates (Jinja2)
│   ├── index.html          # Homepage / Input form
│   ├── register.html       # User Registration page
│   ├── login.html          # User Login page
│   ├── profile.html        # User Profile management
│   ├── dashboard.html      # Progress tracking & saved plans
│   └── result.html         # Generated Plan view
│
└── utils/                  # Utility scripts
    └── pdf_generator.py    # Logic for generating downloadable PDF reports
```

## 🗺️ Routes Reference

| Route | HTTP Method | Auth Required | Purpose |
|-------|-------------|---------------|---------|
| `/` | GET, POST | No | Home page / Calculate metrics & generate plan |
| `/register` | GET, POST | No | User Registration |
| `/login` | GET, POST | No | User Login |
| `/logout` | GET | Yes | User Logout |
| `/dashboard` | GET | Yes | Progress dashboard & active plans |
| `/profile` | GET, POST | Yes | View / Update user profile |
| `/save_record` | POST | Yes | Save generated plan to user account |
| `/download_pdf` | POST | No | Generate & download PDF of plan |

## 🚀 Step-by-Step Usage Guide

1. **Sign Up / Login**: 
   - Navigate to `/register` to create a new account.
   - Navigate to `/login` to access your dashboard.
2. **Setup Profile**: 
   - Once logged in, go to the **Profile** section (`/profile`).
   - Enter your metrics (Age, Gender, Weight, Height) and preferences (Activity Level, Diet Type). Saving this will pre-fill the calculator in the future.
3. **Generate a Plan**: 
   - Go to the **Home** page (`/`).
   - If your profile is set up, your details will be pre-filled. Select your ultimate goal (Fat Loss, Muscle Gain, etc.).
   - Click **Calculate & Generate Plan**.
4. **Review Results**: 
   - You will be redirected to the results page (`/result`).
   - Here, you can view your calculated BMI, TDEE, required Calories, and your Macro split.
   - Review your customized 7-Day Workout and Diet schedules.
5. **Save or Export**: 
   - Click **Save to Profile** to store this plan and log your current weight/BMI in your Dashboard history.
   - Click **Download PDF** to get a local copy of your plan.
6. **Track Progress**: 
   - Visit the **Dashboard** (`/dashboard`) to view your historical weight and BMI trends and review your currently active fitness plan.

## 💻 Getting Started (Local Development)

### Prerequisites
- Python 3.8 or higher
- `pip` (Python Package Installer)

### Installation Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd "AI Fitness & Diet Recommendation Web App"
   ```

2. **Set up a virtual environment** (Highly Recommended):
   - On Windows:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize & Run the Application**:
   ```bash
   python app.py
   ```
   *Note: The SQLite database (`fitness.db`) will be created automatically upon the first run.*

5. **Access the Web App**:
   Open your preferred web browser and navigate to: `http://127.0.0.1:5000`

## 🐳 Docker Deployment

To run the application inside an isolated Docker container without installing Python dependencies locally:

1. **Build the Docker image**:
   ```bash
   docker build -t ai-fitness-app .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 5000:5000 ai-fitness-app
   ```
3. Access the app at `http://localhost:5000`.

## 🛣️ Roadmap

- [ ] **Phase 2: Core UX & Usability**: Unit toggles, meal swapping, allergy filters, dark mode.
- [ ] **Phase 3: Tracking & Visualization**: Trend charts, water/meal trackers, streak counter.
- [ ] **Phase 4: Personalization & AI**: Progressive overload tracking, adaptive diet plan regeneration, smarter macros.
- [ ] **Phase 5: Engagement**: Email nudges, achievement badges, shareable progress cards.

## 📜 License

This project is open-source and available under the MIT License.
