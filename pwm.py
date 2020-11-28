#TODO:
#Create Hasher who hashes passwords         x
#Create addUser                             x
#create setupUser                           x
#Create delete User                         x
#Create delete User setup                   x
#Create checker who checks credentials      x

#small Menü for testing                     x

#Create a Database for each user
#Create addAccount in user
#Create removeAccount in user
#Create an encrypter 
#Create a decrypter
#Create Random password generator

#onstart read users from file or database
#onexit overwrite users in file or database with current users 

#Maybe make an UI

#used libaries
import hashlib
import os
import sys

users = []

def hasher(password, salt):
    bin_pw = password.encode()
    hasher = hashlib.pbkdf2_hmac('sha256', bin_pw, salt, 100000)
    
    hashed_pw = hasher.hex()
    return hashed_pw

def addUser(name, password):
    user = []
    user.append(name)
    salt = os.urandom(16)
    user.append(hasher(password, salt))
    user.append(salt)
    global users
    users.append(user)


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
        addUser(username, password)
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

    return granted

def menu():
    while True:
        # print("\n\n")
        print("Menu")
        print(30*"-")
        print("Do you want to login?            Press: 1")
        print("Do you want to add a new user?   Press: 2")
        print("Do you want to delete a user?    Press: 3")
        print("Do you want to exit?             Press: 4")
        print(30*"-")

        number = input("\nYour choice: ")
        print("\n\n")

        if number == "1":
            print("login")
            login_success = login()

        elif number == "2":
            setupUser()
        elif number == "3":
            deleteUserSetup()
        elif number == "4":
            break
        else:
            print("Your input is not valid. Please try again.")

#both comming funktions should also be decrypted and encrypted 
def onstart():
    try:
        with open("cad.txt", "r") as file:
            for line in file:
                acc = line
                acc = acc.strip("\n")
                acc = acc.strip(",").split(",")
                acc[2] = acc[2].encode()
                users.append(acc)
                print(users)
    except:
        print("Something went wrong")

    

def onexit():
    with open("cad.txt", "w") as file:
        for user in users:
            counter = 0
            for attribute in user:
                # if counter == 2:
                #     attribute = attribute.decode()
                file.write(str(attribute))
                file.write(",")
            file.write("\n")



if __name__ == "__main__":    
    #read credential file
    onstart()
    #programm mainloop
    menu()
    #save and overwrite credential file
    onexit()
    #exit programm
    sys.exit()

