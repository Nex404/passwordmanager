from tkinter import *
from tkinter import messagebox
import classes as c
import os
import cryptography_pwm as crypto



# Font for Headline
Font_tuple = ("Comic Sans MS", 20, "bold")
loged_in = False


def init_users():
    global users
    users = c.users()
    users.load_users()


# get the index of the user to validate the password
def get_index(username):
    index = 0
    for user in users.users:
        if user.username == username:
            return index
        index += 1
        
    return -1


#get called when login button pushed
def validate(username, password):
    index = get_index(username)
    if index == -1:
        print("No Account found for this username")
        return 
    
    # get the account 
    user = users.users[index]
    
    # valedate if password is correct
    if user.hashed_password == crypto.hasher(password, user.salt):
        print("Access granted")
        
        #giving the user a password        
        user.password = password
        # decrypt db file
        user.decrypt()
        # read db acc file and load into accs of user
        accounts = user.db_accounts.see_all(username)
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
        print("incorrect password")
        return 


# on logout delete user 
def logout(user):
    user.password = None
    user.accounts = []
    print("logged out")


def create_lbl(acc_name, username, email, password, url, index):
    # account_name, username, email, password, url=None
    acc_lbl = Label(acc_list, text=acc_name)
    acc_lbl.grid(row=index, column=0)
    
    user_lbl = Label(acc_list, text=username)
    user_lbl.grid(row=index, column=1)
    
    password_lbl = Label(acc_list, text=password)
    password_lbl.grid(row=index, column=2)
    
    email_lbl = Label(acc_list, text=email)
    email_lbl.grid(row=index, column=3)
    
    url_lbl = Label(acc_list, text=url)
    url_lbl.grid(row=index, column=4)


def submit():
    global user 
    global acc_name_entry
    global user_name_entry
    global password_entry
    global email_entry
    global url_entry
    
    if url_entry:
        acc = c.account(acc_name_entry.get(), user_name_entry.get(), email_entry.get(), password_entry.get(), url_entry.get())
    else:
        acc = c.account(acc_name_entry.get(), user_name_entry.get(), email_entry.get(), password_entry.get())
        
    user.add_acc(acc)
    
    if messagebox.askokcancel("Logout", "To confirm changes u must relog"):
        logout(user)
        # close your serial here
        acc_list.destroy()
        global loged_in
        loged_in = False
        global add_user
        add_user.destroy()
    
    
    
    
# function for add_acc
def add_acc():
    # global user
    
    # create window
    global add_user
    add_user = Toplevel()
    add_user.title("Account List")
    add_user.iconbitmap()
    add_user.geometry("400x400")
    
    # creating labels
    acc_name = Label(add_user, text="Account Name:")
    acc_name.grid(row=0, column=0)
    
    user_name = Label(add_user, text="Username:")
    user_name.grid(row=1, column=0)
    
    password_name = Label(add_user, text="Password:")
    password_name.grid(row=2, column=0)
    
    email_name = Label(add_user, text="Email:")
    email_name.grid(row=3, column=0)
    
    url_name = Label(add_user, text="Url:")
    url_name.grid(row=4, column=0)
    
    # creating entries
    global acc_name_entry
    global user_name_entry
    global password_entry
    global email_entry
    global url_entry
    acc_name_entry = Entry(add_user)
    acc_name_entry.grid(row=0, column=1, columnspan=2)
    
    user_name_entry = Entry(add_user)
    user_name_entry.grid(row=1, column=1, columnspan=2)
    
    password_entry = Entry(add_user)
    password_entry.grid(row=2, column=1, columnspan=2)
    
    email_entry = Entry(add_user)
    email_entry.grid(row=3, column=1, columnspan=2)
    
    url_entry = Entry(add_user)
    url_entry.grid(row=4, column=1, columnspan=2)
    
    # submit button
    sub = Button(add_user, text="submit", command=submit)
    sub.grid(row=5, column=0, columnspan=3)
    # refresh display


# del user help
def del_user_help():
    global user
    
    if messagebox.askokcancel("Logout", "To confirm changes u must relog"):
        # close your serial here
        global account_name_entry
        user.remove_acc(account_name_entry.get())
        global del_acc
        del_acc.destroy()
        global acc_list
        acc_list.destroy()
        logout(user)
        global loged_in
        loged_in = False


