import random
from fpdf import FPDF
from datetime import datetime

# Prompt the user for input
lowest_num = int(input("Enter the lowest number: "))
highest_num = int(input("Enter the highest number: "))
operation = input("Do you want addition or subtraction problems? (Enter 'addition' or 'subtraction'): ")

# Step 1: Generate 50 random problems based on user input
if operation == "addition":
    problems = [(random.randint(lowest_num, highest_num), random.randint(lowest_num, highest_num)) for _ in range(50)]
    symbol = "+"
elif operation == "subtraction":
    problems = [(random.randint(lowest_num, highest_num), random.randint(1, lowest_num)) for _ in range(50)]
    symbol = "-"
else:
    print('Error couldn\'t resolve operation. Please specify either "addition" or "subtraction"')

title = (f'Henry\'s Single Digit {operation} Minute Math')

# Step 2: Convert to PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title.title(), 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_problem(self, x, y, a, b):
        self.set_xy(x, y)
        self.set_font('Arial', '', 12)
        self.cell(20, 10, str(a), 0, 2, 'R')  # Right-aligned top number
        self.set_font('Arial', 'U', 12)  # Set underline for the bottom number
        self.cell(20, 10, f"{symbol} {b}", 0, 2, 'R')  # Right-aligned bottom number with underline
        self.set_font('Arial', '', 12)  # Reset to no underline for the answer space
        self.cell(20, 10, "", 0, 2, 'C')  # Empty space for the answer
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
pdf.output(f'{operation}_worksheet_{current_date}.pdf')