import random

DIET_DATABASE = {
    'fat loss': {
        'veg': {
            'breakfast': [
                {'name': 'Oats with berries', 'protein': 8, 'carbs': 45, 'fats': 6, 'fiber': 8, 'iron': '2mg', 'calories': 260},
                {'name': 'Moong Dal Chilla', 'protein': 12, 'carbs': 35, 'fats': 5, 'fiber': 6, 'iron': '3mg', 'calories': 230},
                {'name': 'Smoothie Bowl', 'protein': 10, 'carbs': 50, 'fats': 8, 'fiber': 9, 'iron': '1mg', 'calories': 310},
                {'name': 'Besan Poha', 'protein': 9, 'carbs': 40, 'fats': 7, 'fiber': 5, 'iron': '2mg', 'calories': 250},
                {'name': 'Greek Yogurt with Nuts', 'protein': 15, 'carbs': 15, 'fats': 12, 'fiber': 3, 'iron': '1mg', 'calories': 230}
            ],
            'lunch': [
                {'name': 'Quinoa Salad', 'protein': 14, 'carbs': 45, 'fats': 10, 'fiber': 10, 'iron': '4mg', 'calories': 320},
                {'name': 'Paneer & Veggie Wrap', 'protein': 18, 'carbs': 40, 'fats': 15, 'fiber': 7, 'iron': '2mg', 'calories': 370},
                {'name': 'Lentil Soup with Brown Rice', 'protein': 16, 'carbs': 55, 'fats': 4, 'fiber': 12, 'iron': '5mg', 'calories': 320},
                {'name': 'Soya Chunks Stir-fry', 'protein': 25, 'carbs': 20, 'fats': 8, 'fiber': 8, 'iron': '6mg', 'calories': 250},
                {'name': 'Mixed Bean Salad', 'protein': 15, 'carbs': 35, 'fats': 5, 'fiber': 14, 'iron': '4mg', 'calories': 240}
            ],
            'dinner': [
                {'name': 'Roasted Vegetables', 'protein': 5, 'carbs': 25, 'fats': 8, 'fiber': 8, 'iron': '2mg', 'calories': 190},
                {'name': 'Paneer Tikka with Salad', 'protein': 20, 'carbs': 15, 'fats': 18, 'fiber': 5, 'iron': '1mg', 'calories': 300},
                {'name': 'Dal Khichdi (Light)', 'protein': 12, 'carbs': 40, 'fats': 6, 'fiber': 6, 'iron': '3mg', 'calories': 260},
                {'name': 'Vegetable Clear Soup', 'protein': 3, 'carbs': 15, 'fats': 2, 'fiber': 4, 'iron': '1mg', 'calories': 90},
                {'name': 'Mushroom Sauté', 'protein': 6, 'carbs': 10, 'fats': 7, 'fiber': 3, 'iron': '2mg', 'calories': 130}
            ]
        },
        'eggitarian': {
            'breakfast': [
                {'name': 'Boiled Eggs & Toast', 'protein': 16, 'carbs': 25, 'fats': 10, 'fiber': 3, 'iron': '2mg', 'calories': 250},
                {'name': 'Egg White Omelet', 'protein': 20, 'carbs': 5, 'fats': 2, 'fiber': 1, 'iron': '0.5mg', 'calories': 120},
                {'name': 'Scrambled Eggs with Spinach', 'protein': 18, 'carbs': 6, 'fats': 12, 'fiber': 2, 'iron': '3mg', 'calories': 200},
                {'name': 'Protein Pancakes', 'protein': 22, 'carbs': 30, 'fats': 6, 'fiber': 5, 'iron': '2mg', 'calories': 260},
                {'name': 'Poached Eggs on Rye', 'protein': 14, 'carbs': 20, 'fats': 10, 'fiber': 4, 'iron': '2mg', 'calories': 230}
            ],
            'lunch': [
                {'name': 'Grilled Chicken Salad', 'protein': 35, 'carbs': 10, 'fats': 8, 'fiber': 4, 'iron': '2mg', 'calories': 250},
                {'name': 'Egg Curry (Light)', 'protein': 18, 'carbs': 20, 'fats': 14, 'fiber': 3, 'iron': '2mg', 'calories': 280},
                {'name': 'Tuna/Egg Wrap', 'protein': 25, 'carbs': 30, 'fats': 10, 'fiber': 5, 'iron': '3mg', 'calories': 310},
                {'name': 'Baked Fish with Greens', 'protein': 30, 'carbs': 5, 'fats': 6, 'fiber': 4, 'iron': '1mg', 'calories': 190},
                {'name': 'Turkey Breast Sandwich', 'protein': 28, 'carbs': 35, 'fats': 7, 'fiber': 5, 'iron': '2mg', 'calories': 315}
            ],
            'dinner': [
                {'name': 'Chicken Stir-fry', 'protein': 30, 'carbs': 15, 'fats': 8, 'fiber': 5, 'iron': '2mg', 'calories': 250},
                {'name': 'Omelet with Veggies', 'protein': 16, 'carbs': 8, 'fats': 12, 'fiber': 3, 'iron': '2mg', 'calories': 200},
                {'name': 'Grilled Chicken & Broccoli', 'protein': 40, 'carbs': 10, 'fats': 5, 'fiber': 6, 'iron': '2mg', 'calories': 245},
                {'name': 'Egg Bhurji (No Butter)', 'protein': 15, 'carbs': 5, 'fats': 10, 'fiber': 2, 'iron': '2mg', 'calories': 170},
                {'name': 'Salmon with Asparagus', 'protein': 25, 'carbs': 8, 'fats': 15, 'fiber': 4, 'iron': '1mg', 'calories': 270}
            ]
        }
    },
    'muscle gain': {
        'veg': {
            'breakfast': [
                {'name': 'Paneer Paratha', 'protein': 18, 'carbs': 55, 'fats': 18, 'fiber': 6, 'iron': '2mg', 'calories': 450},
                {'name': 'Protein Smoothie with Oats', 'protein': 25, 'carbs': 60, 'fats': 10, 'fiber': 8, 'iron': '3mg', 'calories': 430},
                {'name': 'Peanut Butter Toast & Milk', 'protein': 20, 'carbs': 45, 'fats': 22, 'fiber': 5, 'iron': '1mg', 'calories': 460},
                {'name': 'Sprouted Salad & Paneer', 'protein': 22, 'carbs': 35, 'fats': 12, 'fiber': 10, 'iron': '5mg', 'calories': 340},
                {'name': 'Tofu Scramble', 'protein': 20, 'carbs': 15, 'fats': 15, 'fiber': 4, 'iron': '4mg', 'calories': 275}
            ],
            'lunch': [
                {'name': 'Dal Makhani & Brown Rice', 'protein': 22, 'carbs': 75, 'fats': 15, 'fiber': 15, 'iron': '6mg', 'calories': 520},
                {'name': 'Paneer Butter Masala (Mod) & Roti', 'protein': 25, 'carbs': 60, 'fats': 25, 'fiber': 8, 'iron': '3mg', 'calories': 560},
                {'name': 'Soya Chunk Pulao', 'protein': 30, 'carbs': 65, 'fats': 12, 'fiber': 10, 'iron': '7mg', 'calories': 490},
                {'name': 'Chickpea Curry & Quinoa', 'protein': 20, 'carbs': 70, 'fats': 10, 'fiber': 16, 'iron': '6mg', 'calories': 450},
                {'name': 'Rajma Chawal', 'protein': 18, 'carbs': 80, 'fats': 8, 'fiber': 14, 'iron': '5mg', 'calories': 460}
            ],
            'dinner': [
                {'name': 'Paneer Bhurji & Roti', 'protein': 25, 'carbs': 50, 'fats': 20, 'fiber': 7, 'iron': '3mg', 'calories': 480},
                {'name': 'Lentil Pasta', 'protein': 22, 'carbs': 60, 'fats': 8, 'fiber': 12, 'iron': '4mg', 'calories': 400},
                {'name': 'Tofu & Veggie Stir-fry', 'protein': 20, 'carbs': 25, 'fats': 14, 'fiber': 6, 'iron': '4mg', 'calories': 310},
                {'name': 'Stuffed Mushrooms & Paneer', 'protein': 18, 'carbs': 15, 'fats': 15, 'fiber': 5, 'iron': '2mg', 'calories': 270},
                {'name': 'Vegetable Stew & Bread', 'protein': 10, 'carbs': 55, 'fats': 8, 'fiber': 8, 'iron': '3mg', 'calories': 330}
            ]
        },
        'eggitarian': {
            'breakfast': [
                {'name': 'Whole Eggs Omelet (3-4 eggs)', 'protein': 24, 'carbs': 5, 'fats': 20, 'fiber': 1, 'iron': '3mg', 'calories': 295},
                {'name': 'Chicken Sausage & Eggs', 'protein': 30, 'carbs': 10, 'fats': 25, 'fiber': 2, 'iron': '4mg', 'calories': 385},
                {'name': 'French Toast with Honey', 'protein': 15, 'carbs': 65, 'fats': 12, 'fiber': 3, 'iron': '2mg', 'calories': 430},
                {'name': 'Egg & Cheese Sandwich', 'protein': 22, 'carbs': 40, 'fats': 18, 'fiber': 4, 'iron': '3mg', 'calories': 410},
                {'name': 'Protein Oats with Egg Whites', 'protein': 35, 'carbs': 50, 'fats': 8, 'fiber': 6, 'iron': '3mg', 'calories': 410}
            ],
            'lunch': [
                {'name': 'Chicken Breast & Rice', 'protein': 45, 'carbs': 70, 'fats': 8, 'fiber': 3, 'iron': '2mg', 'calories': 530},
                {'name': 'Egg Fried Rice (High Protein)', 'protein': 25, 'carbs': 65, 'fats': 15, 'fiber': 5, 'iron': '3mg', 'calories': 495},
                {'name': 'Beef/Chicken Burrito', 'protein': 35, 'carbs': 60, 'fats': 20, 'fiber': 8, 'iron': '5mg', 'calories': 560},
                {'name': 'Grilled Fish & Sweet Potato', 'protein': 40, 'carbs': 50, 'fats': 12, 'fiber': 7, 'iron': '2mg', 'calories': 470},
                {'name': 'Lamb Chops & Veggies', 'protein': 35, 'carbs': 20, 'fats': 28, 'fiber': 6, 'iron': '4mg', 'calories': 470}
            ],
            'dinner': [
                {'name': 'Steak & Mashed Potatoes', 'protein': 40, 'carbs': 55, 'fats': 22, 'fiber': 5, 'iron': '6mg', 'calories': 580},
                {'name': 'Chicken Pasta', 'protein': 35, 'carbs': 70, 'fats': 12, 'fiber': 6, 'iron': '3mg', 'calories': 530},
                {'name': 'Grilled Salmon & Rice', 'protein': 35, 'carbs': 50, 'fats': 18, 'fiber': 3, 'iron': '2mg', 'calories': 500},
                {'name': 'Scrambled Eggs & Avocado Toast', 'protein': 20, 'carbs': 35, 'fats': 25, 'fiber': 10, 'iron': '3mg', 'calories': 445},
                {'name': 'Turkey Burger (No Bun)', 'protein': 35, 'carbs': 15, 'fats': 12, 'fiber': 4, 'iron': '3mg', 'calories': 310}
            ]
        }
    }
}