# function for delete acc
def delete_acc_setup():
    # creating window
    global del_acc
    del_acc = Toplevel()
    del_acc.title("Delete Account")
    del_acc.iconbitmap()
    del_acc.geometry("400x400")
    
    # Label
    account_name = Label(del_acc, text="Account name:")
    account_name.grid(row=0, column=0)
    
    # Entry
    global account_name_entry
    account_name_entry = Entry(del_acc)
    account_name_entry.grid(row=0, column=1)
    
    # submit button
    sb = Button(del_acc, text="Submit", command=del_user_help)
    sb.grid(row=1, column=0, columnspan=2)
    
    
    
# function for changing master pw
def ch_m_pw():
    # creating window
    global ch_mpw
    ch_mpw = Toplevel()
    ch_mpw.title("Change Master Password")
    ch_mpw.iconbitmap()
    ch_mpw.geometry("400x400")
    
    # Labels
    pw = Label(ch_mpw, text="Password:", padx=20)
    pw.grid(row=0, column=0)
    
    c_pw = Label(ch_mpw, text="Confirm Password:", padx=20)
    c_pw.grid(row=1, column=0)
    
    # option = Label(ch_mpw, text="").grid(row=3, column=0, columnspan=2)
    # Entries
    pw_entry = Entry(ch_mpw)
    pw_entry.grid(row=0, column=1)
    
    c_pw_entry = Entry(ch_mpw)
    c_pw_entry.grid(row=1, column=1)
    
    
    # func for button (bad style?)
    def confirm():
        # see if pws match
        if pw_entry.get() == c_pw_entry.get():
            if messagebox.askokcancel("Logout", "To confirm changes u must relog"):
                # close your serial here
                global user
                user.change_master_pw(pw_entry.get())
                ch_mpw.destroy()
                global acc_list
                acc_list.destroy()
                logout(user)
                global loged_in
                loged_in = False
        
    
        else:                
            option = Label(ch_mpw, text="Passwords don't match.").grid(row=3, column=0, columnspan=2)
               
    
    # button
    b = Button(ch_mpw, text="Submit", command=confirm)
    b.grid(row=2, column=0, columnspan=2)
    
    
            

# function for delete user
def delete_user_setup():
    if messagebox.askokcancel("Delete", "Are you sure, you want to delete your account? All your data will be lost!"):
        global user
        global users
        users.remove_user(user, user.password)
        
        global acc_list
        acc_list.destroy()

        global loged_in
        loged_in = False
    

# edit acc help func
def edit_acc_help():
    # open new window
    a_name = a_name_entry.get() 
    global acc_name
    acc_name.destroy()
    
    # getting acc
    global user
    index = 0
    for acc in user.accounts:
        if acc.acc_name == a_name:
            break
        index += 1
    
    if index < len(user.accounts):
        acc = user.accounts[index]
        acc_name.destroy()
                    
        # put old acc in new window
        global edit_acc
        edit_acc = Toplevel()
        edit_acc.title("Edit Account")
        edit_acc.iconbitmap()
        edit_acc.geometry("200x200")
        
        # labels
        l1 = Label(edit_acc, text="Account name")
        l1.grid(row=0, column=0)
        
        l2 = Label(edit_acc, text="User name")
        l2.grid(row=1, column=0)
        
        l3 = Label(edit_acc, text="Password:")
        l3.grid(row=2, column=0)
        
        l4 = Label(edit_acc, text="Email:")
        l4.grid(row=3, column=0)
        
        l5 = Label(edit_acc, text="URL:")
        l5.grid(row=4, column=0)
        
        # Entries
        global e1
        e1 = Entry(edit_acc)
        e1.insert(0, acc.acc_name)
        e1.grid(row=0, column=1)
        
        global e2
        e2 = Entry(edit_acc)
        e2.insert(0, acc.username)
        e2.grid(row=1, column=1)
        
        global e3
        e3 = Entry(edit_acc)
        e3.insert(0, acc.password)
        e3.grid(row=2, column=1)
        
        global e4
        e4 = Entry(edit_acc)
        e4.insert(0, acc.email)
        e4.grid(row=3, column=1)
        
        global e5
        e5 = Entry(edit_acc)
        e5.insert(0, acc.url)
        e5.grid(row=4, column=1)
        
        # submit btn
        b = Button(edit_acc, text="submit", command=lambda: confirm_changes(index)).grid(row=5, column=0, columnspan=2)
  
        
