import sqlite3
import csv

import numpy as np
import matplotlib.pyplot as plt
import math

# make importing from a directory above possible [1]
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))
from variables import *
from core.detect_peaks import detect_peaks

# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()

#################
# GET PEAK DATA #
#################

# get first and last millisecond count from database
cur.execute("SELECT min(timestamp), max(timestamp) FROM loggerdata")
minmax = cur.fetchall()
minmax, = minmax
minmillis = minmax[0]
maxmillis = minmax[1]

# get all data from database and save it into variables
cur.execute("SELECT date, time, timestamp, xyzsum FROM loggerdata")
data = cur.fetchall()
xyzsum = [(x[3]) for x in data]
alldat = [(x[0:5]) for x in data]

# detect all peaks and select data of peaks (with timestamp, date, time and peak value)
# as the xyz data are used, there are no valleys - the data is always positive
ind = detect_peaks(xyzsum, mph=peakthres, show=False) # [1]
print(str(len(ind)) + " peaks found")
ind_data = [alldat[x] for x in ind]
ind_peaks = [xyzsum[x] for x in ind]

###########################
# EXPORT PEAK DATA AS CSV #
###########################

csvWriter = csv.writer(open("results/peaks.csv", "w"))
csvWriter.writerow(["date", "time", "timestamp", "peakvalue"])
for row in ind_data:
    csvWriter.writerow(row)
print ("Peaks successfully saved as csv file.")


#########################
# EXPORT HISTOGRAM DATA #
#########################

# get min and max values (rounded up rep. down)
maxval = (math.ceil(max(ind_peaks)))
minval = (math.floor(min(ind_peaks)))

# get tuple with list for bins from min to max value with step width
step = 0.5
tup = np.arange(minval, (maxval + step), step)
tup = tuple(tup)

# use numpy funcion to generate hisogram data
hist, bin_edges = np.histogram(ind_peaks, bins=(tup), density=False)
hist = tuple(hist)
bin_edges = tuple(bin_edges)

# combine both tuples in new array
histdat = [(bin_edges[k], hist[k]) for k in xrange(0,len(bin_edges)-1)]

# export histogram data to csv file
csvWriter = csv.writer(open("results/peaks_histogram.csv", "w"))
csvWriter.writerow(["bin", "number"])
for row in histdat:
    csvWriter.writerow(row)
print ("Histogram of peaks successfully saved as csv file.")




fig = plt.subplots(figsize = (12,6), tight_layout=True)
ax = plt.axes()
ax.set_axisbelow(True)
ax.grid(color='#dddddd', linestyle='-', linewidth=0.5)
ax.set_frame_on(False)

ax.set_xlabel("accelerations in $m/s^2$")
ax.set_ylabel("number of values")

# plot histogram using mathplotlib
y_pos = np.arange(len(hist))
plt.bar(y_pos,hist, color="#A95260")
plt.xticks(y_pos, bin_edges)
plt.title('Peaks; threshold = ' + str(peakthres))

# save histogram in results folder
plt.savefig(str("results/peak_histogram.png"), dpi=300, transparent=False)
print("Histogram saved.")

#plt.show()



# [1]: https://github.com/demotu/BMC/blob/master/notebooks/DetectPeaks.ipynb