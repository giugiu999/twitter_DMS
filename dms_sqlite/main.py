import connect
import user
import login_out
import tweets
import user
import sys

def main():
    '''
    ask the code for register,login,and logout
    '''
    global conn,c
    if len(sys.argv) != 2:
        print("Usage: python main.py <database_path>")
        sys.exit(1)
    menu = "Dashboard:\n1.log in \n2.register\n3.exit"
    usermenu = "\nWelcome back! Dashboard:\n1.search for tweets\n2.search for users\n3.compose a tweet\n4.list followers\n5.reply to a tweet\n6.retweet a tweet\n7.follow a user\n8.log out"
    path = sys.argv[1]
    # check if it's valid path
    try:
        connect.connect(path)
        print(f"Connected to database: {path}")
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        sys.exit(1)
    loop=True
    while loop:
        print(menu)
        try:
            code = int(input("enter the number for the operation:"))
            code <= 3
        except:
            print("please enter 1,2,or 3.")
        if code ==1:
            usr = input("user ID: ")
            if login_out.login(usr):
                print(usermenu)
                code2=int(input())
                if code2 == 1:
                    tweets.search_tweets()
                elif code2 == 2:
                    user.search_user()
                elif code2 == 3:
                    tweets.compose_tweet(usr)
                elif code2 == 4:
                    user.list_flw(usr)
                elif code2 == 5:
                    tid = input("Enter the Tweet ID to reply to: ")
                    tweets.compose_reply(tid, usr)
                elif code2 == 6:
                    tid = input("Enter the Tweet ID to retweet: ")
                    tweets.retweet(tid, usr)
                elif code2 == 7:
                    follower_id = input("Enter the User ID to follow: ")
                    user.follow_user(usr, follower_id)
                elif code2 == 8:
                    login_out.logout()
                    break
        elif code == 2:
            login_out.register()
        elif code==3:
            answer=input("log out?(y/n)")
            if answer == 'y':
                login_out.logout()
                loop=False
            
if __name__ =="__main__":
    main()