# function to confirm changes
def confirm_changes(index):
    # confirm all changes
    global user
    if messagebox.askokcancel("Logout", "To confirm changes u must relog"):
        # close your serial here
        acc = c.account(e1.get(), e2.get(), e4.get(), e3.get(), e5.get())
        user.edit_acc(index, acc) 
        edit_acc.destroy()
        global acc_list
        acc_list.destroy()
        logout(user)
        global loged_in
        loged_in = False
        
    
    
         
        

# function for editing a acc
def edit_acc():
    global user
    # get acc name
    global acc_name
    acc_name = None
    acc_name = Toplevel()
    acc_name.title("Edit Account")
    acc_name.iconbitmap()
    acc_name.geometry("200x200")
    
    # label
    a_name = Label(acc_name, text="Account name:")
    a_name.grid(row=0, column=0)
    
    # Entry
    global a_name_entry
    a_name_entry = Entry(acc_name)
    a_name_entry.grid(row=0, column=1)
    
    # button
    b = Button(acc_name, text="submit", command=edit_acc_help)
    b.grid(row=1, column=0, columnspan=2)
    
    
    




# options in acc_list
def hit_option():
    v = var.get()
    if v == "add_acc":
        # function for add_acc
        add_acc()
        # print("add acc")
    elif v == "delete_acc":
        # function for delete acc
        delete_acc_setup()
        # print("del acc")
        # maybe rewrite delete for primaries
    ### update acc ???
    elif v == "change_master_pw":
        # function for changing master pw
        ch_m_pw()
        # print("c m pw")
    elif v == "delete_user":
        # function for delete user
        delete_user_setup()
        # print("deluser")
    elif v == "edit_acc":
        edit_acc()
    
# function for presenting the data of accounts
def load_list(user):
    global acc_list
    global loged_in 
    loged_in = True
    
    # creating window
    acc_list = Toplevel()
    acc_list.title("Account List")
    acc_list.iconbitmap()
    acc_list.geometry("400x400")
    acc_list.protocol("WM_DELETE_WINDOW", lambda: ask_logout(user))
    
    # implement options for change master pw, add acc, delete acc, delete user
    Options = ["add_acc", "delete_acc", "change_master_pw", "delete_user", "edit_acc"]
    global var
    var = StringVar()
    var.set(Options[0])
    drop = OptionMenu(acc_list, var, *Options)
    drop.grid(row=0, column=0, columnspan=2)
    
    hit_opt = Button(acc_list, text="Hit Option", command=hit_option)
    hit_opt.grid(row=0, column=2)
    
    # displaying the accs
    create_lbl("Account name", "Username", "Email", "Password", "Url", 1)
    index = 2
    for acc in user.accounts:
        create_lbl(acc.acc_name, acc.username, acc.email, acc.password, acc.url, index)
        index += 1
    


def ask_logout(user):
    if messagebox.askokcancel("Logout", "You want to logout now?"):
        logout(user)
        # close your serial here
        acc_list.destroy()
        global loged_in
        loged_in = False



def login_acc():
    global loged_in 
    if loged_in == True:
        # creating errorlabel for user still logged in
        errormsg = "User still logged in."
        error_lbl = Label(top, text=errormsg, pady=10)
        error_lbl.grid(row=4, column=0, columnspan=2)
        return
        
    global user
    user = validate(username_entry.get(), password_entry.get())
    # user = val()
    if user:
        top.destroy()
        load_list(user)
    else:
        # creating errorlabel for unseccessful login
        errormsg = "Username or Password incorrect"
        error_lbl = Label(top, text=errormsg, pady=10)
        error_lbl.grid(row=4, column=0, columnspan=2)


def login():
    # create new window for login
    global top
    top = Toplevel()
    top.title("LogIn")
    top.iconbitmap()
    top.geometry("250x200")
    
    # headlabel
    head_lbl = Label(top, text="LogIn", pady=10, font=Font_tuple)
    head_lbl.grid(row=0, column=0, columnspan=2)
    
    # create labels and position
    username_lbl = Label(top, text="Username:", pady=10, padx=20 )
    username_lbl.grid(row=1, column=0)
    password_lbl = Label(top, text="Password:", pady=10, padx=20)
    password_lbl.grid(row=2, column=0)
    
    # create Entrys and position
    global username_entry
    global password_entry
    username_entry = Entry(top)
    username_entry.grid(row=1, column=1)
    password_entry = Entry(top)
    password_entry.grid(row=2, column=1)
    
    # creating Login Button
    login_btn = Button(top, text="log in", command=login_acc, padx=10)
    login_btn.grid(row=3, column=0, columnspan=2)

