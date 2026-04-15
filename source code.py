import mysql.connector
import datetime
import csv
import random
# Establish the connection
connection = mysql.connector.connect(
            host="localhost",
            user="root", #Enter your user name
            password="YOUR_PASSWORD", #Enter your password 
            database="Insurance_Company"
        )
        
cursor = connection.cursor()

def party_code(type_of_insurance,year):
    #NP=family floater,TU=Top up,UK=New med claim
    #SH=Shopkeeper,MI=money insurance,BI=burgalry
    branch_no="67200"
    if type_of_insurance in ["TW",'PC','CV']:
        product_code="31" #motor
    if type_of_insurance in ['NP','TU','UK']:
        product_code="34" #health
    if type_of_insurance in ['FS']:#fire insurance
        product_code="11"
    if type_of_insurance in ['SH','MI','BI']:
        product_code="46" #miscellanous
    if type_of_insurance in ["PU"]:
        product_code="42"# personal accident
    random_no = random.randint(10000000, 99999999)
    party_code=branch_no+product_code+str(year)+str(random_no)
    with open("party_code.txt","r+") as file:
        content=file.read()
        if product_code not in content:
            return int(party_code)
            file.write(party_code)
        else:
            
            party_code(type_of_insurance,year)

def password_checking():
    password="Enter your password" #Enter your password
    pwd=input("Enter the password:")
    if pwd==password:
       underwriter()
    else:
        print("Access Denied")

def name_from_database(party_code):
    tuple=(party_code,)
    query = "SELECT Name FROM Customer_Details WHERE party_code = %s"
    cursor.execute(query,tuple)
    result = cursor.fetchone()
    if result:
        name=result[0]
        return name
    else:
         return None


def customer():
    party_code=input("Enter your party code:")
    Name=name_from_database(party_code)
    if Name == None:
        print("Party Code doesn't exist")
    else:
        print("Welcome",Name)
        print("""
            What would you what to do?
            1.View your details
            2.Request for change of your details""")
        choice=int(input("Enter your choice:"))
        if choice==1:
            cursor.execute("SELECT * FROM Customer_Details WHERE party_code ="+party_code)
            result=cursor.fetchall()
            for detail in result:
                print("Party_Code:",detail[0])
                print("Name:",detail[1])
                print("Phone no.:",detail[2])
                print("Address:",detail[3])
                print("Type of Insurance:",detail[4])
                print("Email:",detail[5])
                print("Pincode:",detail[6])
                print("Starting date of insurance:",detail[7])
                print("Ending date of insurance:",detail[8])
                
            
            
        elif choice==2:
            print("""Details and Deatails' Number
                  1.Name
                  2.Phone no.
                  3.Address
                  4.Type of Insurance
                  5.Email
                  6.Pincode
                  7.Starting date of insurance
                  8.Ending date of insurance""")
                  
            while True:
                with open("Requests.csv","a") as file:
                    detail=input("Enter the detail number:")
                    value=input("Enter the new value:")
                    csvwriter=csv.writer(file)
                    list=[party_code,detailno,value]
                    csvwriter.writerow(list)
                    ch=input("Do you want request to change another details(y/n):")
                    if ch.lower()=='n':
                        print("Your request has been sucessfully submitted")  
                        break
def data_from_user():
    while True:
        Name=input("Enter your name (max.25 characters):")
        if len(Name)<26:
            break
        print("Name should have maximum 25 characters")
        
    while True:
        phno=input("Enter your phone number:")
        if len(phno)==10 and phno.isdigit():
            break
        print("A phone no. should contains 10 digits")
        
    while True:
        address=input("Enter your address(City)(max.50 characters):")
        if len(address) <=50:
            break
        print("Address should have maximum 25 characters")
        

    while True:
        Type_of_insurance=input("Enter the type of insurance:")
        if Type_of_insurance in ["TW",'PC','CV','NP','TU','UK','SH','MI','BI','PU','FS']:
            break
        print("Enter the correct type of insurance")
        

    email=input("Enter the your email:")

    while True:
        pincode=int(input("Enter the pincode:"))
        if pincode >100000 and pincode<1000000:
            break
        print("Enter correct pincode")
    
    while True:
        date_start=input("Enter the starting date of insurance formatted as YYYY-MM-DD:").split('-')
        yr,mn,dt=date_start
        date_end=input("Enter the ending date of insurance formatted as YYYY-MM-DD:").split('-')
        year,month,date=date_end
        start_date=datetime.date(int(yr),int(month),int(date))
        end_date=datetime.date(int(year),int(month),int(date))
        yr=int(yr)//100
        pc=party_code(Type_of_insurance,yr)
        return pc,Name,phno,address,Type_of_insurance,email,pincode,start_date,end_date
        
        
