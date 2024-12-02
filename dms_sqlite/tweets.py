import connect
import re

def search_tweets():
    '''
    starts with # --> text includes the #hashtag (through hashtag_mentions)
    no # --> tweets.text
    new to old
    5 lists on each page
    user can check num of retweets and reply
    '''
    global conn,c
    keywords = input("Enter keywords separated by spaces: ").split()
    results=[]
    for keyword in keywords:
        if keyword.startswith("#"):
            query = '''select tweets.tid,tweets.text,tweets.tdate
                        from tweets
                        join hashtag_mentions ON tweets.tid = hashtag_mentions.tid 
                        where hashtag_mentions.term=?
                        order by tweets.tdate desc limit 5 offset ?;''' 
            connect.c.execute(query, (keyword.strip("#"), 0)) # initial page offset=0
        else:
            query = '''select tid, text, tdate from tweets where lower(text) like ?
                        order by tdate desc limit 5 offset ?;''' 
        connect.c.execute(query, (f"%{keyword}%", 0))# initial page offset=0
        result=connect.c.fetchall()
        results.extend(result)
        # 分页显示
        page=0
        while True:
            start=page*5
            end=start+5
            contents=results[start:end]
            if not contents:
                print("no more tweets to display.")
                break
            for tweet in contents:
                print(f"Tweet ID: {tweet[0]}, Date: {tweet[2]}, Text: {tweet[1]}")
        
            # choices for futher operations
            choice = input("enter 'n' for the next page, 's' to select a tweet, or 'q' to quit:").lower()
            if choice =='n':
                page+=1
            elif choice=='s':
                tid = input("enter the tweet ID to view details:")
                show_tinfo()
            elif choice=='q':
                break
            else:
                print("invalid input. please try again.")

def show_tinfo(tid):
    '''
    some statistics about the tweet including the number of retweets and the number of replies.
    '''
    Qretweets = '''select count(*) from retweets where tid=?;'''
    connect.c.execute(Qretweets,(tid,))
    retweetnum = connect.c.fetchone()[0]
    Qreply = '''select replyto_tid from tweets where tid=?;'''
    connect.c.execute(Qreply,(tid,))
    replynum = connect.c.fetchone()[0]
    print(f"Tweet ID: {tid}")
    print(f"Retweet Count: {retweetnum}")
    print(f"Reply Count: {replynum}")
    while True:
        choice = input("Enter 'r' to reply, 't' to retweet, or 'q' to quit: ").lower()
        if choice=='r':
            compose_reply(tid)
        elif choice == "t":
            retweet(tid)
        else:
            print("invalid input.please try again.")

def compose_reply(tid,uid):
    '''
    compose a reply below a tweet by current login id
    '''
    reply = input("please enter your reply:").strip()
    if not reply:
        print("Reply cannot be empty. Please try again.")
        return
    query = '''insert into tweets (writer_id, text, tdate, ttime, replyto_tid) 
    values (?, ?, DATE('now'), TIME('now'), ?);'''# built-in module in sqlite
    connect.c.execute(query,(uid,reply,tid))
    connect.conn.commit()
    print("Reply posted successfully!")
    
def retweet(tid,uid):
    '''
    retweet by current login id
    you cannot retweet a tweet twice
    '''
    # check if the user has already retweeted it
    Qcheck='''select 1 from retweets WHERE tid = ? AND retweeter_id = ?;'''
    connect.c.execute(Qcheck, (tid, uid))
    result = connect.c.fetchone()
    if result:
        print("You have already retweeted this tweet.")
        return
    
    query = '''
    INSERT INTO retweets (tid, retweeter_id, rdate, spam)
    VALUES (?, ?, DATE('now'), 0);'''
    connect.c.execute(query, (tid, uid))
    connect.conn.commit()
    print("Tweet retweeted successfully!")

def compose_tweet(uid):
    '''
    Compose a new tweet by the current login user.
    - The tweet can include hashtags (marked with #).
    - Duplicate hashtags in a single tweet are ignored.
    '''
    text=input("please enter your text:").strip()
    if not text:
        print("Tweet cannot be empty!")
        return
    # extract hashtags(start with #) from text
    hashtags = set(re.findall(r'#(\w+)', text)) # avoid duplicating
    Qtweet='''insert into tweets (writer_id, text, tdate, ttime) values (?, ?, DATE('now'), TIME('now'));'''
    connect.c.execute(Qtweet,(uid,text))
    tid=connect.c.lastrowid
    if hashtags:
        for hashtag in hashtags:
            Qhashtag='''insert into hashtag_mentions (tid, term) values (?,?);'''
            connect.c.execute(Qhashtag,(tid,hashtag))
    connect.conn.commit()
    print("Tweet posted successfully!")