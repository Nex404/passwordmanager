#defining classes for users and accounts

import os
import db_pwm as db
import cryptography_pwm as crypto


class user():
    #constructor
    #Note: has to be encrypted before using
    def __init__(self, hashedpassword, salt, password=None):
        self.salt = salt
        self.hashed_password = hashedpassword #crypto.hasher(password, self.salt)
        if password:
            if crypto.hasher(password, self.salt) == self.hashed_password:
                self.password = password
            else:
                self.password = None
                print("Password Incorrect")
            
        self.accounts = []
        
        try:
            self.db_accounts = db.db_acc()
        except:
            print("couldnt connect to db")

        
    def add_acc(self, account):
        # if crypto.hasher(confirm_password, self.salt) == self.hashed_password:
        if self.password:
            self.accounts.append(account)
            self.decrypt()
            self.db_accounts.add_acc(account.acc_name, account.username, account.email, account.password, account.url)
            self.encrypt()
        else:
            print("no password")
        
    def remove_acc(self, account):
        # if crypto.hasher(confirm_password) == self.hashed_password:
        if self.password:
            self.decrypt()
            self.db_accounts.remove_acc(account.acc_name, account.username, account.email, account.password)
            self.encrypt()
            index = 0
            for i in self.accounts:
                if i.acc_name == account.acc_name:
                    break
                index += 1
                
            self.accounts.pop(index)
        else:
            print("no Password")
     
        # not working
    def change_master_pw(self, new_password):
        # if self.hashed_password == crypto.hasher(confirm_password, self.salt):
        if self.password:    
            #handeling acc db
            self.decrypt()
            self.hashed_password = crypto.hasher(new_password, self.salt)
            self.password = new_password
            self.encrypt()
            
            # update hashed password in users db
            db.update_pw(self.hashed_password)
            
            print("masterpassword changed")
        else:
            print("No Password")
            
    def encrypt(self):
        crypto.encrypter(self.password, self.salt, "accs.db")
        
    def decrypt(self):
        crypto.decrypter(self.password, self.salt, "accs.db")
        
    #debug method
    def print_user(self):
        print(f"I'm  and have {self.hashed_password} as pw. the salt is {self.salt}")
        
    def print_accs(self):
        if self.password:
            for acc in self.accounts:
                print(acc.username + " " + acc.password)
        else:
            print("No Password")


    
        
        
    
class account():
    #constructor
    def __init__(self, account_name, username, email, password, url=None):
        self.acc_name = account_name
        self.username = username
        self.email = email
        self.password = password
        self.url = url
    
    def edit_acc_name(self, new_acc_name):
        self.acc_name = new_acc_name
        
    def edit_username(self, new_user_name):
        self.username = new_user_name
    
    def edit_email(self, new_email):
        self.email = new_email
        
    def edit_password(self, new_password):
        pw = input("Please confirm your new password: ")
        if pw == new_password:
            self.password = new_password
        else:
            print("Passwords do not match. Please try again")
        
        #in case for simplification for GUI
        #self.password = new_password
    
    def edit_url(self, new_url):
        self.url = new_url
    
    #debug method
    def print_acc(self):
        print(f"{self.acc_name},{self.username},{self.password},{self.url}")




#Note:
#first initialize users, then user and add user to users
    
if __name__ =="__main__":
    pass
    
    
    
    
    
    
    