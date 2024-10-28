import random
from fpdf import FPDF
from datetime import datetime

# Constants
NUM_PROBLEMS = 50
COL_SPACING = 40
ROW_SPACING = 50
STUDENT_NAME = 'Henry'

def generate_problems(lowest_num, highest_num, operation, times_table=None):
    if operation == "addition":
        return [(random.randint(lowest_num, highest_num), random.randint(lowest_num, highest_num)) for _ in range(NUM_PROBLEMS)], "+"
    elif operation == "subtraction":
        return [(random.randint(lowest_num, highest_num), random.randint(1, lowest_num)) for _ in range(NUM_PROBLEMS)], "-"
    elif operation == "multiplication":
        if times_table is not None:
            return [(times_table, random.randint(lowest_num, highest_num)) for _ in range(NUM_PROBLEMS)], "×"
        else:
            return [(random.randint(lowest_num, highest_num), random.randint(lowest_num, highest_num)) for _ in range(NUM_PROBLEMS)], "×"
    elif operation == "division":
        if times_table is not None:
            return [(random.randint(lowest_num, highest_num) * times_table, times_table) for _ in range(NUM_PROBLEMS)], "÷"
        else:
            return [(random.randint(lowest_num, highest_num), random.randint(1, highest_num)) for _ in range(NUM_PROBLEMS)], "÷"
    else:
        raise ValueError('Please specify either "addition", "subtraction", "multiplication", or "division"')

# Prompt the user for input
lowest_num = int(input("Enter the lowest number: "))
highest_num = int(input("Enter the highest number: "))
operation = input("Do you want addition, subtraction, multiplication, or division problems? (Enter 'addition', 'subtraction', 'multiplication', or 'division'): ")

times_table = None
if operation in ["multiplication", "division"]:
    times_table_input = input("Do you want to focus on a specific times table? (Enter 'yes' or 'no'): ")
    if times_table_input.lower() == 'yes':
        times_table = int(input("Enter the times table number: "))

problems, symbol = generate_problems(lowest_num, highest_num, operation, times_table)
title = STUDENT_NAME+'\'s'+(f' {operation} Minute Math').title()

# Convert to PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_problem(self, x, y, a, b, symbol):
        self.set_xy(x, y)
        self.set_font('Arial', '', 12)
        self.cell(20, 10, str(a), 0, 2, 'R')
        self.set_font('Arial', 'U', 12)
        self.cell(20, 10, f"{symbol} {b}", 0, 2, 'R')
        self.set_font('Arial', '', 12)
        self.cell(20, 10, "", 0, 2, 'C')
        self.ln(5)

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin = 15)
pdf.add_page()

for i, (a, b) in enumerate(problems):
    x = 10 + (i % 5) * COL_SPACING
    y = 30 + (i // 5) % 5 * ROW_SPACING
    pdf.add_problem(x, y, a, b, symbol)
    if i == 24:
        pdf.add_page()

# Output with date in filename
current_date = datetime.now().strftime("%Y%m%d")
pdf.output(f'{operation}_worksheet_{current_date}.pdf')