def add_user_setup(username, password, confirm_password):
    """Setup function to create user and the db and insert in userdatabase"""
    global errorlbl
    global usecase_lbl
    # check if username or password is empty
    if username == "" or password == "":
        if errorlbl:
            errorlbl.destroy()
            
        errormsg = "No Password or no username defined"
        errorlbl = Label(register, text=errormsg, pady=10)
        errorlbl.grid(row=5, column=0, columnspan=2)
        return
    
    # Check if password and confirm password is equal
    if password != confirm_password:
        if errorlbl:
            errorlbl.destroy()
            
        errormsg = "Passwords don't match"
        errorlbl = Label(register, text=errormsg, pady=10)
        errorlbl.grid(row=5, column=0, columnspan=2)
        return
    else:
        if errorlbl:
            errorlbl.destroy()
            
        errormsg = ""
        errorlbl = Label(register, text=errormsg, pady=10)
        errorlbl.grid(row=5, column=0, columnspan=2)
    
    # check if username is already in use
    for user in users.users:
        if user.username == username:
            if errorlbl:
                errorlbl.destroy()
                
            errormsg = "Username taken"
            errorlbl = Label(register, text=errormsg, pady=10)
            errorlbl.grid(row=5, column=0, columnspan=2)
            return
    
    salt = os.urandom(16)
    hashedpassword = crypto.hasher(password, salt)
    u = c.user(username, hashedpassword, salt, password)
    users.add_user(u)
    u.encrypt()
    
    register.destroy()
    
    if usecase_lbl:
        usecase_lbl.destroy()
    usecase_lbl = Label(root, text="Account created", pady=5).pack()

 
def register():
    # create register window
    global register
    register = Toplevel()
    register.title("Register")
    register.iconbitmap()
    register.geometry("300x250")
    
    # headlabel
    head_lbl = Label(register, text="Register", pady=10, font=Font_tuple)
    head_lbl.grid(row=0, column=0, columnspan=2)
    
    # create labels and position
    username_lbl = Label(register, text="Username:", pady=10, padx=20 )
    username_lbl.grid(row=1, column=0)
    password_lbl = Label(register, text="Password:", pady=10, padx=20)
    password_lbl.grid(row=2, column=0)
    confirm_password_lbl = Label(register, text="Confirm Password:", pady=10, padx=20)
    confirm_password_lbl.grid(row=3, column=0)
    
    # create Entrys and position
    username_entry = Entry(register)
    username_entry.grid(row=1, column=1)
    password_entry = Entry(register)
    password_entry.grid(row=2, column=1)
    confirm_password_entry = Entry(register)
    confirm_password_entry.grid(row=3, column=1)
        
    # creating Login Button
    register_btn = Button(register, text="register", command=lambda:add_user_setup(username_entry.get(), password_entry.get(), confirm_password_entry.get()), padx=10)
    register_btn.grid(row=4, column=0, columnspan=2)
    
    global errorlbl
    errorlbl = Label(register, text="", pady=10)
    errorlbl.grid(row=5, column=0, columnspan=2)


if __name__=="__main__":
    root = Tk()
    root.title("Passwordmanager")
    root.iconbitmap()
    root.geometry("300x200")
    # root.configure(background="green")
    
    # initialize users
    init_users()
    
    # creating main window and there widgets
    main_label = Label(root, text="Passwordmanager", font=Font_tuple, pady=10)
    main_label.pack()
    
    
    logIn_btn = Button(root, text="LogIn", command=login, padx="57")
    # logIn_btn.grid(row=1, column=1, columnspan=1)
    logIn_btn.pack()
    
    register_btn = Button(root, text="Register", command=register, padx="51")
    # register_btn.grid(row=2, column=1, columnspan=1)
    register_btn.pack()
                      
    exit_btn = Button(root, text="Exit App", command=root.destroy, padx="50")
    # exit_btn.grid(row=3, column=1, columnspan=1)
    exit_btn.pack()
    
    global usecase_lbl
    usecase_lbl = Label(root, text="", pady=5).pack()
    
    root.mainloop()