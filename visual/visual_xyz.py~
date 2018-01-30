# counter,timestamp,date,time,cap,x,y,z,xyzsum
# helpful: http://www.labri.fr/perso/nrougier/teaching/matplotlib/

import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

# make importing from a directory above possible [1]
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '../'))

# import variables
from variables import *
from core.getdata import *


#####################
# PLOT WITH COUNTER #
#####################

def xyzplot2(lower, upper, filename, headline):

    # prompt info
    print ("generating " + filename)

    # connect to database
    conn = sqlite3.connect('loggerdata.sqlite')
    cur = conn.cursor()

    graphArray = []


    cur.execute("SELECT x, y, z, timestamp, date, time, counter, xyzsum FROM loggerdata WHERE counter >= ? AND counter <= ?", (lower, upper))
    data = cur.fetchall()
    #print ([x[6] for x in data])
    xdata = [x[0] for x in data]
    ydata = [x[1] for x in data]
    zdata = [x[2] for x in data]
    timestamp = [(x[3]) for x in data]
    date = [(x[4]) for x in data]
    time = [(x[5]) for x in data]
    xyzsum = [(x[7]) for x in data]
    xmax = len(data)
    if (xmax > 10):
        nummaygrid = round((xmax/10),0)
        nummingrid = nummaygrid / 10
    else:
        nummaygrid = 10
        nummingrid = 1

    # normalize timestamp [2]
    timestampmin = float(min(timestamp))
    timestampnorm = [(float(x) - timestampmin) for x in timestamp]


    # Plot
    fig = plt.figure()
    plt.grid(color='#dddddd', linestyle='-', linewidth=0.5)

    # Change Axes class
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(nummaygrid))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(nummingrid))
    ax.set_xlim(0, xmax)

    # Labels
    ax.set_xlabel("milliseconds in $ms$")
    ax.set_ylabel("acceleration in $m/s^2$")
    # headline is optional and replaced with a generic one if not given
    datetime = "\n" + str(min(date)) + " at " + str(min(time))
    if (headline == ""):
        ax.set_title("Acceleration of X, Y and Z Axis from" + datetime)
    else: 
        ax.set_title(str(headline) + datetime)

    ax.set_frame_on(False)

    ax.set_aspect('auto')

    ax.plot(timestampnorm, xdata, label='x acceleration', linewidth=0.6, color = "#A95260")
    ax.plot(timestampnorm, ydata, label='y acceleration', linewidth=0.6, color = "#E7BE2B")
    ax.plot(timestampnorm, zdata, label='z acceleration', linewidth=0.6, color = "#496391")
    ax.plot(timestampnorm, xyzsum, label='|x| + |y| + |z|', linewidth=0.6, color = "#555555")

    # Size
    fig.set_size_inches(16, 6)
    fig.tight_layout()

    # Legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.x1 * 0.95, box.height * 0.9]) # shrink plot for legend [1]
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), frameon = False, ncol = 4)

    if (filename != ""):
        #filename = filename.replace("/", "_")
        plt.savefig(str(filename), dpi=300, transparent=False)
    else:
        plt.show()

    # cloes figure, otherwise program gets killed
    plt.close(fig)

####################
# PLOT WITH MILLIS #
####################

def xyzplotmil(lower, upper, filename, headline):

    # prompt info
    print ("generating " + filename)

    # connect to database
    conn = sqlite3.connect('loggerdata.sqlite')
    cur = conn.cursor()

    graphArray = []

    # normalize timestamp -> first row should have timestamp 0
    cur.execute("SELECT timestamp FROM loggerdata WHERE counter = 0")
    mintime = cur.fetchall()
    mintime, = mintime[0]
    
    cur.execute("SELECT x, y, z, timestamp, date, time, counter, xyzsum FROM loggerdata WHERE timestamp >= ? AND timestamp <= ? ORDER BY counter", (lower, upper))
    data = cur.fetchall()
    #print ([x[6] for x in data])
    xdata = [x[0] for x in data]
    ydata = [x[1] for x in data]
    zdata = [x[2] for x in data]
    timestamp = [(x[3]) for x in data]
    date = [(x[4]) for x in data]
    time = [(x[5]) for x in data]
    xyzsum = [(x[7]) for x in data]
    timestampnorm = [(float(x) - mintime) for x in timestamp]
    xmax = max(timestampnorm)
    xmin = min(timestampnorm)

    if (xmax > 10):
        nummaygrid = round((xmax/10),0)
        nummingrid = nummaygrid / 10
    else:
        nummaygrid = 10
        nummingrid = 1



    # Plot
    fig = plt.figure()
    plt.grid(color='#dddddd', linestyle='-', linewidth=0.5)

    # Change Axes class
    ax = plt.axes()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(nummaygrid))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(nummingrid))
    ax.set_xlim(xmin, xmax)

    # Labels
    ax.set_xlabel("milliseconds in $ms$")
    ax.set_ylabel("acceleration in $m/s^2$")
    # headline is optional and replaced with a generic one if not given
    datetime = "\n" + str(min(date)) + " at " + str(min(time))
    if (headline == ""):
        ax.set_title("Acceleration of X, Y and Z Axis from" + datetime)
    else: 
        ax.set_title(str(headline) + datetime)

    ax.set_frame_on(False)

    ax.set_aspect('auto')

    ax.plot(timestampnorm, xdata, label='x acceleration', linewidth=0.6, color = "#A95260")
    ax.plot(timestampnorm, ydata, label='y acceleration', linewidth=0.6, color = "#E7BE2B")
    ax.plot(timestampnorm, zdata, label='z acceleration', linewidth=0.6, color = "#496391")
    ax.plot(timestampnorm, xyzsum, label='|x| + |y| + |z|', linewidth=0.6, color = "#555555")

    # Size
    fig.set_size_inches(16, 6)
    fig.tight_layout()

    # Legend
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.1, box.x1 * 0.95, box.height * 0.9]) # shrink plot for legend [1]
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), frameon = False, ncol = 4)

    if (filename != ""):
        #filename = filename.replace("/", "_")
        plt.savefig(str(filename), dpi=300, transparent=False)
    else:
        plt.show()

    # cloes figure, otherwise program gets killed
    plt.close(fig)

#xyzplotmil(6744569.0864,6746645.6057,"","")

#[1] https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
#[2] https://stackoverflow.com/questions/4918425/subtract-a-value-from-every-number-in-a-list-in-python