def filter_foods(food_list, excluded_foods_str):
    if not excluded_foods_str:
        return food_list
    excluded = [e.strip().lower() for e in excluded_foods_str.split(',') if e.strip()]
    if not excluded:
        return food_list
        
    filtered = []
    for item in food_list:
        name_lower = item['name'].lower()
        if not any(ex in name_lower for ex in excluded):
            filtered.append(item)
            
    # If filtering removes everything, return original to avoid crashing
    return filtered if filtered else food_list

def scale_meal(meal, target_meal_calories):
    if meal['calories'] == 0: return meal
    multiplier = target_meal_calories / meal['calories']
    scaled = meal.copy()
    scaled['calories'] = int(round(meal['calories'] * multiplier))
    scaled['protein'] = int(round(meal['protein'] * multiplier))
    scaled['carbs'] = int(round(meal['carbs'] * multiplier))
    scaled['fats'] = int(round(meal['fats'] * multiplier))
    scaled['fiber'] = int(round(meal['fiber'] * multiplier))
    
    if isinstance(meal['iron'], str) and 'mg' in meal['iron'].lower():
        try:
            iron_val = float(meal['iron'].lower().replace('mg', '').strip())
            scaled['iron'] = f"{round(iron_val * multiplier, 1)}mg"
        except:
            pass
    return scaled

