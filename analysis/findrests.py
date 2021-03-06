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

##########
# THEORY #
##########

# do not cycle over periods of time. It is mouch easier: 
# when not moving, every redout has a similar value than the readout before. 
# Therefore, all sections with similar values are rests, interrupted by movement (where the values are not similar)


###############
# PREPARATION #
###############

# add new column for rest number
cur.execute("ALTER TABLE loggerdata ADD COLUMN restnumber INTEGER")
cur.execute("ALTER TABLE loggerdata ADD COLUMN restormovement TEXT")

# add new table where the rests finally are saved in an orderly manner
cur.execute("CREATE TABLE IF NOT EXISTS rests (rowfrom INTEGER, rowto INTEGER, time1 REAL, time2 REAL, timediff REAL, isrest TEXT, orientation TEXT)")

# Get the number of all cells
cur.execute('SELECT COUNT(*) FROM loggerdata')
totalcells, = (cur.fetchall()[0])
print(totalcells)


#################
#     PART I    #
# finding rests #
#################
# this is similar to finding drops. 

print ("Searching for rests...")

# make list with all lines where xyz a similar value than the one before. 
# order by counter as otherwise the findings are messed up

restnumber = 0  # give the first rest a number
concur = 10     # start out with "enough" findings so that the first finding gets noted. 
writevalue = "" # initialize writevalue

# loop through all lines. x is the number of current entry. 
# No worries about last value, because it gets not processed (range is up to, not including the last value. 
for x in range(0, 100000):
    try:
        cur.execute("SELECT xyzsum FROM loggerdata WHERE counter >= ? AND counter <= ? ORDER BY counter ASC", (x, x+1))
        values = cur.fetchall()
        # get the values for this iteration
        firstval, = values[0]
        lastval, = values[1]
        valdiff = abs(lastval - firstval)
        if (valdiff > restthreshold):
            # if the difference between the values is bigger than the threshold
            # it is moving
            indicator = "moving"
        else:
            # if not, 
            # it is resting
            indicator = "resting"
        # increase the counter for noting the number of concurrent findings
        concur = concur + 1
        if (concur > restconcurthres and writevalue != indicator):
            # only change the writevalue if there were enough concurrent findings
            # this smoothes out "flickering" if there is a lot of action going on
            writevalue = indicator
            # reset the number of concurrent findings
            concur = 0
            # a new rest/movement phase was detected. Increase the counter
            restnumber = restnumber + 1
            print("Number " + str(restnumber) + " detected. It is " + writevalue + ".")
        # finally, write stuff to the database
        cur.execute("UPDATE loggerdata SET restnumber = ? WHERE counter = ?", (restnumber, x,))
        cur.execute("UPDATE loggerdata SET restormovement = ? WHERE counter = ?", (writevalue, x,))
    except:
        continue


####################
#      PART II     #
# distilling rests #
####################

# Then, find all phases
cur.execute("SELECT min(counter), max(counter), min(timestamp), min(time), min(date), max(timestamp), max(time), max(date), restnumber, restormovement FROM loggerdata GROUP BY restnumber ORDER BY restnumber")
phases = cur.fetchall()
#print (phases)

# Save all as csv

# create csv file
csvWriter = csv.writer(open("results/rest_and_movement.csv", "w"))
# write first row
csvWriter.writerow(["startcounter", "endcounter", "startmillis", "starttime", "startdate", "endmillis", "endtime", "enddate", "restnumber", "restormovement"])
#write all other rows
for row in phases:
    csvWriter.writerow(row)


conn.close()
'''
# loop through all lines. x is the number of the current entry
for x in range(0, totalcells):
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

##############################

changecounter = 0
casea = 0

# Sample over data and save counters of rests
print("Sampling over database for rests...")

minxrange = (samples/2)
#maxxrange = (totalcells - (samples/2))
maxxrange = 10

for x in range(minxrange, maxxrange):
    minsample = x - (samples/2)
    maxsample = x + (samples/2)
    print(minsample)
    print(maxsample)
    cur.execute("SELECT max(x), max(y), max(z), avg(x), avg(y), avg(z) FROM loggerdata WHERE counter > ? AND counter < ?", (minsample, maxsample))
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
        cur.execute("UPDATE loggerdata SET rests = ? WHERE counter = ?", ("resting", x,))
        cur.execute("UPDATE loggerdata SET restchange = ? WHERE counter = ?", (changecounter, x,))
        if (casea == 0):
            changecounter = changecounter + 1
        casea = 1
    else:
        cur.execute("UPDATE loggerdata SET rests = ? WHERE counter = ?", ("moving", x,))
        cur.execute("UPDATE loggerdata SET restchange = ? WHERE counter = ?", (changecounter, x,))
        if (casea == 1):
            changecounter = changecounter + 1
        casea = 0
        #print(str(tx) + " | " + str(ty) + " | " + str(tz) + " | movement")

print ("got samples")

# Search for changes, measure them and put them into a new table
# First, create new table
cur.execute("CREATE TABLE IF NOT EXISTS rests (rowfrom INTEGER, rowto INTEGER, time1 REAL, time2 REAL, timediff REAL, isrest TEXT, orientation TEXT)")

# Then, find all rests thanks to restchange
cur.execute("SELECT min(counter), max(counter), min(timestamp), max(timestamp), rests FROM loggerdata GROUP BY restchange")
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
    cur.execute("SELECT avg(x), avg(y), avg(z) FROM loggerdata WHERE counter > ? AND counter < ?", (rowfrom, rowto))
    findor = cur.fetchall()
    isitx = abs(int(findor[0][0]))
    isity = abs(int(findor[0][1]))
    isitz = abs(int(findor[0][2]))
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
        
        
'''
