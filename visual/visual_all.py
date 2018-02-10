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


# get minimal an maximal milli counter
cur.execute("SELECT min(timestamp), max(timestamp) FROM loggerdata")
#cur.execute("SELECT timestamp FROM loggerdata WHERE counter = 0")
minmax = cur.fetchall()
minmax, = minmax
minmillis = minmax[0]
maxmillis = minmax[1]

# calculate section length and number of files
diff = maxmillis - minmillis
sectionlength = sectionlength*1000
totaldiagrams = int(round((diff / sectionlength),0))
print(str(totaldiagrams) + " diagramms will be generated.\n")

for x in xrange(0,totaldiagrams):
    print("Generating diagram " + str(x) + " from " + str(totaldiagrams))
    try:
        sectionstart = minmillis + (sectionlength * x)
        sectionend = sectionstart + sectionlength
        filename = ("results/visual/alldata/alldata " + str(x) + ".png")
        #filename = ("alldata " + str(x) + ".png")
        headline = "Drop data from " + str(sectionstart) + "ms until " + str(sectionend) + " ms"
        xyzplotmil(sectionstart, sectionend, filename, "")
    except:
        continue