def get_weekly_diet(goal, diet_type, excluded_foods_str='', target_calories=2000):
    goal = goal.lower()
    if goal not in DIET_DATABASE:
        goal = 'fat loss'
        
    pool = DIET_DATABASE.get(goal).get(diet_type.lower(), DIET_DATABASE['fat loss']['veg'])
    
    breakfasts = filter_foods(pool['breakfast'], excluded_foods_str)
    lunches = filter_foods(pool['lunch'], excluded_foods_str)
    dinners = filter_foods(pool['dinner'], excluded_foods_str)
    
    b_target = target_calories * 0.30
    l_target = target_calories * 0.40
    d_target = target_calories * 0.30
    
    weekly_plan = {}
    for i in range(1, 8):
        weekly_plan[f"Day {i}"] = {
            'breakfast': scale_meal(random.choice(breakfasts), b_target),
            'lunch': scale_meal(random.choice(lunches), l_target),
            'dinner': scale_meal(random.choice(dinners), d_target)
        }
    return weekly_plan

def get_alternative_meal(goal, diet_type, meal_type, excluded_foods_str='', target_calories=2000):
    goal = goal.lower()
    if goal not in DIET_DATABASE:
        goal = 'fat loss'
    pool = DIET_DATABASE.get(goal).get(diet_type.lower(), DIET_DATABASE['fat loss']['veg'])
    meals = filter_foods(pool.get(meal_type, pool['breakfast']), excluded_foods_str)
    meal = random.choice(meals)
    
    multiplier = 0.30
    if meal_type.lower() == 'lunch':
        multiplier = 0.40
    elif meal_type.lower() == 'dinner':
        multiplier = 0.30
        
    return scale_meal(meal, target_calories * multiplier)

