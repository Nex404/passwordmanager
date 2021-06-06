#defining classes for users and accounts

import os
import db_pwm as db
import cryptography_pwm as crypto


class user():
    #constructor
    #Note: has to be encrypted before using
    def __init__(self, username, hashedpassword, salt, password=None):
        self.username = username
        self.salt = salt
        self.hashed_password = hashedpassword #crypto.hasher(password, self.salt)
        self.password = password
        self.accounts = []
        self.db_accounts = db.db_acc(self.username)

        
    def add_acc(self, account):
        if self.password:
            self.accounts.append(account)
            self.decrypt()
            self.db_accounts.add_acc(self.username, account.acc_name, account.username, account.email, account.password, account.url)
            self.encrypt()
        else:
            print("No password:add_acc")
        
    def remove_acc(self, account_name):
        if self.password:
            # get index
            accname = ""
            index = 0
            for acc in self.accounts:
                if acc.acc_name == account_name:
                    accname = account_name
                    break
                index += 1
                
            acc = self.accounts[index]
            

            if index < len(self.accounts):
                self.accounts.pop(index)
                print(f"Account {accname} got deleted.")
            
                self.decrypt()
                self.db_accounts.remove_acc(self.username, acc.acc_name, acc.username, acc.email, acc.password)
                self.encrypt()    
            else:
                print("no account found for this acc name")
        else:
            print("No Password:remove_acc")
            
    def edit_acc(self, index, new_account):
        
        acc = self.accounts[index]
        # edit acc
        self.accounts[index] = new_account
        acc_new = self.accounts[index]
        
        # decrypt
        self.decrypt()
        
        # edit db
        self.db_accounts.update_acc(self.username, acc.acc_name, acc.username, acc_new.acc_name, acc_new.username, acc_new.email, acc_new.password, acc_new.url)
        
        
        # encrypt
        self.encrypt()
        
        pass
        
    def change_master_pw(self, new_password):
        if self.password:  
            #handeling acc db
            print("befor changing")
            print(self.hashed_password)
            
            self.decrypt()
            self.hashed_password = crypto.hasher(new_password, self.salt)
            self.password = new_password
            self.encrypt()
            
            # update hashed password in users db
            print("after changing")
            print(self.username, self.hashed_password)
            db.update_pw(self.username, self.hashed_password)
            print("after db change")
            
            print("masterpassword changed")
        else:
            print("no password:change_master_pw")
            
    def encrypt(self):
        if self.password:
            crypto.encrypter(self.password, self.salt, f"{self.username}.db")
        else:
            print("No Password:encrypt")
        
    def decrypt(self):
        if self.password:
            crypto.decrypter(self.password, self.salt, f"{self.username}.db")
        else:
            print("No Password:decrypt")
        
    #debug method
    def print_user(self):
        print(f"I'm {self.username} and have {self.hashed_password} as pw. the salt is {self.salt}")
        
    def print_accs(self):
        if len(self.accounts) > 0:
            for acc in self.accounts:
                print(acc.username + " " + acc.password)
        else:
            print("Accounts are empty:print_accs")




class users():
    def __init__(self):
        self.db_users = db.db_users()
        self.users = []
        
        
    def load_users(self):
        # load all accounts into users
        users = self.db_users.see_all() # 
          
        # create a user for each tupel in users
        for u in users:
            username = u[1]
            hashed_pw = u[2]
            salt = u[3]
            
            userr = user(username, hashed_pw, salt)
            
            self.users.append(userr)
                  
    
    def add_user(self, user):
        #check that double acc names are not allowed
        for u in self.users:
            if u.username == user.username:
                print("Accountname already exists. Try another name.")
                return

        self.users.append(user)
        self.db_users.add_user(user.username, user.hashed_password, user.salt)
        
    def remove_user(self, user, confirm_password):
        if user.hashed_password == crypto.hasher(confirm_password, user.salt):
            self.db_users.remove_user(user.username, user.hashed_password, user.salt)
            self.users.remove(user)
            print("User got removed.")
            
        else:
            print("No such user or incorrect password.")
            
            
    def see_users(self):
        for u in self.users:
            print(u.username)
        
        
        
    
class account():
    #constructor
    def __init__(self, account_name, username, email, password, url=None):
        self.acc_name = account_name
        self.username = username
        self.email = email
        self.password = password
        self.url = url
    
    def edit_acc(self, new_acc_name, new_user_name, new_email, new_password, new_url):
        self.acc_name = new_acc_name
        self.username = new_user_name
        self.email = new_email
        self.password = new_password
        self.url = new_url
    
    #debug method
    def print_acc(self):
        print(f"{self.acc_name},{self.username},{self.password},{self.url}")



def test_case1():
    salt = os.urandom(16)
    password = crypto.hasher("abc", salt)
    Nex = user("Nex", password, salt, "abc")
    Nex.encrypt()
    
    a1 = account("fb", "Nex", "abc@abc", "Penis", "fb.com")
    Nex.add_acc(a1)
    a2 = account("gmail", "Nex", "abc@abcd", "BIG", "google.com")
    Nex.add_acc(a2)
    u.add_user(Nex)

def test_case2():
    salt = os.urandom(16)
    password = crypto.hasher("abc", salt)
    Nex = user("Berta", password, salt, "abc")
    Nex.encrypt()
    
    a1 = account("fb", "Nex", "abc@abc", "Penis", "fb.com")
    Nex.add_acc(a1)
    a2 = account("gmail", "Nex", "abc@abcd", "BIG", "google.com")
    Nex.add_acc(a2)
    u.add_user(Nex)
    
    
def init_users():
    global u
    u = users()
    u.load_users()    

#Note:
#first initialize users, then user and add user to users
    
if __name__ =="__main__":
    init_users()
    
    # test_case1()
    # test_case2()
    
    u.see_users()
    
    
    
    
    
    
    