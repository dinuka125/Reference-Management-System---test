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

def create_table_l_to_whome():
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    cur.executescrip


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


#======================================================================= Request data base functions 

def insert_data_L_to_whome(positions, contributions, summary, cpm):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        query = "INSERT INTO L_to_whome (POSITIONS, CONTRIBUTIONS, SUMMARY, CPM) VALUES(?,?,?,?)"
        data = [positions, contributions, summary, cpm]
        cur.execute(query, data)
        con.commit()

    except Exception as e:
        print(e)

def insert_data_L_higher_studies(university, degree, year, other_details, cpm):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        query = "INSERT INTO L_higher_studies (UNIVERSITY, DEGREE, YEAR, OTHER_DETAILS, CPM) VALUES(?,?,?,?,?)"
        data = [university, degree, year, other_details, cpm]
        cur.execute(query, data)
        con.commit()

    except Exception as e:
        print(e)


def insert_ref_emp(company, job, activities_at_uni,cpm):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        query = "INSERT INTO L_ref_emp (COMPANY, JOB_TITLE, ACTIVITIES_AT_UNI , CPM) VALUES(?,?,?,?)"
        data = [company, job, activities_at_uni,cpm]
        cur.execute(query, data)
        con.commit()

    except Exception as e:
        print(e)        

def insert_data_L_visa(country, reason, activities_at_uni, cpm):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        query = "INSERT INTO L_VISA (COUNTRY, REASON, ACTIVITIES, CPM) VALUES(?,?,?,?)"
        data = [country, reason, activities_at_uni, cpm]
        cur.execute(query, data)
        con.commit()

    except Exception as e:
        print(e)    

def insert_data_L_other(reason, summary, cpm):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        query = "INSERT INTO L_OTHER (REASON, SUMMARY, CPM) VALUES(?,?,?)"
        data = [reason, summary, cpm]
        cur.execute(query, data)
        con.commit()

    except Exception as e:
        print(e)    


#====================================================================== Request data base functions ends here

def get_user_data(cpm):
    try:
        con = sqlite3.connect("ref_database.db")
        cur = con.cursor()
        query = "SELECT * FROM USER WHERE CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out 
        
    except Exception as e:
        print(e)    


def fetch_data(cpm, mc, nic):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM USER WHERE CPM=? AND MC=? AND NIC=?"
        data = [cpm, mc, nic]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e)

def fetch_data_2(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM USER WHERE CPM=?"
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

####====================================================== DATA Retreival Functions for seprate type of letters ======================

def fetch_data_requests_to_whome_it(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM L_TO_WHOME WHERE CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e)        

def fetch_data_requests_higher_studies(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM L_higher_studies WHERE CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e)                


def fetch_data_requests_ref_emp(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM L_ref_emp WHERE CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e)    


def fetch_data_requests_L_visa(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM L_VISA WHERE CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e)       


def fetch_data_requests_other(cpm):        
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()

    try:
        query = "SELECT * FROM L_OTHER CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    
    except Exception as e:
        print(e) 

#==============================================================================================================================                          

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

def fetch_auto(cpm):
    con = sqlite3.connect("ref_database.db")
    cur = con.cursor()
    try:
        query = "SELECT * FROM L_VISA WHERE CPM=?"
        data = [cpm]
        cur.execute(query,data)
        out = cur.fetchall()
        return out
    except Exception as e:
        print(e)


        
    


if __name__ == "__main__":
    initiate_db()
    # cpm = int(input("Please input the cpm :"))
    # mc  = int(input("please input the MC :"))
    # nic = input("Please input the nic")
    # name = input("Please input the name :")
    # dob = input("Please input the DOB :")
    # email = input("Please input the email :")
    # phone = input("Please input the phone :")        

    # insert_data(cpm,mc,nic,name,dob,email,phone)

    # out = fetch_data(17774,87548,"963320558V")
    # if not out:
    #     print("yeah")
    # else:
    #     print(out)    
    
    # insert_data_L_visa("USA", "work visa", "comittee member", 17521)
    # out = fetch_auto(17521)
    # print(out)
        
    out = get_user_data(17779)    
    print(out[0][3])