def _ex(name, sets, reps, rest, notes='', target=''):
    return {'name': name, 'sets': sets, 'reps': reps, 'rest': rest, 'notes': notes, 'target': target}

def get_weekly_workout(goal, workout_style='home'):
    if goal.lower() == 'fat loss':
        plans = {
            'Day 1': {
                'type': 'HIIT Cardio', 'focus': 'Full Body Fat Burn', 'duration': '40 min', 'color': '#f43f5e',
                'exercises': [
                    _ex('Burpees', 4, '15 reps', '30s', 'Explosive jump at top, land softly', 'Full Body, Core'),
                    _ex('Mountain Climbers', 4, '20 each leg', '30s', 'Keep hips level, fast pace', 'Core, Shoulders'),
                    _ex('Jumping Jacks', 3, '40 reps', '20s', 'Full arm extension overhead', 'Cardio, Calves'),
                    _ex('High Knees', 4, '30s', '30s', 'Drive knees above waist height', 'Cardio, Hip Flexors'),
                    _ex('Jump Rope', 3, '60s', '30s', 'Stay light on your toes', 'Cardio, Calves'),
                ]
            },
            'Day 2': {
                'type': 'Upper Body Strength', 'focus': 'Chest, Shoulders, Triceps', 'duration': '45 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Push-ups', 4, '15 reps', '45s', 'Full ROM, chest touches floor', 'Chest, Triceps'),
                    _ex('Pike Push-ups', 3, '12 reps', '45s', 'Targets shoulders, hips high', 'Shoulders'),
                    _ex('Tricep Dips (Chair)', 3, '12 reps', '45s', 'Elbows close to body', 'Triceps'),
                    _ex('Diamond Push-ups', 3, '10 reps', '45s', 'Hands form a diamond shape', 'Inner Chest, Triceps'),
                    _ex('Plank Hold', 3, '60s', '30s', 'Straight line head to heel', 'Core, Shoulders'),
                ]
            },
            'Day 3': {
                'type': 'Active Recovery', 'focus': 'Mobility and Flexibility', 'duration': '30 min', 'color': '#22c55e',
                'exercises': [
                    _ex('Brisk Walk', 1, '20 min', '-', 'Maintain conversational pace', 'Cardio Recovery'),
                    _ex('Hip Flexor Stretch', 2, '60s each side', '-', 'Lunge position, push hips forward', 'Hip Flexors'),
                    _ex('Cat-Cow Stretch', 2, '10 reps', '-', 'Slow and controlled breathing', 'Spine Mobility'),
                    _ex('Pigeon Pose', 2, '60s each side', '-', 'Hold and breathe deeply', 'Glutes, Hips'),
                    _ex("Child's Pose", 2, '60s', '-', 'Relax entire back', 'Lower Back'),
                ]
            },
            'Day 4': {
                'type': 'HIIT Cardio', 'focus': 'Speed and Agility', 'duration': '40 min', 'color': '#f43f5e',
                'exercises': [
                    _ex('Sprint Intervals', 6, '30s on / 30s off', '-', 'Max effort on, walk during off', 'Cardio, Quads'),
                    _ex('Box Jumps', 4, '12 reps', '45s', 'Land with soft knees, step down', 'Explosive Power, Legs'),
                    _ex('Lateral Shuffles', 4, '30s', '30s', 'Stay low, quick feet', 'Agility, Outer Thighs'),
                    _ex('Jump Squats', 4, '15 reps', '45s', 'Explode upward, land quietly', 'Quads, Glutes'),
                    _ex('Plank to Downdog', 3, '10 reps', '30s', 'Controlled transition', 'Core, Shoulders'),
                ]
            },
            'Day 5': {
                'type': 'Lower Body Strength', 'focus': 'Glutes, Quads, Hamstrings', 'duration': '45 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Bodyweight Squats', 4, '20 reps', '45s', 'Knees track over toes, depth below parallel', 'Quads, Glutes'),
                    _ex('Reverse Lunges', 3, '12 each leg', '45s', 'Back knee hovers above floor', 'Glutes, Hamstrings'),
                    _ex('Glute Bridges', 4, '20 reps', '30s', 'Squeeze glutes at top, hold 1s', 'Glutes, Lower Back'),
                    _ex('Wall Sit', 3, '60s', '45s', 'Thighs parallel to floor', 'Quads endurance'),
                    _ex('Calf Raises', 3, '20 reps', '30s', 'Full extension at top, pause', 'Calves'),
                ]
            },
            'Day 6': {
                'type': 'Full Body Circuit', 'focus': 'Endurance and Strength', 'duration': '50 min', 'color': '#f97316',
                'exercises': [
                    _ex('Burpee + Push-up', 4, '10 reps', '45s', 'Add push-up at the bottom of each burpee', 'Full Body'),
                    _ex('Squat + Overhead Press', 3, '12 reps', '45s', 'Use dumbbells or water bottles', 'Quads, Shoulders'),
                    _ex('Renegade Row', 3, '10 each side', '45s', 'Keep hips square to floor', 'Back, Core'),
                    _ex('Jumping Lunges', 3, '10 each leg', '45s', 'Explosive switch, land softly', 'Legs, Cardio'),
                    _ex('Plank + Shoulder Tap', 3, '10 each side', '30s', 'Minimal hip rotation', 'Core stability'),
                ]
            },
            'Day 7': {
                'type': 'Rest Day', 'focus': 'Recovery', 'duration': '-', 'color': '#94a3b8',
                'exercises': [
                    _ex('Complete Rest', 1, '-', '-', 'Let your muscles repair and grow', 'CNS Recovery'),
                    _ex('Foam Rolling', 1, '10-15 min', '-', 'Focus on sore muscle groups', 'Myofascial Release'),
                ]
            },
        }
    elif goal.lower() == 'muscle gain':
        plans = {
            'Day 1': {
                'type': 'Chest and Triceps', 'focus': 'Upper Body Push', 'duration': '60 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Bench Press', 4, '8-10 reps', '90s', 'Full ROM, controlled descent, drive through chest', 'Chest (Pec Major)'),
                    _ex('Incline Dumbbell Press', 3, '10-12 reps', '75s', 'Elbows at 45 degrees, squeeze at top', 'Upper Chest'),
                    _ex('Cable Chest Fly', 3, '12-15 reps', '60s', 'Slight bend in elbows, feel the stretch', 'Inner Chest'),
                    _ex('Tricep Rope Pushdown', 3, '12-15 reps', '45s', 'Flare hands at bottom of movement', 'Triceps (Lateral Head)'),
                    _ex('Overhead Tricep Extension', 3, '12 reps', '45s', 'Keep elbows pointing forward', 'Triceps (Long Head)'),
                ]
            },
            'Day 2': {
                'type': 'Back and Biceps', 'focus': 'Upper Body Pull', 'duration': '60 min', 'color': '#06b6d4',
                'exercises': [
                    _ex('Deadlift', 4, '6-8 reps', '120s', 'Neutral spine, drive through heels', 'Lower Back, Hamstrings, Glutes'),
                    _ex('Pull-ups / Lat Pulldown', 3, '8-10 reps', '90s', 'Full extension at bottom', 'Lats, Biceps'),
                    _ex('Seated Cable Row', 3, '10-12 reps', '75s', 'Pull elbows back, squeeze scapula', 'Mid Back (Rhomboids)'),
                    _ex('Dumbbell Bicep Curl', 3, '12 reps', '60s', 'Supinate at top, no swinging', 'Biceps (Short Head)'),
                    _ex('Hammer Curl', 3, '12 reps', '45s', 'Targets brachialis and forearms', 'Brachialis, Forearms'),
                ]
            },
            'Day 3': {
                'type': 'Rest / Active Recovery', 'focus': 'Mobility', 'duration': '20-30 min', 'color': '#22c55e',
                'exercises': [
                    _ex('Light Walk or Cycle', 1, '20 min', '-', 'Keep heart rate low, recover actively', 'Active Recovery'),
                    _ex('Thoracic Spine Stretch', 2, '60s', '-', 'Use foam roller on upper back', 'Spine Mobility'),
                    _ex('Lat Stretch', 2, '60s each side', '-', 'Doorframe or band stretch', 'Lats Flexibility'),
                    _ex('Wrist and Forearm Stretch', 2, '60s', '-', 'Important after heavy pulling days', 'Forearms'),
                ]
            },
            'Day 4': {
                'type': 'Legs', 'focus': 'Quads, Hamstrings, Glutes, Calves', 'duration': '65 min', 'color': '#f97316',
                'exercises': [
                    _ex('Barbell Squat', 4, '8-10 reps', '120s', 'Depth below parallel, chest up, brace core', 'Quads, Glutes'),
                    _ex('Romanian Deadlift', 3, '10-12 reps', '90s', 'Hinge at hips, feel hamstring stretch', 'Hamstrings, Glutes'),
                    _ex('Leg Press', 3, '12-15 reps', '75s', 'Feet shoulder-width, full ROM', 'Quads'),
                    _ex('Leg Curl', 3, '12-15 reps', '60s', 'Slow eccentric, squeeze at top', 'Hamstrings isolation'),
                    _ex('Standing Calf Raise', 4, '15-20 reps', '45s', 'Full extension, hold 1s at top', 'Calves'),
                ]
            },
            'Day 5': {
                'type': 'Shoulders and Abs', 'focus': 'Deltoids and Core', 'duration': '55 min', 'color': '#a855f7',
                'exercises': [
                    _ex('Overhead Press (BB/DB)', 4, '8-10 reps', '90s', 'Full lockout overhead, no lower-back arch', 'Anterior Deltoid'),
                    _ex('Lateral Raise', 3, '12-15 reps', '60s', 'Lead with elbows, slight forward lean', 'Lateral Deltoid'),
                    _ex('Face Pull', 3, '15 reps', '45s', 'Targets rear delts and external rotators', 'Rear Deltoid, Traps'),
                    _ex('Cable Crunch', 3, '15-20 reps', '45s', 'Round through the abs, chin to chest', 'Rectus Abdominis'),
                    _ex('Hanging Leg Raise', 3, '12 reps', '60s', 'Slow and controlled on the way down', 'Lower Abs'),
                ]
            },
            'Day 6': {
                'type': 'Full Body Power', 'focus': 'Compound Strength', 'duration': '60 min', 'color': '#f43f5e',
                'exercises': [
                    _ex('Power Clean', 4, '5 reps', '120s', 'Explosive hip drive, catch in rack position', 'Full Body Power'),
                    _ex('Front Squat', 3, '8 reps', '90s', 'Elbows high, upright torso', 'Quads, Core'),
                    _ex('Weighted Pull-up', 3, '6-8 reps', '90s', 'Add belt weight for progression', 'Lats, Biceps'),
                    _ex('Dumbbell Row', 3, '10 each side', '60s', 'Elbow past torso, full stretch', 'Lats, Rhomboids'),
                    _ex("Farmer's Carry", 3, '30m walk', '60s', 'Heavy load, tight core, tall posture', 'Grip, Core'),
                ]
            },
            'Day 7': {
                'type': 'Rest Day', 'focus': 'Recovery', 'duration': '-', 'color': '#94a3b8',
                'exercises': [
                    _ex('Complete Rest', 1, '-', '-', 'Muscles grow during recovery, not training', 'Systemic Recovery'),
                    _ex('Protein and Nutrition Focus', 1, '-', '-', 'Hit your calorie and protein targets today', 'Nutrition'),
                    _ex('Optional Stretch / Foam Roll', 1, '15 min', '-', 'Light work only, no loading', 'Active Recovery'),
                ]
            },
        }
    else:
        plans = {
            'Day 1': {
                'type': 'Moderate Cardio', 'focus': 'Aerobic Base', 'duration': '35 min', 'color': '#06b6d4',
                'exercises': [
                    _ex('Jogging', 1, '20 min', '-', 'Conversational pace, nasal breathing', 'Cardio'),
                    _ex('Cycling', 1, '15 min', '-', 'Moderate resistance', 'Legs, Cardio'),
                    _ex('Cool-down Walk', 1, '5 min', '-', 'Gradual heart rate drop', 'Recovery'),
                ]
            },
            'Day 2': {
                'type': 'Upper Body', 'focus': 'Push and Pull Balance', 'duration': '40 min', 'color': '#6366f1',
                'exercises': [
                    _ex('Push-ups', 3, '12 reps', '45s', 'Chest to floor, full range', 'Chest, Triceps'),
                    _ex('Dumbbell Row', 3, '12 each side', '45s', 'Squeeze at top', 'Back, Biceps'),
                    _ex('Shoulder Press', 3, '12 reps', '45s', 'Full lockout overhead', 'Shoulders'),
                    _ex('Bicep Curl', 2, '12 reps', '30s', 'Slow and controlled', 'Biceps'),
                    _ex('Tricep Dip', 2, '12 reps', '30s', 'Elbows stay close to body', 'Triceps'),
                ]
            },
            'Day 3': {
                'type': 'Active Recovery', 'focus': 'Mobility', 'duration': '25 min', 'color': '#22c55e',
                'exercises': [
                    _ex('Yoga Flow', 1, '20 min', '-', 'Sun salutations and hip openers', 'Flexibility'),
                    _ex('Deep Breathing', 1, '5 min', '-', 'Box breathing for recovery', 'Relaxation'),
                ]
            },
            'Day 4': {
                'type': 'Lower Body', 'focus': 'Legs and Glutes', 'duration': '40 min', 'color': '#f97316',
                'exercises': [
                    _ex('Squats', 3, '15 reps', '45s', 'Below parallel, knees track toes', 'Quads, Glutes'),
                    _ex('Lunges', 3, '12 each leg', '45s', 'Alternate legs, upright torso', 'Glutes, Quads'),
                    _ex('Glute Bridge', 3, '15 reps', '30s', 'Squeeze glutes at top, hold 1s', 'Glutes'),
                    _ex('Step-ups', 3, '12 each leg', '30s', 'Full hip extension at top', 'Quads'),
                    _ex('Calf Raises', 2, '20 reps', '30s', 'Single leg for more challenge', 'Calves'),
                ]
            },
            'Day 5': {
                'type': 'Core and Flexibility', 'focus': 'Stability', 'duration': '30 min', 'color': '#a855f7',
                'exercises': [
                    _ex('Plank', 3, '45s', '30s', 'Perfect straight line, no sagging hips', 'Core'),
                    _ex('Side Plank', 3, '30s each side', '30s', 'Hip off the floor', 'Obliques'),
                    _ex('Dead Bug', 3, '10 each side', '30s', 'Lower back pressed to floor', 'Core'),
                    _ex('Bird Dog', 3, '10 each side', '30s', 'Opposite arm and leg extend', 'Lower Back'),
                    _ex('Full Body Stretch', 1, '10 min', '-', 'Hold each stretch for 30 seconds', 'Flexibility'),
                ]
            },
            'Day 6': {
                'type': 'Sports / Recreation', 'focus': 'Fun and Active', 'duration': '45+ min', 'color': '#06b6d4',
                'exercises': [
                    _ex('Football / Badminton / Swimming', 1, '45 min', '-', 'Enjoy your favourite sport', 'Cardio'),
                    _ex('Hiking', 1, 'Optional', '-', 'Great low-impact cardio option', 'Endurance'),
                ]
            },
            'Day 7': {
                'type': 'Rest Day', 'focus': 'Recovery', 'duration': '-', 'color': '#94a3b8',
                'exercises': [
                    _ex('Complete Rest', 1, '-', '-', 'Well-deserved rest day', 'Recovery'),
                    _ex('Hydration Focus', 1, '-', '-', 'Drink 2.5 to 3 litres of water today', 'Health'),
                ]
            },
        }

    if workout_style.lower() == 'yoga':
        for day, data in plans.items():
            if 'Rest' not in data['type']:
                data['type'] = 'Yoga Flow'
                data['focus'] = 'Flexibility & Core'
                data['exercises'] = [
                    _ex('Sun Salutations', 3, '5 reps', '30s', 'Flow with breath', 'Full Body'),
                    _ex('Downward Dog', 3, '60s hold', '30s', 'Press heels to floor', 'Hamstrings, Shoulders'),
                    _ex('Warrior II', 3, '45s each side', '30s', 'Keep front knee over ankle', 'Legs, Core'),
                    _ex('Tree Pose', 3, '60s each side', '30s', 'Find balance, engage core', 'Balance'),
                    _ex("Child's Pose", 1, '2 min', '-', 'Relax and breathe deeply', 'Recovery')
                ]
    elif workout_style.lower() == 'gym':
        swaps = {
            'Push-ups': 'Bench Press',
            'Diamond Push-ups': 'Tricep Rope Pushdown',
            'Pike Push-ups': 'Overhead Dumbbell Press',
            'Tricep Dips': 'Cable Tricep Extensions',
            'Bodyweight Squats': 'Barbell Squats',
            'Reverse Lunges': 'Dumbbell Lunges',
            'Glute Bridges': 'Barbell Hip Thrusts',
            'Wall Sit': 'Leg Press',
            'Burpees': 'Kettlebell Swings',
            'Jump Squats': 'Box Jumps',
            'Pull-ups': 'Lat Pulldown',
            'Plank': 'Weighted Plank'
        }
        for day, data in plans.items():
            if 'Rest' not in data['type']:
                data['type'] += ' (Gym)'
            for ex in data.get('exercises', []):
                for old, new in swaps.items():
                    if old in ex['name']:
                        ex['name'] = ex['name'].replace(old, new)
                        if 'Weighted' not in ex['notes']:
                            ex['notes'] = 'Use challenging weights. ' + ex['notes']
                        if 'min' not in ex['reps'] and 's' not in ex['reps']:
                            ex['reps'] = '8-12 reps'

    return plans
