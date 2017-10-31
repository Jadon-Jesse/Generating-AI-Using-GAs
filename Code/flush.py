# -*- coding: utf-8 -*-
"""
Created on Mon Sep  4 22:04:00 2017

@author: Jadon
"""

import numpy as np
import glob, os, shutil
import pymysql

#replace the select.def file
def my_super_copy():
    source = "CharTemplate/select.def"
    target = "../MUGEN/mugen-1.0/mugen/data/select.def"
    try:
        shutil.copy(source, target)
    except IOError:
        os.chmod(target, 777) #?? still can raise exception
        shutil.copy(source, target)


#First delete all characters named dArwin
def kill_darwin():
    dirs = glob.glob("../MUGEN/mugen-1.0/mugen/chars/dArwIn*")
    print("Removing...")
    print()
    for dir in dirs:
        print(dir)
        shutil.rmtree(dir)
    print()
    print("Done!")
    
def kill_logs():
    print("Removing logs..")
    files = glob.glob("Logs/*")
    for f in files:
        os.remove(f)
        
def kill_db_matchtbl():
    print("Removing ALL records from db..")
    db = pymysql.connect("jadonjes.heliohost.org","jadonjes_darwin","HackThisDB1","jadonjes_OUTCOME" )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # Prepare SQL query to DELERE ALL records from the database.
    sql = "TRUNCATE TABLE MatchOutTBL"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       
    except:
       print ("Error: unable to fetch data")
       
def kill_db_matchstats():
    print("Removing ALL records from db..")
    db = pymysql.connect("jadonjes.heliohost.org","jadonjes_darwin","HackThisDB1","jadonjes_OUTCOME" )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    
    # Prepare SQL query to DELERE ALL records from the database.
    sql = "TRUNCATE TABLE GenStatsTBL"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       
    except:
       print ("Error: unable to fetch data")


kill_darwin()
my_super_copy()
kill_logs()

#kill_db_matchtbl()
#kill_db_matchstats()