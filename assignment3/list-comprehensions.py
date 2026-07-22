import csv

with open("../csv/employees.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)
print(rows[0])
names = [row[1] + " " + row[2] for row in rows[1:]]
print(f"Names: {names}")
names_with_e = [name for name in names if "e" in name]
print(f"Names with e: {names_with_e}")