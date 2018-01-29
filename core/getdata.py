# counter,timestamp,date,time,cap,x,y,z,xyzsum
# helpful: http://www.labri.fr/perso/nrougier/teaching/matplotlib/

import sqlite3

# requesting data from just one line 
def getdata1(line):
    # connect to database
    conn = sqlite3.connect('loggerdata.sqlite')
    cur = conn.cursor()
    
    # select values
    cur.execute("SELECT * FROM loggerdata WHERE counter = ?", (line))

    # save values in variable and return it
    values = cur.fetchall()
    return values


# requesting data from a specific range 
def getdata2(lower, upper):
    # connect to database
    conn = sqlite3.connect('loggerdata.sqlite')
    cur = conn.cursor()
    
    # select values
    cur.execute("SELECT * FROM loggerdata WHERE counter >= ? AND counter <= ? ORDER BY counter", (lower, upper))

    # save values in variable and return it
    values = cur.fetchall()
    return values

# requesting data from a specific range AND a specific column
def getdata3(lower, upper, column):
    # connect to database
    conn = sqlite3.connect('loggerdata.sqlite')
    cur = conn.cursor()

    # select values from database and pass them to alldata (which is a tuple)
    cur.execute("SELECT * FROM loggerdata WHERE counter >= ? AND counter <= ? ORDER BY counter", (lower, upper))
    alldata = cur.fetchall()

    # get all values of column from alldata in the range [1]
    values = [x[column] for x in alldata]

    return values


#[1] https://stackoverflow.com/questions/22412258/get-the-first-element-of-each-tuple-in-a-list-in-python
