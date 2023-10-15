import random
from fpdf import FPDF
from datetime import datetime

# Step 1: Generate 50 random single-digit addition problems
problems = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(50)]

# Step 2: Convert to PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Single Digit Addition Worksheet', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_problem(self, x, y, a, b):
        self.set_xy(x, y)
        self.set_font('Arial', '', 12)
        self.cell(20, 10, str(a), 0, 2, 'C')
        self.cell(20, 10, f"+ {b}", 0, 2, 'C')
        self.cell(20, 10, "______", 0, 2, 'C')
        self.ln(5)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin = 15)
pdf.add_page()
pdf.set_left_margin(10)
pdf.set_right_margin(10)

col_spacing = 40
row_spacing = 50

for i, (a, b) in enumerate(problems):
    x = 10 + (i % 5) * col_spacing
    y = 30 + (i // 5) % 5 * row_spacing  # Reset y after every 5 problems
    pdf.add_problem(x, y, a, b)
    if i == 24:  # After the first 25 problems, add a new page
        pdf.add_page()

# Step 3: Output with date in filename
current_date = datetime.now().strftime("%Y%m%d")
pdf.output(f'addition_worksheet_{current_date}.pdf')