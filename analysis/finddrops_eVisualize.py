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


###################
#     FINALE      #
# visualize drops #
###################

# get the drops from the freshly made table drops
cur.execute("SELECT begin, end, dropnr, dropdur, height FROM drops ORDER BY begin ASC")
data = cur.fetchall()

end = len(data)
for x in range(0,end):
    try:
        lower = data[x][0] - dropboundary
        upper = data[x][1] + dropboundary
        #print(lower, "|", data[x][0], "||", data[x][1], "|", upper)
        filename = ("results/visual/drops/dropevent " + str(data[x][2]) + ".png")
        #filename = ""
        headline = "Drop event " + str(data[x][2]) + ", " + str(round((data[x][3]),2)) + " ms, " + str(round((data[x][4]),2)) + " cm"
        line = (data[x][0], data[x][1])
        xyzplotmil(lower, upper, filename, headline, line)
    except:
        continue
        

# [1] https://pythonadventures.wordpress.com/tag/import-from-parent-directory/
