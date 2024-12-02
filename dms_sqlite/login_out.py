import connect

def login(usr):
    ''' if user login successfully,return True, otherwis return false '''    
    pwd = input("password: ")
    checksql = '''select pwd from users where usr = ?;'''
    connect.c.execute(checksql, (usr,))
    result = connect.c.fetchone()
    if result is None:
        print("The user doesn't exist.")
        return False
    if result and result[0] == pwd:
        print("you log in successfully!")
        return True
    else:
        print("the user doesn't or password is incorrect.") # 分成两部分1.不存在 2.密码错误
        return False

def logout():
    print("You have logged out successfully!")
    return

def register():
    '''
    register new users, and generate the uid automatically
    insert value into the users table
    '''
    global conn,c
    print("register:")
    name = input("please enter your name:")
    email = input("please enter your email:")
    phone_num = input("please enter your phone number:")
    # enterthe same password twiice for verification
    while True:
        pwd = input("Please enter your password: ")
        confirm_pwd = input("Please confirm your password: ")
        if pwd == confirm_pwd:
            break
        else:
            print("Passwords do not match. Please try again.")
    # calculate the new user id
    query = '''SELECT MAX(usr) FROM users;'''
    connect.c.execute(query)
    max_usr = connect.c.fetchone()[0]
    if max_usr is None:
        newid = 1
    else:
        newid = max_usr+1
    #insert value into the tables
    insertsql = '''insert into users (usr, name, email, phone, pwd) values (?,?,?,?);'''
    try:
        connect.c.execute(insertsql,(newid,name,email,phone_num,pwd))
        connect.c.conn.commit()
        print(f"you have registered successfully! your user id is:{newid}")
    except:
        print("error.")
    return newid