def add(data):
    query = "INSERT INTO Customer_Details VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(query,data)

def upadating_the_policy():
    with open("Requests.csv","r+") as file:
        csvreader=csv.reader(file)
        for row in csvreader:
            if len(row)==0:
                continue
            pc,no,value=row
            tuple=(value,pc)
            if no==1:
                query = 'UPDATE Customer_Details SET Name=%s WHERE party_code=%s'
            elif no==2:
                query = 'UPDATE Customer_Details SET Phone_no=%s WHERE party_code=%s'
            elif no==3:
                query = 'UPDATE Customer_Details SET Address=%s WHERE party_code=%s'
            elif no==4:
                query = 'UPDATE Customer_Details SET Type_of_Insurance=%s WHERE party_code=%s'
            elif no==5:
                query = 'UPDATE Customer_Details SET Email=%s WHERE party_code=%s'
            elif no==6:
                query = 'UPDATE Customer_Details SET Pincode=%s WHERE party_code=%s'
            elif no==7:
                query = 'UPDATE Customer_Details SET Policy_Start_Date=%s WHERE party_code=%s'
            elif no==8:
                query = 'UPDATE Customer_Details SET Policy_End_Date=%s WHERE party_code=%s'
            else:
                continue
            cursor.execute(query,tuple)
        file.truncate()

def canceling_a_policy():
    party_code = int(input("Enter the party_code:")) 
    query = f'''SELECT * FROM Customer_Details
        WHERE party_code = {party_code};'''
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        query = f'''DELETE FROM Customer_Details
            WHERE party_code = {party_code};'''
        cursor.execute(query)
        print(f"Policy with has been canceled sucessfully...")
    else:
        print(f"No policy found with party_code {party_code}.")
        
def renew_a_policy():
    party_code=int(input("Enter the party code:"))
    query =f'''UPDATE Customer_Details SET Policy_Start_Date = DATE_ADD(Policy_Start_date, INTERVAL 1 YEAR),
    Policy_End_Date = DATE_ADD(Policy_End_date, INTERVAL 1 YEAR)WHERE party_code={party_code};'''
    cursor.execute(query)

def display_policies():
    
    query=cursor.execute("SELECT * FROM Customer_Details")
    result=cursor.fetchall()
    list=["Party_Code","Name:","Phone no.:","City:",
          "Type of Insurance:","Address:","Pincode:","Starting date of insurance:","Ending date of insurance:"]
    for tuple in result:
        for i in range(len(tuple)):
            print(list[i],tuple[i])
            
def view_request():
    with open("Requests.csv") as file:
        csvreader=csv.reader(file)
        for row in csvreader:
            if len(row)==0:
                continue
            print(row)
            
def underwriter():
    print('-'*90)
    print("""
            What would you like to do?
            1.Add a new policy
            2.Update the policy
            3.Cancel a policy
            4.Renew a policy
            5.Display policies
            6.View request changes from customers
            7.Exit""")
    while True:
        choice=int(input("Enter the your choose:"))
        if str(choice) not in '12345678':
            print("Enter a valid choose")
        elif choice==1:
            data=data_from_user()
            add(data)
            print("Policy added successfully....")
        elif choice==2:
            upadating_the_policy()
            print("Policy upadated successfully...")
        elif choice==3:
            canceling_a_policy()
        elif choice==4:
            renew_a_policy()
            print("Policy renewed successfully...")
        elif choice==5:
            display_policies()
        elif choice==6:
             view_request()   
        else:
            print("Task Completed")
            print('-'*90)
            break

print(' '*30,"Welcome",' '*30)
print("Choose an option")
print("""
1.Customer
2.Underwriter""")
while True:
    choice=input("Enter the your choice:")
    if choice not in "12":
        continue
    if choice =="1":
        customer()
        break
    elif choice=="2":
        password_checking()
        break




 
