from datetime import datetime
import csv
import custom_module
import os
import traceback


# Task 2: Read a CSV File
def read_employees():

    employees = {}
    rows = []

    with open("../csv/employees.csv", "r") as file:

        reader = csv.reader(file)
        first_row = True
        for row in reader:
            if first_row:
                employees["fields"] = row
                first_row = False
            else:
                rows.append(row)

        
    employees["rows"] = rows
    return employees

# Task 3: Find the Column Index
def column_index(column_name):
    return employees["fields"].index(column_name)

# Task 4: Find the Employee First Name
def first_name(row_number):

    first_name_column = column_index("first_name")
    row = employees["rows"][row_number]
    return row[first_name_column]

# Task 5: Find the Employee: a Function in a Function
def employee_find(employee_id):

    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches = list(filter(employee_match, employees["rows"]))
    return matches

# Task 6: Find the Employee with a Lambda

def employee_find_2(employee_id):

    matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
    return matches

#Task 7: Sort the Rows by last_name Using a Lambda
def sort_by_last_name():
    last_name_column = column_index("last_name")
    employees["rows"].sort(key = lambda row: row[last_name_column])
    return employees["rows"]

#Task 8: Create a dict for an Employee
def employee_dict(row):
    result = {}

    for field in employees["fields"]:
        if field != "employee_id":
            result[field] = row[column_index(field)]
    
    return result
#Task 9: A dict of dicts, for All Employees
def all_employees_dict():
    result = {}
    for row in employees["rows"]:
        emp_id = row[employee_id_column]
        result[emp_id] = employee_dict(row)
    return result

# Task 10: Use the os Module
def get_this_value():

    return os.getenv("THISVALUE")


# Task 11: Creating Your Own Module
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


#Task 12: Read minutes1.csv and minutes2.csv
def read_csv_helper(path):
    result = {}
    rows = []

    with open(path, 'r') as file:
        reader = csv.reader(file)
        first_row = True
        for row in reader:
            if first_row:
                result["fields"] = row
                first_row = False
            else:
                rows.append(tuple(row))

    result["rows"] = rows
    return result

#Task 12: Read minutes1.csv and minutes2.csv
def read_minutes():
    minutes1 = read_csv_helper('../csv/minutes1.csv')
    minutes2 = read_csv_helper('../csv/minutes2.csv')
    return minutes1, minutes2

# Task 13: Create minutes_set
def create_minutes_set():
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    combined = set1.union(set2)
    return combined

# Task 14: Convert to datetime
def create_minutes_list():
    minutes_list_raw = list(minutes_set)
    minutes_list = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list_raw))
    return minutes_list

# Task 15: Write Out Sorted List
def write_sorted_list():
    minutes_list.sort(key=lambda x: x[1])

    converted_list = list(map(lambda x: (x[0], x[1].strftime("%B %d, %Y")), minutes_list))

    with open('./minutes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(minutes1["fields"])
        for row in converted_list:
            writer.writerow(row)

    return converted_list

employees = None
employee_id_column = None
minutes1 = None
minutes2 = None
minutes_set = None
minutes_list = None

try:
    employees = read_employees()
    print(employees)
    employee_id_column = column_index("employee_id")
    sort_by_last_name()
    print(employees)
    print(employee_dict(employees["rows"][0]))
    print(all_employees_dict())
    set_that_secret("Esin!3")
    print(custom_module.secret)
    minutes1, minutes2 = read_minutes()
    print(minutes1)
    print(minutes2)
    minutes_set = create_minutes_set()
    print(minutes_set)
    minutes_list = create_minutes_list()
    print(minutes_list)
    sorted_minutes = write_sorted_list()
    print(sorted_minutes)

except Exception as e:

    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()

    for trace in trace_back:
        stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    print("An exception occurred.")

    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")

    print(f"Stack trace: {stack_trace}")


