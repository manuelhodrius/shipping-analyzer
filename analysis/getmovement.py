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
#from core.detect_peaks import detect_peaks


#'''
# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()


#############
# FUNCTIONS #
#############

# calculate load factor
def loadfactor(vals):
    # max values
    max_std = 15

    # calculate standard deviation, maximum and average
    maxx = np.amax(vals)
    avg = np.average(vals)
    std = np.std(vals, axis=0)

    # weigh values
    # when there is no movement, the result be near zero. 
    # If there is no movement, max and avg should be about 0.981; std should be near 0. 
    # Therefore, substract 0.981 from max and avg to get 0 when there is no movement. 

    diff = 0.981
    
    maxx = abs(maxx - diff)
    avg = abs(avg - diff)

    # calculate and return result as the sum of the three (weighted) factors
    res = maxx + avg + std
    return res


# get results for window
def window(start, end): 
    # get data from database
    cur.execute("SELECT xyzsum FROM loggerdata WHERE timestamp >= ? AND timestamp <= ?", (start, end))
    data = cur.fetchall()
    data = [x[0] for x in data]
    #data = tuple(data)
    return data


# export data as csv
def write_csv(results, file = "movefactor"):
    filename = "results/" + file + ".csv"
    csvWriter = csv.writer(open(filename, "w"))
    csvWriter.writerow(["timestamp", "factor"])
    for row in results:
        csvWriter.writerow(row)
    print ("Movement analysis successfully saved as csv file.")


# Plot
def plot_data(plotdata, file, windowwidth):
    pass
    fig = plt.subplots(figsize = (12,6), tight_layout=True)
    ax = plt.axes()
    ax.get_yaxis().set_visible(False)
    ax.set_frame_on(False)
    ax.set_title("Movement during journey\nResolution: " + str(windowwidth) + " seconds per bar")
    #ax.set_xlabel("time in $m/s^2$")

    # plotdata
    #NaN = np.nan
    #plotdata = [0,NaN,1,2,3,4,5,6,7,8,9,10]
    plotdata = [x[1] for x in results]

    plotdata = [plotdata]
    imgplot = plt.imshow(plotdata, interpolation='nearest', aspect='auto', vmin=0, vmax=5)
    imgplot.set_cmap('RdYlBu_r')

    #plt.plot(plotdata)

    # save histogram in results folder
    filename = "results/" + file + ".png"
    plt.savefig(filename, dpi=600, transparent=False)
    print("Plot saved.")

    #plt.show()


# Get min and max milliseconds from database
def getminmillis():
    # get first and last millisecond count from database
    cur.execute("SELECT min(timestamp), max(timestamp) FROM loggerdata")
    minmax = cur.fetchall()
    minmax, = minmax
    minmillis = minmax[0]
    maxmillis = minmax[1]

    return minmillis, maxmillis


# iterate over data with a sliding window and calculate factor for every window
def dowindow(windowwidth):
    minmillis, maxmillis = getminmillis()
    millis = minmillis
    results = []
    windowwidth = windowwidth*1000
    ####
    #maxmillis = minmillis+windowwidth*5
    ####
    while (millis <= maxmillis):
        winstart = millis
        winend = millis + windowwidth
        
        try:
            # get data from the window
            data = window(winstart, winend)
            # calculate factor
            factor = loadfactor(data)

        except:
            # set factor to NaN value (that is not plotted later)
            factor = np.nan
            #print("nodata")

        # put everything into tuple and append it to the 'results' list 
        res = (winstart, factor)
        res = tuple(res)
        #print(res)
        results.append(res)

        # next millis
        millis = millis + windowwidth

    return results



###########
# EXECUTE #
###########

# Iterate onece or multiple times over data with different resolutions (= window widths)
for wind_width in (1,10,60,120,600):
    print("\nGenerating files using a sliding window of " + str(wind_width) + " seconds.")
    # define file name
    filename = "move/movefactor_" + str(wind_width)

    # get data
    results = dowindow(wind_width)
    # export csv
    write_csv(results, filename)
    # plot data
    plot_data(results, filename, wind_width)
