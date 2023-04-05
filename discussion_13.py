import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    table = """ CREATE TABLE IF NOT EXISTS employees (
                employee_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                job_id INTEGER,
                hire_date TEXT,
                salary NUMERIC
                )"""
    
    cur.execute(table)
    conn.commit()
    return

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()  
    # THE REST IS UP TO YOU
    emp_list = json.loads(file_data)
    for dicts in emp_list:
        e_id = dicts["employee_id"]
        f_name = dicts["first_name"]
        l_name = dicts["last_name"]
        h_date = dicts["hire_date"]
        j_id = dicts["job_id"]
        sal = dicts["salary"]
        cur.execute("""INSERT OR IGNORE INTO employees 
                       (employee_id, first_name, last_name, job_id, hire_date, salary)
                       VALUES (?, ?, ?, ?, ?, ?)""", (e_id, f_name, l_name, j_id, h_date, sal))
    conn.commit()
    return

# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute(""" Select Employees.hire_date, Jobs.job_title
                    FROM Employees JOIN Jobs
                    ON Employees.job_id = Jobs.job_id
                    """)
    results = cur.fetchall()
    title = results[0][1]
    return title

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute(""" SELECT Employees.first_name, Employees.last_name
                    FROM Employees JOIN Jobs
                    ON Jobs.job_id = Employees.job_id
                    WHERE Employees.salary < Jobs.min_salary OR Employees.salary > Jobs.max_salary
                """)
    results = cur.fetchall()
    tup_list = []
    for result in results:
        tup_list.append(result)
    return tup_list

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    cur.execute(""" SELECT Jobs.job_title, Employees.salary
                    FROM Jobs JOIN Employees
                    ON Jobs.job_id = Employees.job_id
                """)
    results = cur.fetchall()
    x = []
    y = []
    for result in results:
        x.append(result[0])
        y.append(result[1])
    
    plt.scatter(x, y)

    cur.execute(""" SELECT Jobs.job_title, Jobs.min_salary, Jobs.max_salary FROM Jobs""")
    results = cur.fetchall()
    print(results)
    x = []
    y = []
    for result in results:
        x.append(result[0])
        y.append(result[1])
    plt.scatter(x, y, color='red', marker='x')
    for result in results:
        x.append(result[0])
        y.append(result[2])
    plt.scatter(x, y, color='red', marker='x')

    plt.show()
    return


class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

    visualization_salary_data(cur, conn)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

