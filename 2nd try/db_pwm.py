import sqlite3
from sqlite3 import Error


def query(sql_command, dbfile, params = None):
    # """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(dbfile)
        cursor = conn.cursor()
        
        if params:
            cursor.execute(sql_command, params)
        else:
            cursor.execute(sql_command)
            
            
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
            
def update_pw(new_hashed_pw):
    params = (new_hashed_pw,)
    sql_command = """UPDATE users SET userhashedpassword = ? WHERE usernum = 1;"""    
    query(sql_command, "users.db", params)


            
class db_users():
    def __init__(self):
        sql_command = """
            CREATE TABLE IF NOT EXISTS users ( 
            usernum INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            userhashedpassword VARCHAR(50),
            salt VARCHAR(50));"""
            
        query(sql_command, "users.db")
            
        
                
    def add_user(self, hashedpassword, salt):
        # sql_command = f"INSERT INTO users (username, userhashedpassword, salt)\
        #     VALUES ({username}, {hashedpassword}, {salt});"
        
        param = (hashedpassword, salt)
        sql_command = "INSERT INTO users VALUES (NULL, ?, ?)"
            
        query(sql_command, "users.db", params=param)
    
                
    # def remove_user(self, username, hashedpassword, salt):
    #     sql_command = "DELETE FROM users WHERE username = ? AND userhashedpassword = ? AND salt = ?;"
    #     param = (username, hashedpassword, salt)        
    #     query(sql_command, "users.db", param)
    
    def see_all(self):
        sql_command = "SELECT * FROM users;"
        
        users = []
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            
            cursor.execute(sql_command)
            
            rows = cursor.fetchall()
            
            for row in rows:
                users.append(row)
                print(row)
                
            conn.commit()
    
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
        
        return users



class db_acc():
    def __init__(self):
        # potentially better to make username a class var, than calling the whole time username
        
        sql_command = """
            CREATE TABLE IF NOT EXISTS accounts ( 
            acc_num INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
            acc_name VARCHAR(50), 
            acc_username VARCHAR(50), 
            acc_email VARCHAR(30), 
            acc_password VARCHAR(50),
            acc_url VARCHAR(50) DEFAULT NULL);"""
            
        query(sql_command, "accs.db")
    
    def add_acc(self, acc_name, acc_username, email, password, url=None):
        
        if url:
            params = (acc_name, acc_username, email, password, url)
            sql_command = "INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?, ?);"
        else:
            params = (acc_name, acc_username, email, password)
            sql_command = "INSERT INTO accounts VALUES (NULL, ?, ?, ?, ?, NULL);"
            
        query(sql_command, "accs.db", params)
        
        
    def remove_acc(self, acc_name, acc_username, email, password):
        params= (acc_name, acc_username, email, password)
        sql_command = "DELETE FROM accounts WHERE acc_name = ? AND acc_username = ? AND acc_email = ? AND acc_password = ? ;"
        
        query(sql_command, "accs.db", params)
        
    def see_all(self):
        sql_command = "SELECT * FROM accounts"
        accs = []
        conn = None
        try:
            conn = sqlite3.connect("accs.db")
            cursor = conn.cursor()
            
            cursor.execute(sql_command)
            
            rows = cursor.fetchall()
            
            for row in rows:
                accs.append(row)
                print(row)
                
            conn.commit()
    
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
        
        return accs
        

    
    
if __name__=="__main__":    
    # init_users_db()
    # add_user("nbex", "abc", "123")
    # remove_user("nbex", "abc", "123")
    # init_acc_db("Nex")
    # add_acc("Nex", "fb", "Nex", "bla@bla.com", "Penis", "fb.com")
    # remove_acc("Nex", "fb", "Nex", "bla@bla.com", "Penis")
    
    
    
    
    users = db_users()
    users.add_user("lol", "123")

    userss = users.see_all()
    
    for a in userss:
        print(a[0])
    
    
    
    
    
    
    