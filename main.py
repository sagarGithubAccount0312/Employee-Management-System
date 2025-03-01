import sqlite3
import re

def menu():
    print("Welcome to Employee Management System")
    print("Press ")
    print("1 to Add Employee")
    print("2 to Remove Employee")
    print("3 to Promote Employee")
    print("4 to Display Employees")
    print("5 to Display all employees")
    print("6 to Exit")
 
    ch = input("Enter your Choice: ")
    if ch == '1':
        Add_Employ()
    elif ch == '2':
        Remove_Employ()
    elif ch == '3':
        Promote_Employee()
    elif ch == '4':
        Display_Employees()
    elif ch == '5':
         Display_All_Employees()
    elif ch == '6':
        exit(0)
    else:
        print("Invalid Choice")
        menu()


def create_connection():
    try:
        conn = sqlite3.connect("empDataBase.db")
    except Exception as e:
            print("Error in database ",e)

    return conn


def Add_Employ():

 
    while True:
        Name = input("Enter Employee Name : ").strip()
        checkName = Name.replace(" ", "").isalpha()
    
        if not checkName:
            print("---->Please enter alphabates only")
        else:
            break
    while True:

        Post = input("Enter Employee Post : ").strip()
        checkPost = re.match(r"[a-zA-Z0-9]+", Post)
        
        if not checkPost:
             print("---->Please fill post")
        else:
            break


    while True:
        Salary = input("Enter Employee Salary(per annum) : ").strip()
        checkSalary = Salary.isnumeric()
        if not checkSalary:
            print("---->Please enter numeric value only")
        else:
            break

    data = (Name, Post, Salary)

    sql = 'INSERT INTO EMS (NAME,POST,SALARY) VALUES(?,?,?)'

    conn = create_connection()
    c = conn.cursor()
    c.execute(sql, data)
        
    conn.commit()
    print("\nEmployee Added Successfully\n")
    menu()
        


def check_employee(employee_id):
     
  
    Checksql = f'SELECT * FROM EMS WHERE ID = "{employee_id}"'
     
    conn = create_connection()
    c = conn.cursor()
    c.execute(Checksql)
    r = c.fetchone()

    if r != None:
        
        return True, r
    else:
        return False, r


def Remove_Employ():

    Id = input("Enter Employee Id : ")
    if Id.isnumeric():

        if(check_employee(Id)[0] == False):
            print("\nEmployee does not  exists\nTry Again\n")
        
        else:
                
            sql = f'DELETE FROM EMS WHERE ID="{Id}"'
            con = create_connection()
            c = con.cursor()
            c.execute(sql)
            con.commit()
            print("\nEmployee Removed\n")
    else:
        print("\nPlease enter numeric value\n")
        Remove_Employ()
    menu()       
     
def Promote_Employee():
     print("\nBuild in progress!\m")
     menu()
def Display_Employees():
     
     emId = input("Employee id: ")
     if emId.isnumeric():
        data = check_employee(emId)[1]

        if data:
            print("\nEmployee Name : ", data[1])
            print("Employee Post : ", data[2])
            print("Employee Salary : ", data[3], "per annum")
            print("--------------------------------------")
        else:
            print("\n**No record found**\n")
     else:
         Display_Employees()
         print("\nPlease enter numeric value\n")

     menu()

def Display_All_Employees():

    sql = 'SELECT * FROM EMS'
    conn = create_connection()
    c = conn.cursor()
    c.execute(sql)
    r = c.fetchall()
   
    print("\nTotal Record: ",len(r))

    if len(r):
        print("--------------------------------------")
        for i in r:
            print("Employee Id : ", i[0])
            print("Employee Name : ", i[1])
            print("Employee Post : ", i[2])
            print("Employee Salary : ", i[3], "per annum")
            print("--------------------------------------")
    else:
         print("**No record found**")         
    menu()


menu()