# Enterprise Data Management System

This project implements an enterprise data management system using Python and SQLite, simulating a social media platform where users can manage tweets, follow others, and view follower activity. The project demonstrates the integration of SQL with Python to provide functionalities similar to a simplified Twitter.

## Features

1. **User Authentication**: Supports login for registered users and signup for new users.
2. **View Tweets and Retweets**: Registered users can view tweets and retweets by people they follow.
3. **Tweet Search**: Allows searching for tweets based on keywords or hashtags.
4. **User Search**: Find users by name keyword.
5. **Compose Tweet**: Users can post new tweets with hashtags.
6. **List Followers**: View and manage followers.
7. **Logout**: Users can log out and return to the main screen.

## Database Schema

The system uses the following tables:
- **users**: Stores user credentials and information.
- **follows**: Records relationships between followers and followees.
- **tweets**: Stores user tweets.
- **retweets**: Records retweet information.
- **lists**: Manages user-specific lists.
- **include**: Associates tweets with lists.
- **hashtag_mentions**: Tracks hashtags in tweets.


**users(usr, name, email, phone, pwd)**
**follows(flwer, flwee, start_date)**
**lists(owner_id, lname)**
**include(owner_id, lname, tid)**
**tweets(tid, writer_id, text, tdate, ttime, replyto_tid)**
**retweets(tid, retweeter_id, writer_id, spam, rdate)**
**hashtag_mentions(tid,term)**
Each user has a unique user id (usr), in addition to their name, email, phone and password (pwd).
The table "follows" records each following by storing the follower's id (flwer), the followee's id (flwee), and the date of following (start_date).
User tweets are recorded in the table "tweets". Each tweet has a unique identifier (tid), id of the user who wrote the tweet (writer_id), the text, the date (tdate), and the time (ttime). If the tweet is a reply to another tweet, it will store the original tweet's id (replyto_tid)
Table "retweets" records the id of the tweet (tid), id of the retweeter (retweeter_id), and the tweet's writer. It also stores a flag indicating whether it is spam (spam), and the date of the retweet (rdate).
A user's favorite list is stored in the "lists" table that records the user's id (owner_id) and the list name (lname). The include table consists of the user’s id (owner_id), list name (lname), and tweet id (tid). 

## Setup and Execution

1. **Install Requirements**: Ensure Python 3 and SQLite are installed.
2. **Database Setup**: Import the provided database schema using:
   ```sh
   sqlite3 database.db < schema.sql
3. **Run the application**:Start the app with:
   ```sh
   python main.py database.db
**we have a sample database for testing, but you can use your own database.If you have any questions about the code, feel free to contact me!**
