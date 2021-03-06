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


###############
# PREPARATION #
###############

# add new column for drops
cur.execute("ALTER TABLE loggerdata ADD COLUMN drops TEXT")


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
        diff = (currval - preval)
        
        #if the current entry is not more than [dropdiff] after the previous
        if (diff > dropdiff): 
            # increase the dropcounter and prompt the finding
            dropcounter = dropcounter + 1
            print ("Drop no. " + str(dropcounter) + " detected")

    # either way, save the finding in loggerdata in the new column. 
    # this enables to generate a table with the drops in the next part
    cur.execute("UPDATE loggerdata SET drops = ? WHERE counter = ?", (dropcounter, currval,))



################
#    PART II   #
# saving drops #
################

# Find out drops by grouping alls drops with the same id via sqlite statement
# Here, the order is not imporant, as we work with min and max. The correct order is maintained by the previous part
cur.execute("SELECT min(counter), max(counter), drops, min(timestamp), max(timestamp) FROM loggerdata GROUP BY drops")
alldrops = cur.fetchall()
totaldrops = len(alldrops)
print(totaldrops)

# Save drops in new table of the database, therefore create it
cur.execute("CREATE TABLE IF NOT EXISTS drops (firstrow INTEGER, lastrow INTEGER, dropnr INTEGER, begin REAL, end REAL, dropdur REAL, height REAL)")

# save the values in individual variables and insert them into the new table
for dr in range(1, totaldrops):
    d = dr
    firstrow = int(alldrops[d][0])
    lastrow = int(alldrops[d][1])
    dropnr =  int(alldrops[d][2])
    begin =  float(alldrops[d][3])
    end = float(alldrops[d][4])
    dropdur = end - begin
    height = 0.5*9.81*(dropdur/1000)*(dropdur/1000)*1000  # 0.5 gt2, in seconds; result in millimeters

    # inser only if drop is longer than threshold dropdur
    # d is the new drop number
    if (dropdur > nodrop):
        cur.execute("INSERT INTO drops (firstrow, lastrow, dropnr, begin, end, dropdur, height) VALUES (?, ?, ?, ?, ?, ?, ?)", (firstrow, lastrow, d, begin, end, dropdur, height))

# Give out the findings
    print ("Drop " + str(dropnr) + " lasted " + str(round(dropdur,2)) + " ms and was from a height of " + str(round((height*100),1)) + " cm.")

conn.commit()



###################
#     PART III    #
# output csv file #
###################

# output csv
cur.execute("SELECT * FROM drops ORDER BY dropnr")
rows = cur.fetchall()

csvWriter = csv.writer(open("results/drops.csv", "w"))
csvWriter.writerow(["firstrow", "lastrow", "dropnr", "begin", "end", "dropdur", "height"])
for row in rows:
    csvWriter.writerow(row)


###################
#     FINALE      #
# visualize drops #
###################

# get the drops from the freshly made table drops
cur.execute("SELECT begin, end, dropnr, dropdur, height FROM drops ORDER BY dropnr ASC")
data = cur.fetchall()

end = len(data)
for x in range(0,end):
    try:
        lower = data[x][0] - dropboundary
        upper = data[x][1] + dropboundary
        filename = ("results/visual/dropevent " + str(data[x][2]) + ".png")
        headline = "Drop event " + str(data[x][2]) + ", " + str(round((data[x][3]),2)) + " ms, " + str(round((data[x][4]),2)) + " cm"
        xyzplotmil(lower, upper, filename, headline)
    except:
        continue
        

# [1] https://pythonadventures.wordpress.com/tag/import-from-parent-directory/
