import connect

def search_user():
    '''
    enter a keyword and the system should retrieve all users whose names contain the keyword
    display both the user id and the user name
    an ascending order of name length.
    '''
    keyword=input("please enter a keyword to search users:").strip().lower()
    query='''select usr,name from users where lower(name) like ?
            order by ength(name) asc'''
    connect.c.execute(query,(f"%{keyword}%"))
    results=connect.c.fetchall()
    if not results:
        print("No users found matching your keyword.")
        return
    # 分页显示
    page=0
    while True:
        start = page*5
        end = page+5
        contents=results[start:end]
        if not contents:
            print("no more user to display.")
            break
        print("matching users:")
        for user in contents:
            print(f"User ID: {user[0]}, Name: {user[1]}")
        while True:
            choice = input("\nEnter 'n' for next page, 's' to select a user, or 'q' to quit: ").lower()
            if choice == 'n':
                page += 1
            elif choice == 's':
                suid = input("Enter the User ID to view details: ")
                show_uinfo(suid)
            elif choice == 'q':
                break
            else:
                print("Invalid input. Please try again.")

def show_uinfo(uid,suid):
    '''
    select a user and see more information about the user including 
    the number of tweets, the number of users being followed by the user, the number of followers,
    and up to 3 most recent tweets. 
    '''
    Qtweets = '''select count(*) from tweets 
        where writer_id = ?;'''
    connect.c.execute(Qtweets,(suid,))
    tweetnum=connect.c.fetchone()[0]
    Qflwee = '''select count(*) from follows where flwer=?;'''
    connect.c.execute(Qflwee, (suid,))
    flweenum = connect.c.fetchone()[0]
    Qflw='''select count(*) from follows where flwee=?;'''
    connect.c.execute(Qflw,(suid,))
    flwnum=connect.c.fetchone()[0]
    # 3 most recent tweets
    Q3tweets='''select text,tdate,time from tweets where writer_id = ? order by tdate desc, ttime desc limit 3;'''
    connect.c.execute(Q3tweets,(suid,))
    tweets=connect.c.fetchall()
    print(f"\nUser ID: {suid}")
    print(f"Number of Tweets: {tweetnum}")
    print(f"Number of Users Following: {flweenum}")
    print(f"Number of Followers: {flwnum}")
    print("Recent Tweets:")
    for tweet in tweets:
        print(f"- {tweet[0]} (Date: {tweet[1]}, Time: {tweet[2]})")
    while True:
        action = input("\nEnter 'f' to follow this user, 'm' to see more tweets, or 'q' to quit: ").lower()
        if action == 'f':
            follow(uid,suid)
        elif action == 'm':
            show_more_tweets(uid)
        elif action == 'q':
            return
        else:
            print("Invalid input.please try again.")

def follow(uid,suid):
    '''
    Follow a selected user(suid) by the current logged-in user(uid).
    insert value into the related tables
    '''
    Qcheck='''select 1 from follows where flwer=? and flwee=?;'''
    connect.c.execute(Qcheck,(uid,suid))
    if connect.c.fetchone():
        print("You are already following this user.")
        return
    Qfollow='''insert into follows (flwer, flwee, start_date) values (?,?,date('now'));'''
    connect.c.execute(Qfollow, (uid, suid))
    connect.c.connection.commit()
    print("You are now following this user!")

def show_more_tweets(uid):
    query = '''
        SELECT text, tdate 
        FROM tweets 
        WHERE writer_id = ? 
        ORDER BY tdate DESC;
    '''
    connect.c.execute(query, (uid,))
    tweets = connect.c.fetchall()
    if not tweets:
        print("This user has no tweets.")
        return
    print(f"\nAll tweets by User ID {uid}:")
    for tweet in tweets:
        print(f"- {tweet[0]} (Date: {tweet[1]})")

def list_flw(uid):
    '''
    list all flw(5 each time), and user can check the flw's: 
    the number of tweets, 
    the number of users being followed, 
    the number of followers, 
    and up to 3 most recent tweets.
    '''
    query = '''SELECT flwer FROM follows WHERE flwee = ?;'''
    connect.c.execute(query, (uid,))
    followers = connect.c.fetchall()

    if not followers:
        print("You have no followers.")
        return

    page = 0
    while True:
        start = page * 5
        end = start + 5
        followers_to_display = followers[start:end]

        if not followers_to_display:
            print("No more followers to display.")
            break

        print("\nYour followers:")
        for follower in followers_to_display:
            print(f"Follower ID: {follower[0]}")

        user_input = input("Enter 'n' for next page, 's' to select a follower, or 'q' to quit: ").lower()
        if user_input == "n":
            page += 1
        elif user_input == "s":
            follower_id = input("Enter the Follower ID to view details: ")
            show_uinfo(uid,follower_id)
        elif user_input == "q":
            break
        else:
            print("Invalid input. Please try again.")