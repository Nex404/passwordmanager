#TODO:
#Create Hasher who hashes passwords         x
#Create addUser                             x
#create setupUser                           x
#Create delete User                         x
#Create delete User setup                   x
#Create checker who checks credentials      x
#Create changeMasterPW

#small Menü for testing                     x

#Create a Database for each user            x
#Create addAccount in user                  x
#Create removeAccount in user               x
#Create Injection to see passwords          x   
#Create copy to clipboard
#Create an encrypter                        x
#Create a decrypter                         x
#Create Random password generator           x


#onstart read users from file or database   x
#onexit overwrite users in file or database with current users x

#Maybe make an UI

#used libaries
import hashlib
import os
import sys
import sqlite3
from sqlite3 import Error
import random
import string
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet, InvalidToken
import time

users = []

def hasher(password, salt):
    bin_pw = password.encode()
    hasher = hashlib.pbkdf2_hmac('sha256', bin_pw, salt, 100000)
    
    hashed_pw = hasher.hex()
    return hashed_pw


def en_de_alg(password, salt):
    pw = password  # This is input in the form of a string
    pw_b = pw.encode()  # Convert to type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(pw_b))  # Can only use kdf once
    return key


def encrypter(password, salt, db_file):
    key = en_de_alg(password, salt)
    input_file = db_file
    output_file = db_file + ".encrypted"

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the input file

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)  # Write the encrypted bytes to the output file

    # delete input_file
    # os.remove(input_file)
    return output_file
    

def decrypter(password, salt, db_file):
    key = en_de_alg(password, salt)
    input_file = db_file + ".encrypted"
    output_file = db_file

    with open(input_file, 'rb') as f:
        data = f.read()  # Read the bytes of the encrypted file

    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(data)

        with open(output_file, 'wb') as f:
            f.write(decrypted)  # Write the decrypted bytes to the output file

        # Note: You can delete input_file here if you want
        # os.remove(input_file)

    except InvalidToken as e:
        print("Invalid Key - Unsuccessfully decrypted")
        print(e)

    return output_file


def addUser(name, password):
    user = []
    user.append(name)
    salt = os.urandom(16)
    user.append(hasher(password, salt))
    user.append(salt)
    global users
    users.append(user)
    return salt


def setupUser():
    print("Welcome User! \nNow we will start with the Account Creation.")
    username = input("Please enter your prefered username: ")
    #preventing double usernames:
    for user in users:
        if username in user:
            print("This username is already taken. Please try again")
            return

    password = input("Please enter your prefered masterpassword: ")
    password_conf = input("Please confirm your prefered masterpassword: ")
    if password != password_conf:
        print("Please try again. Your passwords doesn't match.")

    else:
        salt = addUser(username, password)

        # create db for accounts
        db_file = "DBs/" + username + "_acc.db"
        init_db(db_file)
        encrypter(password, salt, db_file)

        print("Account successfully created!")


def deleteUser(user, password):
    account_found = False
    usercounter = 0
    for u in users:
        if user in u:
            if hasher(password, u[2]) == u[1]:
                account_found = True
                confirm = input("Do you realy want to delete this Account? (y/n): ")
                if confirm == "y" or confirm == "yes":
                    delacc = users.pop(usercounter)
                    os.remove("DBs/" + user + "_acc.db")
                    print(f"You deleted the Account {delacc[0]}")

                else:
                    print("You declined or gave an incorrect input.")
                
                break
                    
        usercounter = usercounter + 1 


    if account_found == False:
        print("No such account found.")


def deleteUserSetup():
    confirm = input("You are about to delete an account. Do you want to continue? (y/n) ")
    if confirm != "y":
        return
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    deleteUser(username, password)


