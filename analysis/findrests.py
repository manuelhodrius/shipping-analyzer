# counter,timestamp,date,time,cap,x,y,z,xyzsum

import sqlite3
import csv

# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()
cur.execute("ALTER TABLE loggerdata ADD COLUMN rests TEXT")  # Add new table for rests
cur.execute("ALTER TABLE loggerdata ADD COLUMN restchange TEXT")  # Add new table for orientation
cur.execute("ALTER TABLE loggerdata ADD COLUMN orientation TEXT")  # Add new table for orientation


# Set limits
samples = 500
maxdiff = .2

# Number of all cells
cur.execute('SELECT COUNT(*) FROM loggerdata')
totalcells, = (cur.fetchall()[0])
print(totalcells)

changecounter = 0
casea = 0

# Sample over data and save rowids of rests
print("Sampling over database for rests...")

for x in range(0,(totalcells - samples)):
    cur.execute("SELECT max(x), max(y), max(z), avg(x), avg(y), avg(z) FROM loggerdata WHERE rowid > ? AND rowid < ?", (x, (x + samples)))
    lines = cur.fetchall()
    maxx = lines[0][0]
    maxy = lines[0][1]
    maxz = lines[0][2]
    avgx = lines[0][3]
    avgy = lines[0][4]
    avgz = lines[0][5]
    tx = abs(maxx - avgx)
    ty = abs(maxy - avgy)
    tz = abs(maxz - avgz)
    if (tx < maxdiff and ty < maxdiff and tz < maxdiff):
        cur.execute("UPDATE loggerdata SET rests = ? WHERE rowid = ?", ("resting", x,))
        cur.execute("UPDATE loggerdata SET restchange = ? WHERE rowid = ?", (changecounter, x,))
        if (casea == 0):
            changecounter = changecounter + 1
        casea = 1
    else:
        cur.execute("UPDATE loggerdata SET rests = ? WHERE rowid = ?", ("moving", x,))
        cur.execute("UPDATE loggerdata SET restchange = ? WHERE rowid = ?", (changecounter, x,))
        if (casea == 1):
            changecounter = changecounter + 1
        casea = 0
        #print(str(tx) + " | " + str(ty) + " | " + str(tz) + " | movement")

# Search for changes, measure them and put them into a new table
# First, create new table
cur.execute("CREATE TABLE IF NOT EXISTS rests (rowfrom INTEGER, rowto INTEGER, time1 REAL, time2 REAL, timediff REAL, isrest TEXT, orientation TEXT)")

# Then, find all rests thanks to restchange
cur.execute("SELECT min(rowid), max(rowid), min(timestamp), max(timestamp), rests FROM loggerdata GROUP BY restchange")
changes = cur.fetchall()
totalchanges = len(changes)
#print (changes)
for c in range(1,totalchanges):
#c = 3
    rowfrom = int(changes[c][0])
    rowto = int(changes[c][1])
    time1 = float(changes[c][2])
    time2 = float(changes[c][3])
    timediff = time2 - time1
    isrest = (changes[c][4])

    # test for orientation
    cur.execute("SELECT avg(x), avg(y), avg(z) FROM loggerdata WHERE rowid > ? AND rowid < ?", (rowfrom, rowto))
    findor = cur.fetchall()
    isitx = int(findor[0][0])
    isity = int(findor[0][1])
    isitz = int(findor[0][2])
    itsmax = max(isitx, isity, isitz)
    if (itsmax == isitx):
        orientation = "x"
    if (itsmax == isity):
        orientation = "y"
    if (itsmax == isitz):
        orientation = "z"
    cur.execute("INSERT INTO rests (rowfrom, rowto, time1, time2, timediff, isrest, orientation) VALUES (?, ?, ?, ?, ?, ?, ?)", (rowfrom, rowto, time1, time2, timediff, isrest, orientation))
    print ("While in line " + str(rowfrom) + " to " + str(rowto) + " and with " + str(round((timediff/1000),1)) + " seconds was " + isrest + " in orientation " + orientation + ".")

conn.commit()


# output csv
cur.execute("SELECT * FROM rests ORDER BY rowfrom")
rows = cur.fetchall()

csvWriter = csv.writer(open("results/rests.csv", "w"))
csvWriter.writerow(["rowfrom", "rowto", "time1", "time2", "timediff", "isrest", "orientation"])
for row in rows:
    # do your stuff
    csvWriter.writerow(row)
        
        

