import sqlite3

def initiate_db():
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    
    cur.executescript(""" CREATE TABLE IF NOT EXISTS USER

    (CPM INT PRIMARY KEY NOT NULL,
     MC  INT  NOT NULL,
     NIC VHARCHAR(15) NOT NULL,
     NAME VARCHAR(255),
     DOB TEXT(10),
     EMAIL VARCHAR(255),
     PHONE TEXT(10) 
    )   

    """)
    print("--- Database initation success! ---")

    cur.executescript(""" CREATE TABLE IF NOT EXISTS auth_dd(
                    cpm, auth1, auth2
                     ) 
    """)
    return con, cur

def insert_data(cpm, mc, nic, name, dob, email, phone):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        query = "INSERT INTO USER (CPM, MC, NIC, NAME, DOB, EMAIL, PHONE) VALUES(?,?,?,?,?,?,?)"
        data = [cpm, mc, nic, name, dob, email, phone]
        cur.execute(query,data)
        con.commit()
        print("--- Data Row instered Sucessfully ---")

    except Exception as e:
        print(e)

def insert_data_requests(cpm, mc, nic, name, dob, email, phone, type,remarks=None,reason=None, summary=None,
                         university=None, degree=None, year=None, other_details=None ):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        if type == "to_whome_it":
            query = "INSERT INTO REQUESTS (CPM, MC, NIC, NAME, DOB, EMAIL, PHONE, TYPE, REMARKS) VALUES(?,?,?,?,?,?,?,?,?)"
            data = [cpm, mc, nic, name, dob, email, phone, type, remarks]
            cur.execute(query,data)

        if type == "reference":
            query = "INSERT INTO REQUESTS (CPM, MC, NIC, NAME, DOB, EMAIL, PHONE, TYPE, university, degree, year, other_details) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
            data = [cpm, mc, nic, name, dob, email, phone, type, university, degree, year, other_details]
            cur.execute(query,data)

        if type == "other":
            query = "INSERT INTO REQUESTS (CPM, MC, NIC, NAME, DOB, EMAIL, PHONE, TYPE, reason, summary) VALUES(?,?,?,?,?,?,?,?,?,?)"
            data = [cpm, mc, nic, name, dob, email, phone, type, reason, summary]
            cur.execute(query,data)

        con.commit()
        print("--- Data Row instered Sucessfully ---")

    except Exception as e:
        print(e)        


def fetch_data(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM USER WHERE CPM=? "#AND MC=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e)

def fetch_data_requests(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM REQUESTS WHERE CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e)


def send_to_db_auth1(cpm, auth1):
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()
    try:
        query = "INSERT INTO auth_dd (cpm, auth1) VALUES(?,?)"    
        data = [cpm, auth1]
        cur.execute(query, data)
        con.commit()
        return True
    except Exception as e:
        print(e)

            
def send_to_db_auth2(cpm, auth2):
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()
    try:
        query = "UPDATE auth_dd SET auth2=? WHERE CPM=?"
        data = [auth2,cpm]
        cur.execute(query,data)
        con.commit()
        print(cpm, auth2, "sucessfully inserted the second data")
        return True
    except Exception as e:
        print(e)


def fetch_auth_data(cpm):
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()
    try:
        query = "SELECT * FROM auth_dd WHERE cpm=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    except Exception as e:
        print(e)



        
    


if __name__ == "__main__":
    initiate_db()
    cpm = int(input("Please input the cpm :"))
    mc  = int(input("please input the MC :"))
    nic = input("Please input the nic")
    name = input("Please input the name :")
    dob = input("Please input the DOB :")
    email = input("Please input the email :")
    phone = input("Please input the phone :")        

    insert_data(cpm,mc,nic,name,dob,email,phone)

    out = fetch_data(cpm)
    if not out:
        print("yeah")
    else:
        print(out)    
        