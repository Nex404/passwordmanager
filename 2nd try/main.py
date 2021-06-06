import db_pwm as db
import classes as c
import cryptography_pwm as crypto
import os




def init_users():
    db_file = db.db_users()
    users = db_file.see_all()
    u = users[0]
    global user
    user = c.user(u[1], u[2])
    


# get the index of the user to validate the password
# def get_index(username):
#     index = 0
#     for user in users.users:
#         if user.username == username:
#             return index
#         index += 1
        
#     return -1


#get called when login button pushed
def validate(password):
    # index = get_index(username)
    # if index == -1:
    #     print("No Account found for this username")
    #     return 
    
    # get the account 
    # user = users.users[index]
    
    # valedate if password is correct
    if user.hashed_password == crypto.hasher(password, user.salt):
        print("Access granted")
        user.password = password
        
        
        # decrypt db file
        user.decrypt()
        
        # read db acc file and load into accs of user
        accounts = user.db_accounts.see_all()
        for acc in accounts:
            # print(acc)
            acc_name = acc[1]
            username = acc[2]
            email = acc[3]
            password = acc[4]
            url = acc[5]
            user.accounts.append(c.account(acc_name, username, email, password, url))
            
        # encrypt db file
        user.encrypt()
        return user
    else:
        print("accsess not granted")
        return 
    
# on logout delete user 
# evetually has to edit users, that the accs are not stored anymore
def logout(user):
    print("loged out")
    del user
    


def test_case1():
    salt = os.urandom(16)
    password = "HalloMan123"
    hashed_password = crypto.hasher(password, salt)
    global user
    user = c.user(hashed_password, salt, password)
    user.encrypt()
    a1 = c.account("fb", "Nex", "bla@bla.com", "Penis", "fb.com")
    a2 = c.account("fq", "Nex", "bla@bla.com", "Penis", "fb.com")
    user.add_acc(a1)
    user.add_acc(a2)
    
    
    
    db_user = db.db_users()
    db_user.add_user(hashed_password, salt)


def test_case2():
    db_user = db.db_users()
    db_user.see_all()
    
    
# existiert user noch in users?    


if __name__=="__main__":
    init_users()
    # test_case1()
    # test_case2()
    
    # user.print_user()
    
    # validate("HalloMan123")
    # user.change_master_pw("HalloMan1234")
    # validate("HalloMan1234")
    
    # a3 = c.account("fq", "Nex", "bla@bla.com", "Penis", "fb.com")
    # user.add_acc(a3)
    # user.remove_acc(a3)
    
    # user.print_accs()
    
    # user.print_accs()
    
    
    
    
    
    
    
    
    
    
    