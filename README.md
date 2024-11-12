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

## Setup and Execution

1. **Install Requirements**: Ensure Python 3 and SQLite are installed.
2. **Database Setup**: Import the provided database schema using:
   ```sh
   sqlite3 database.db < schema.sql
3. **Run the application**:Start the app with:
   ```sh
   python main.py database.db