def changeMasterPW(user, password, salt):
    pw = input("Please enter your current password: ")
    for u in users:
        if user in u:
            if hasher(pw, salt) == hasher(password, salt):
                # create new masterpassword
                new_pw = input("Please enter the new masterpassword: ")
                new_pw_conf = input("Please confirm the new masterpassword: ")
                if new_pw != new_pw_conf:
                    print("The passwords doesn't match. Please try again")
                    return
                
                # override in users the hashed masterpassword
                u[1] = hasher(new_pw, salt)

                # text u gonna be loged out pls login again to continue
                print("Your masterpassword has been successfully changed.")
                print("You will be loged out. To continue please login again.")
                time.sleep(2)

            else:
                print("Password not correct, please try again.")
             
    pass


def init_db(db_file):
    # """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        sql_command = """
            CREATE TABLE accounts ( 
            acc_num INTEGER NOT NULL AUTO_INCREMENT PRIMARY KEY, 
            acc_name VARCHAR(50), 
            acc_username VARCHAR(50), 
            acc_email VARCHAR(30), 
            acc_password VARCHAR(50),
            acc_url VARCHAR(50));"""
        
        cursor.execute(sql_command)
        conn.commit()

    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def addAccount(db_file, acc_name, acc_username, acc_email, acc_password, acc_url):
    # open connection to db
    connection = None
    try:
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # insert data into db
        sql_command = f"INSERT INTO accounts (acc_name, acc_username, acc_email, acc_password, acc_url) VALUES ({acc_name}, {acc_username}, {acc_email}, {acc_password}, {acc_url});"
        cursor.execute(sql_command)

        # save and close connection
        connection.commit()
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def addAccountSetup(db_file, password, salt):
    # details from user
    acc_name = input("Whats the name (alias) for this account? \nThats the name you look for when u serch for your acc details: ")
    acc_username = input("Whats the username: ")
    acc_email = input("Whats the email adress: ")
    acc_password = input("Whats the password for this account: ")
    acc_url = input("For which website is this account: ")
    # decrypt file
    db_file = decrypter(password, salt, db_file)
    # add account
    addAccount(db_file, acc_name, acc_username, acc_email, acc_password, acc_url)
    # encrypt file
    db_file = encrypter(password, salt, db_file)


def removeAccount(db_file, acc_name):
    connection = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()  

        sql_command = f"DELETE FROM accounts WHERE acc_name = {acc_name}"

        cursor.execute(sql_command)
        connection.commit()

    except Error as e:
        print(e)

    finally:
        if connection:
            connection.close()


def removeAccountSetup(db_file, password, salt):
    agree = input("You are about to delete an Account. Do you want to continue? (y/n): ")
    if agree == "y":
        accname = input("Which account do you want to delete?: ")
        # decrypt file
        db_file = decrypter(password, salt, db_file)
        
        # injection to be sure
        print("You are about to delete: ")
        accInjection(db_file, accname)
        cont = input("Do you want to continue? (y/n): ")
        if cont == "y":
            # remove account
            removeAccount(db_file, accname)
            
        # encrypt file
        db_file = encrypter(password, salt, db_file)


def accInjection(db_file, acc_name):
    connection = None
    try:
        # esteblish connection
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        # create injection
        sql_command = f"SELECT * FROM accounts WHERE acc_name LIKE %{acc_name}%;"
        # cursor.execute(sql_command)

        print(cursor.fetchall(sql_command))
        # close connection
    except Error as e:
        print(e)
    finally:
        if connection:
            connection.close()


def accInjectionSetup(db_file, password, salt):
    accountname = input("Which account are you looking for?: ")

    # decrypt file
    db_file = decrypter(password, salt, db_file)
    # injection
    accInjection(db_file, accountname)
    # encrypt file
    db_file = encrypter(password, salt, db_file)


def login():
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    granted = False
    for user in users:
        if username in user:
            if hasher(password, user[2]) == user[1]:
                print("Access granted")
                granted = True
                break

    if granted == False:
        print("Username or Password is wrong. Please try again.")

    return granted, username, password

# get random string password with letters, digits, and symbols
def get_random_password_string(length):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(password_characters) for i in range(length))
    print("Random string password is:", password)
    confirm = input("Do you want to use this password? (y/n): ")
    if confirm == "y":
        return password
    else:
        return


def menu():
    while True:
        # print("\n\n")
        print("Menu")
        print(40*"-")
        print("Do you want to login?            Press: 1")
        print("Do you want to add a new user?   Press: 2")
        print("Do you want to delete a user?    Press: 3")
        print("Do you want to exit?             Press: 4")
        print(30*"-")

        number = input("\nYour choice: ")
        print("\n\n")

        if number == "1":
            print("login")
            login = login()


            if login[0] == True:
                # Account 
                username = login[1]
                password = login[2]
                salt = b''
                #find salt
                for user in users:
                    if username in user:
                        salt = user[2] 

                # login menu
                while True:
                    print("Login Menu")
                    print(40*"-")
                    print("Do you want to search for an account?        Press: 1")
                    print("Do you want to add a new account?            Press: 2")
                    print("Do you want to remove an account?            Press: 3")
                    print("Do you want to change your master password?  Press: 4")
                    print("Do you want to logout?                       Press: 5")
                    print(30*"-")

                    number = input("\nYour choice: ")
                    print("\n\n")

                    db_file = "DBs/" + username + ".db.encrypted"

                    if number == "1":
                        # accInjectionSetup(db_file, password, salt)
                        accountname = input("Which account are you looking for?: ")

                        # decrypt file
                        db_file = decrypter(password, salt, db_file)
                        # injection
                        accInjection(db_file, accountname)
                        # encrypt file
                        db_file = encrypter(password, salt, db_file)


                    elif number == "2":
                        # addAccountSetup(db_file, password, salt)
                        # details from user
                        acc_name = input("Whats the name (alias) for this account? \nThats the name you look for when u serch for your acc details: ")
                        acc_username = input("Whats the username: ")
                        acc_email = input("Whats the email adress: ")
                        acc_password = input("Whats the password for this account: ")
                        acc_url = input("For which website is this account: ")

                        # decrypt file
                        db_file = decrypter(password, salt, db_file)
                        # add account
                        addAccount(db_file, acc_name, acc_username, acc_email, acc_password, acc_url)
                        # encrypt file
                        db_file = encrypter(password, salt, db_file)

                    elif number == "3":
                        # removeAccountSetup(db_file, password, salt)
                        agree = input("You are about to delete an Account. Do you want to continue? (y/n): ")
                        if agree == "y":
                            accname = input("Which account do you want to delete?: ")

                            # decrypt file
                            db_file = decrypter(password, salt, db_file)
                            
                            # injection to be sure
                            print("You are about to delete: ")
                            accInjection(db_file, accname)
                            cont = input("Do you want to continue? (y/n): ")

                            if cont == "y":
                                # remove account
                                removeAccount(db_file, accname)

                            # encrypt file
                            db_file = encrypter(password, salt, db_file)

                    elif number == "4":
                        changeMasterPW(username, password, salt)
                        break
                        

                    elif number == "5":
                        break
                    else:
                        print("Your input is not valid. Please try again.")

        elif number == "2":
            setupUser()
        elif number == "3":
            deleteUserSetup()
        elif number == "4":
            break
        else:
            print("Your input is not valid. Please try again.")

#both comming funktions should also be decrypted and encrypted 
def on_start():
    try:
        with open("cad.txt", "rb") as file:
            for line in file:
                acc = line
                acc = acc.strip("\n".encode())
                acc = acc.split(",".encode())
                acc[0] = acc[0].decode()
                acc[1] = acc[1].decode()
                users.append(acc)
            
            # print(users)
    except:
        print("Something went wrong")

    
def on_exit():
    with open("cad.txt", "wb") as f:
        for user in users:
            counter = 0
            for attribute in user:
                if counter != 2:
                    f.write(attribute.encode())
                    f.write(",".encode())
                    # print(attribute.encode())
                    # print(",".encode())
                else:
                    f.write(attribute)
                    # print(attribute)
                counter = counter + 1
            f.write("\n".encode())



if __name__ == "__main__": 
    #read credential file
    on_start()
    #programm mainloop
    menu()
    #save and overwrite credential file
    on_exit()
    #exit programm
    sys.exit()

