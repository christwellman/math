import random
from fpdf import FPDF
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Literal, Optional

# Type definitions
OperationType = Literal["addition", "subtraction", "multiplication", "division"]
Problem = Tuple[int, int]

class WorksheetConfig:
    """Configuration settings for math worksheet generation"""
    # Layout constants
    COL_SPACING = 40
    ROW_SPACING = 40
    PROBLEMS_PER_PAGE = 30  # 5 columns × 6 rows
    DEFAULT_NUM_PROBLEMS = 60
    
    # Valid operations with their symbols
    OPERATIONS = {
        "addition": "+",
        "subtraction": "-",
        "multiplication": "×",
        "division": "÷"
    }
    
    def __init__(self):
        self.lowest_num: int = 0
        self.highest_num: int = 10
        self.operation: OperationType = "addition"
        self.num_problems: int = self.DEFAULT_NUM_PROBLEMS
        self.times_table: Optional[int] = None

class MathWorksheetPDF(FPDF):
    """Custom PDF class for math worksheet generation"""
    
    def __init__(self, student_name: str, operation: str):
        super().__init__()
        self.student_name = student_name
        self.operation = operation.capitalize()
        
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f"{self.student_name}'s {self.operation} Minute Math", 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def add_problem(self, x: int, y: int, a: int, b: int, symbol: str):
        self.set_xy(x, y)
        self.set_font('Arial', '', 12)
        self.cell(20, 10, str(a), 0, 2, 'R')
        self.set_font('Arial', 'U', 12)
        self.cell(20, 10, f"{symbol} {b}", 0, 2, 'R')
        self.set_font('Arial', '', 12)
        self.cell(20, 10, "", 0, 2, 'C')
        self.ln(5)

class WorksheetGenerator:
    """Main class for generating math worksheets"""
    
    def __init__(self):
        self.config = WorksheetConfig()
        
    def generate_problems(self) -> List[Problem]:
        """Generate math problems based on current configuration"""
        problems = []
        
        for _ in range(self.config.num_problems):
            if self.config.operation == "addition":
                a = random.randint(self.config.lowest_num, self.config.highest_num)
                b = random.randint(self.config.lowest_num, self.config.highest_num)
                problems.append((a, b))
                
            elif self.config.operation == "subtraction":
                a = random.randint(self.config.lowest_num, self.config.highest_num)
                b = random.randint(self.config.lowest_num, self.config.highest_num)
                problems.append((max(a, b), min(a, b)))
                
            elif self.config.operation == "multiplication":
                if self.config.times_table is not None:
                    a = self.config.times_table
                    b = random.randint(self.config.lowest_num, self.config.highest_num)
                else:
                    a = random.randint(self.config.lowest_num, self.config.highest_num)
                    b = random.randint(self.config.lowest_num, self.config.highest_num)
                problems.append((a, b))
                
            elif self.config.operation == "division":
                if self.config.times_table is not None:
                    b = self.config.times_table
                    a = b * random.randint(self.config.lowest_num, self.config.highest_num)
                else:
                    b = random.randint(1, self.config.highest_num)  # Avoid division by zero
                    a = b * random.randint(self.config.lowest_num, self.config.highest_num)
                problems.append((a, b))
                
        return problems

    def create_worksheet(self, student_name: str) -> str:
        """Create a worksheet PDF for a given student"""
        problems = self.generate_problems()
        symbol = WorksheetConfig.OPERATIONS[self.config.operation]
        
        pdf = MathWorksheetPDF(student_name, self.config.operation)
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        num_cols = 5
        for i, (a, b) in enumerate(problems):
            x = 10 + (i % num_cols) * WorksheetConfig.COL_SPACING
            y = 30 + ((i // num_cols) % 6) * WorksheetConfig.ROW_SPACING
            
            # Add new page if needed
            if i > 0 and i % WorksheetConfig.PROBLEMS_PER_PAGE == 0:
                pdf.add_page()
                
            pdf.add_problem(x, y, a, b, symbol)

        output_filename = f'{student_name}_{self.config.operation}_worksheet_{datetime.now():%Y%m%d_%H%M%S}.pdf'
        pdf.output(output_filename)
        return output_filename

def get_user_input() -> WorksheetGenerator:
    """Get user input and configure worksheet generator"""
    generator = WorksheetGenerator()
    
    # Get number range
    while True:
        try:
            generator.config.lowest_num = int(input("Enter the lowest number (default: 0): ") or "0")
            generator.config.highest_num = int(input("Enter the highest number (default: 10): ") or "10")
            if generator.config.lowest_num <= generator.config.highest_num:
                break
            print("Lowest number must be less than or equal to highest number.")
        except ValueError:
            print("Please enter valid numbers.")

    # Get operation type
    while True:
        print("\nAvailable operations:")
        for op in WorksheetConfig.OPERATIONS:
            print(f"- {op}")
        operation = input("\nEnter operation type: ").lower()
        if operation in WorksheetConfig.OPERATIONS:
            generator.config.operation = operation
            break
        print("Invalid operation. Please choose from the list above.")

    # Get times table preference for multiplication/division
    if operation in ["multiplication", "division"]:
        if input("Do you want to focus on a specific times table? (yes/no): ").lower() == "yes":
            while True:
                try:
                    generator.config.times_table = int(input("Enter the times table number: "))
                    if generator.config.times_table != 0:
                        break
                    print("Times table cannot be zero.")
                except ValueError:
                    print("Please enter a valid number.")

    # Get number of problems
    while True:
        try:
            num_input = input(f"Enter number of problems (default: {WorksheetConfig.DEFAULT_NUM_PROBLEMS}): ")
            generator.config.num_problems = int(num_input) if num_input else WorksheetConfig.DEFAULT_NUM_PROBLEMS
            
            num_pages = (generator.config.num_problems + WorksheetConfig.PROBLEMS_PER_PAGE - 1) // WorksheetConfig.PROBLEMS_PER_PAGE
            if num_pages > 2:
                print(f"Warning: This will create {num_pages} pages. Maximum recommended is 2 pages (60 problems).")
                if input("Continue? (yes/no): ").lower() != "yes":
                    continue
            break
        except ValueError:
            print("Please enter a valid number.")

    return generator

def main():
    """Main program entry point"""
    print("Math Worksheet Generator")
    print("=======================")
    
    # Ask about batch processing
    batch_mode = input("Generate worksheets for multiple students? (yes/no): ").lower() == "yes"
    
    generator = get_user_input()
    
    if batch_mode:
        while True:
            file_path = input("Enter path to student names file (one name per line): ")
            if Path(file_path).is_file():
                try:
                    with open(file_path, 'r') as f:
                        student_names = [line.strip() for line in f if line.strip()]
                    break
                except Exception as e:
                    print(f"Error reading file: {e}")
            print("File not found. Please try again.")
        
        print("\nGenerating worksheets...")
        for name in student_names:
            filename = generator.create_worksheet(name)
            print(f"Created worksheet for {name}: {filename}")
    else:
        student_name = input("Enter student name: ")
        filename = generator.create_worksheet(student_name)
        print(f"\nCreated worksheet: {filename}")

if __name__ == "__main__":
    main()