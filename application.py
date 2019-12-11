#!/usr/local/var/pyenv/shims/python3
#!python3
import psycopg2
import os
import pymongo
import database

if __name__ == '__main__':
    HOST = 'localhost'
    DBNAME = 'project'
    USER = 'project'
    PASSWORD = 'project'

    conn_string = "host=%s dbname=%s user=%s password=%s" % (HOST, DBNAME, USER, PASSWORD)
    conn = psycopg2.connect(conn_string)

    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    mydb = myclient['nyc']
    col = mydb['geo']
    fav = mydb['favor']
    fav.remove()

    while True:

        mode = input("--- Mode Select ---\n\n1. NYC Air Quality\n2. NYC Liquor\n3. NYC Airbnb\n4. NYC Crime\n5. Hybrid Airbnb & Crime\n6. Hybrid Liquor Store & Crime\nq. Quit\n\nEnter here: ")
        if mode == '1':
            database.airquality_query(conn)
        elif mode == '2':
            database.liquor_query(conn)
        elif mode == '3':
            database.abnyc_query(conn)
        elif mode == '4':
            database.crime_query(conn)
        elif mode == '5':
            database.crime_airbnb(conn, col, fav)
        elif mode == '6':
            database.crime_liquor(conn, col)
        else: 
            break


    # DELETE FROM crime WHERE cmplnt_num=211843983 OR cmplnt_num=821425869 OR cmplnt_num=414788103  OR cmplnt_num=148685327;
    # DELETE FROM crime_geo WHERE cmplnt_num=211843983 OR cmplnt_num=821425869 OR cmplnt_num=414788103  OR cmplnt_num=148685327;
