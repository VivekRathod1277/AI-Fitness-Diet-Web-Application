from fpdf import FPDF
import os
from datetime import datetime

class FitnessPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'AI Fitness Studio - 7-Day Weekly Plan', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()} | Generated on {datetime.now().strftime("%Y-%m-%d")}', 0, 0, 'C')

def generate_pdf(data):
    pdf = FitnessPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 12)

    # User Stats
    pdf.set_fill_color(240, 240, 240)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Your Fitness Summary', 0, 1, 'L', True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f'Goal: {data["goal"]}', 0, 1)
    pdf.cell(0, 10, f'BMI: {data["bmi"]}', 0, 1)
    pdf.cell(0, 10, f'Daily Target: {data["calories"]} kcal', 0, 1)
    pdf.cell(0, 10, f'Macros: P: {data["protein"]}g | C: {data["carbs"]}g | F: {data["fats"]}g', 0, 1)
    pdf.ln(10)

    # Weekly Plan
    for i in range(1, 8):
        day_key = f"Day {i}"
        diet = data['weekly_diet'][day_key]
        workout = data['weekly_workout'][day_key]

        if i % 2 == 1 and i > 1:
            pdf.add_page()

        pdf.set_font('Arial', 'B', 14)
        pdf.set_text_color(99, 102, 241) # Primary color
        pdf.cell(0, 10, f'--- {day_key} ---', 0, 1, 'C')
        pdf.set_text_color(0, 0, 0)
        
        # Diet
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, 'Diet Plan:', 0, 1)
        pdf.set_font('Arial', '', 11)
        pdf.multi_cell(0, 8, f"- Breakfast: {diet['breakfast']}")
        pdf.multi_cell(0, 8, f"- Lunch: {diet['lunch']}")
        pdf.multi_cell(0, 8, f"- Dinner: {diet['dinner']}")
        
        # Workout
        pdf.ln(2)
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, f'Workout ({workout["type"]}):', 0, 1)
        pdf.set_font('Arial', '', 11)
        for ex in workout['ex']:
            pdf.cell(0, 8, f"  * {ex}", 0, 1)
        
        pdf.ln(10)

    if not os.path.exists('static/downloads'):
        os.makedirs('static/downloads')

    filename = f"static/downloads/weekly_plan_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    pdf.output(filename)
    return filename
