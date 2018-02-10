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


#################
#     PART I    #
# finding drops #
#################

print ("Searching for drop events...")

# make list with all lines where xyz shows a drop by having a value smaller than the threshold 
# then save the counter for every finding
# order by counter as otherwise the findings are messed up
cur.execute("SELECT counter FROM loggerdata WHERE xyzsum < ? ORDER BY counter ASC", (droplimit,))

# save in variable
lines = cur.fetchall()
#print (lines[1:100])

# prompt the number of lines found
numlinesfound = len(lines)
print (str(numlinesfound) + " lines found")

# initiate dropcounter
dropcounter = 0


for x in range(0, numlinesfound):
    currval, = lines[x]
    preval, = lines[x-1]
    diff = currval - preval
    if (diff < dropdiff):
        cur.execute("UPDATE loggerdata SET drops = ? WHERE counter = ?", (dropcounter, currval,))
    else:
        dropcounter = dropcounter + 1
        cur.execute("UPDATE loggerdata SET drops = ? WHERE counter = ?", (dropcounter, currval,))
        print ("Drop no. " + str(dropcounter) + " detected")



'''
x = 1
diff = 0

while (x <= numlinesfound):
    droplen = 0

    zeroline = lines[x]

    while (diff < dropdiff):
        currval, = lines[x]
        preval, = lines[x-1]
        diff = currval - preval

        droplen = droplen + 1

        x = x + 1

        cur.execute("UPDATE loggerdata SET drops = ? WHERE counter = ?", (dropcounter, currval,))


    endline = lines[x]

    print ("Drop no. " + str(dropcounter) + " detected from line " + str(zeroline) + " to " + str(endline))

    dropcounter = dropcounter + 1






# loop through all lines. x is the number of current entry
for x in range(0, numlinesfound):
    # save the counter number of current finding
    currval, = lines[x]

    # don't ignore the first value, but execute the rest not when looping through the first line
    if (x > 0):
        # get the previous line number
        preval, = lines[x-1] 

        # calculate the difference between the line numbers to see 
        # if it is a new drop (big difference) 
        # or an ongoing drop (small difference) 
        diff = abs(currval - preval)
        
        #if the current entry is not more than [dropdiff] after the previous
        if (diff > dropdiff): 
            # increase the dropcounter and prompt the finding
            dropcounter = dropcounter + 1
            print ("Drop no. " + str(dropcounter) + " detected")

    # either way, save the finding in loggerdata in the new column. 
    # this enables to generate a table with the drops in the next part
    cur.execute("UPDATE loggerdata SET drops = ? WHERE counter = ?", (dropcounter, currval,))
    #print("set" + str(dropcounter) + str(currval))

'''

conn.commit()