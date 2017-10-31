# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 21:02:36 2017

@author: Jadon
"""

import pymysql

def insert(gen, match, win, los):
    # Open database connection
    db = pymysql.connect("jadonjes.heliohost.org","jadonjes_darwin","HackThisDB1","jadonjes_OUTCOME" )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO MatchOutTBL(generation,match_num, winner, looser) VALUES ('{0}', '{1}', '{2}', '{3}')".format(str(gen), str(match), str(win), str(los))
    try:
       # Execute the SQL command
       cursor.execute(sql)
       # Commit your changes in the database
       db.commit()
    except:
       # Rollback in case there is any error
       db.rollback()
    
    # disconnect from server
    db.close()
    return sql

cmd = insert(0,1,'darwin1', 'darwin3')