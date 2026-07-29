import pandas as pd
# Task 1: Create a DataFrame from a dictionary:
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)
print(task1_data_frame)

# Task 1: Add a new column:
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]
print(task1_with_salary)

# Task 1: Modify an existing column:
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1
print(task1_older)

# Task 1: Save the DataFrame as a CSV file:
task1_older.to_csv('employees.csv', index=False)

# Task 2: Read data from a CSV file:
task2_employees = pd.read_csv('employees.csv')
print(task2_employees)

# Task 2: Read data from a JSON file:
json_employees = pd.read_json('additional_employees.json')
print(json_employees)

# Task 2: Combine DataFrames:
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)
print(more_employees)

# Task 3: Use the head() method:
first_three = more_employees.head(3)
print(first_three)

# Task 3: Use the head() method:
last_two = more_employees.tail(2)
print(last_two)

# Task 3: Get the shape of a DataFrame
employee_shape = more_employees.shape
print(employee_shape)

# Task 3: Use the info() method:
more_employees.info()

# Task 4: Create a DataFrame from dirty_data.csv file and assign it to the variable dirty_data
dirty_data = pd.read_csv('dirty_data.csv')
print(dirty_data)

clean_data = dirty_data.copy()

# Task 4: Remove any duplicate rows from the DataFrame
clean_data = clean_data.drop_duplicates().reset_index(drop=True)
print(clean_data)

# Task 4: Convert Age to numeric and handle missing values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')
print(clean_data)

# Task 4: Convert Salary to numeric and replace known placeholders (unknown, n/a) with NaN
clean_data['Salary'] = clean_data['Salary'].replace(['unknown', 'n/a'], pd.NA)
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')
print(clean_data)

# Task 4: Fill missing numeric values (use fillna).  Fill Age with the mean and Salary with the median
clean_data['Age'] = clean_data['Age'].fillna(clean_data['Age'].mean())
clean_data['Salary'] = clean_data['Salary'].fillna(clean_data['Salary'].median())
print(clean_data)

# Task 4: Convert Hire Date to datetime
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'], format='mixed', errors='coerce')
print(clean_data)

# Task 4: Strip extra whitespace and standardize Name and Department as uppercase
clean_data['Name'] = clean_data['Name'].str.strip()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()
print(clean_data)