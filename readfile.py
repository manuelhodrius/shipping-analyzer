# counter,timestamp,date,time,cap,x,y,z,

import sqlite3

def connect():
    conn = sqlite3.connect('loggerdata.sqlite')
    c = conn.cursor()
    return c

c = connect()

#def give(rownum)
#for row in c.execute('SELECT counter, timestamp FROM loggerdata LIMIT 1 OFFSET 5'):
for row in c.execute('SELECT counter, timestamp, x, y FROM loggerdata WHERE x < 0.04 AND y < 0.04'):
        print row
