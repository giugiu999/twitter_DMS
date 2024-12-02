import sqlite3

conn = None
c= None

def connect(path):
    '''
    connect to the databse
    '''
    global conn,c
    conn = sqlite3.connect(path)
    c= conn.cursor()
    foreignsql = '''pragma foreign_keys='on';'''
    c.execute(foreignsql)
    conn.commit()
    return