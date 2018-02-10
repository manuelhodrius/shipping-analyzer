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


# [1] https://pythonadventures.wordpress.com/tag/import-from-parent-directory/
