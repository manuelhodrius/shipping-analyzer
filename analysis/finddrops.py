# counter,timestamp,date,time,cap,x,y,z,xyzsum

import sqlite3
import csv

# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()
cur.execute("ALTER TABLE loggerdata ADD COLUMN drops TEXT")  # Add new column for findings

# Set limits
droplimit = 0.8

#make list with all lines and save the rowid for every finding
cur.execute("SELECT rowid FROM loggerdata WHERE xyzsum < ?", (droplimit,))
lines = cur.fetchall()
numlinesfound = len(lines)
print (str(numlinesfound) + " lines found")

dropcounter = 0

# loop through all lines. x is number of current entry
for x in range(0, numlinesfound):
    currval, = lines[x] #save line number of current finding
    prefval, = lines[x-1] # get previous line number
    diff = (currval - prefval)
    if (diff > 20): #if the current entry is not more than a few entries after the previous
        dropcounter = dropcounter + 1
        print ("Drop no. " + str(dropcounter) + " detected")
    cur.execute("UPDATE loggerdata SET drops = ? WHERE rowid = ?", (dropcounter, currval,))
    dd = 3

# Find out drops by grouping alls drops with the same id via sqlite statement
cur.execute("SELECT min(rowid), drops, min(timestamp), max(timestamp) FROM loggerdata GROUP BY drops")
alldrops = cur.fetchall()
totaldrops = len(alldrops)
print(totaldrops)

# Save drops in new table of database
cur.execute("CREATE TABLE IF NOT EXISTS drops (firstrow INTEGER, dropnr INTEGER, begin REAL, end REAL, dropdur REAL, height REAL)")

for dr in range(1, totaldrops):
    d = dr
    firstrow = int(alldrops[d][0])
    dropnr =  int(alldrops[d][1])
    begin =  float(alldrops[d][2])
    end = float(alldrops[d][3])
    dropdur = end - begin
    height = 0.5*9.81*(dropdur/1000)*(dropdur/1000)  # 0.5 gt2

    cur.execute("INSERT INTO drops (firstrow, dropnr, begin, end, dropdur, height) VALUES (?, ?, ?, ?, ?, ?)", (firstrow, dropnr, begin, end, dropdur, height))

# Give out the findings
    print ("Drop " + str(dropnr) + " lasted " + str(round(dropdur,2)) + " ms and was from a height of " + str(round((height*100),1)) + " cm.")

conn.commit()


# output csv
cur.execute("SELECT * FROM drops ORDER BY firstrow")
rows = cur.fetchall()

csvWriter = csv.writer(open("results/drops.csv", "w"))
csvWriter.writerow(["firstrow", "dropnr", "begin", "end", "dropdur", "height"])
for row in rows:
    # do your stuff
    csvWriter.writerow(row)
        

