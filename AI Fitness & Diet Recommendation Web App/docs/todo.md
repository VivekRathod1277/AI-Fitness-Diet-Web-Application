# Project TODO List

This document tracks all tasks across the 5-phase roadmap for the AI Fitness & Diet Recommendation Web App.

## Phase 1 — Documentation & Presentation Foundation
- [x] Add hero section to README (screenshots/GIF).
- [x] Add shields.io badges (Python, Flask, License, etc.).
- [x] Add a Routes Reference table to README.
- [x] Create `.env.example` documenting environment variables.
- [x] Update `app.py` to use `python-dotenv`.
- [x] Add a "Roadmap" section to README.
- [x] Add `CONTRIBUTING.md`.
- [x] Pin versions in `requirements.txt`.

## Phase 2 — Core UX & Usability Upgrades
- [x] Add unit toggle (kg/lb, cm/ft-in) to UI.
- [x] Add `unit_system` to `User` model & backend logic.
- [x] Implement single-food item swap AND full meal swap UI + backend route.
- [x] Add `excluded_foods` to `User` model & UI.
- [x] Update plan generator to respect allergy/exclusion filters.
- [x] Audit and fix mobile responsiveness (375px width).
- [x] Implement Dark mode toggle (CSS variables + localStorage/DB pref).

## Phase 3 — Tracking & Visualization Layer
- [x] Deep details for Diet: Include Macros & Micros (Protein, Carbs, Fats, Fiber, Iron, etc.) for generated foods.
- [x] Deep details for Workout: Detailed breakdown per exercise.
- [x] Implement Weight/BMI trend chart using `Chart.js` on dashboard.
- [x] Create `WaterLog` model and dashboard quick-log UI.
- [x] Create `FoodLog` model and manual-entry form on dashboard.
- [x] Create `/log_meal` route and daily summary card.
- [x] Compute and display a daily Streak counter badge on dashboard.

## Phase 4 — Personalization & Adaptive Intelligence
- [x] Create `WorkoutLog` model for tracking completed exercises.
- [x] Implement progressive overload rule-based logic.
- [x] Implement adaptive diet plan regeneration flag based on weight trend.
- [x] Add recovery/rest-day guidance (stretching/mobility) to workout plans.
- [x] Implement smarter macro logic (dynamic protein ratios).

## Phase 5 — Engagement & Retention Features
- [x] Configure `Flask-Mail` and create daily/weekly email reminders.
- [x] Create `UserBadge` model and badge unlocking logic.
- [x] (Optional) Create shareable progress card generation using `Pillow`.
