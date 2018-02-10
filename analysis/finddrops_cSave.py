# counter,timestamp,date,time,cap,x,y,z,xyzsum

import sqlite3
import csv

# make importing from a directory above possible [1]
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))

# import variables
from variables import *
from core.getdata import *
from visual.visual_xyz import *

# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()


################
#    PART II   #
# saving drops #
################

# Find out drops by grouping alls drops with the same id via sqlite statement
# Here, the order is not imporant, as we work with min and max. The correct order is maintained by the previous part
cur.execute("SELECT min(counter), max(counter), drops, min(timestamp), max(timestamp) FROM loggerdata GROUP BY drops")
#cur.execute("SELECT drops, timestamp FROM loggerdata")
alldrops = cur.fetchall()
totaldrops = len(alldrops)
#print(alldrops)





# Save drops in new table of the database, therefore create it
cur.execute("CREATE TABLE IF NOT EXISTS drops (firstrow INTEGER, lastrow INTEGER, dropnr INTEGER, begin REAL, end REAL, dropdur REAL, height REAL)")

# save the values in individual variables and insert them into the new table
dropnr =  0

for dr in range(1, totaldrops):
    d = dr
    firstrow = int(alldrops[d][0])
    lastrow = int(alldrops[d][1])
    begin =  float(alldrops[d][3])
    end = float(alldrops[d][4])
    dropdur = end - begin
    height = 0.5*9.81*(dropdur/1000)*(dropdur/1000)*100  # 0.5 * g * t^2, in seconds; result in millimeters

    # inser only if drop is longer than threshold dropdur
    # d is the new drop number
    if (dropdur > nodrop):
        cur.execute("INSERT INTO drops (firstrow, lastrow, dropnr, begin, end, dropdur, height) VALUES (?, ?, ?, ?, ?, ?, ?)", (firstrow, lastrow, dropnr, begin, end, dropdur, height))

        dropnr =  dropnr + 1

        # Give out the findings
        print ("Drop " + str(dropnr) + " lasted " + str(round(dropdur,2)) + " ms and was from a height of " + str(round((height),2)) + " cm.")

conn.commit()

