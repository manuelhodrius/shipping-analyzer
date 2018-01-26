# counter,timestamp,date,time,cap,x,y,z,

import sqlite3

def connect():
    conn = sqlite3.connect('loggerdata.sqlite')
    c = conn.cursor()
    return c

c = connect()
droplimit = 0.04

#def give(rownum)
#for row in c.execute('SELECT counter, timestamp FROM loggerdata LIMIT 1 OFFSET 5'):

#find drops                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 	
for row in c.execute("SELECT counter, timestamp, x, y FROM loggerdata WHERE x < ? AND y < ? AND z < ?", (droplimit,droplimit,droplimit,)):
        print row
        
#find not drops
#for row in c.execute("SELECT timestamp FROM loggerdata WHERE x < ? AND y < ?", (droplimit,droplimit,)):
#        print row

c.execute("SELECT counter, timestamp FROM loggerdata WHERE x < ? AND y < ?", (droplimit,droplimit,))
print [float(record[0]) for record in c.fetchall()]


