# counter,timestamp,date,time,cap,x,y,z,xyzsum
# helpful: http://www.labri.fr/perso/nrougier/teaching/matplotlib/

import sqlite3
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np


# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()

graphArray = []


cur.execute("SELECT x, y, z, timestamp, date, time FROM loggerdata WHERE rowid > ? AND rowid < ?", (0, 30000))
data = cur.fetchall()
#print ([x[0] for x in data])
xdata = [x[0] for x in data]
ydata = [x[1] for x in data]
zdata = [x[2] for x in data]
timestamp = [(x[3]) for x in data]
date = [(x[4]) for x in data]
time = [(x[5]) for x in data]
xmax = len(data)
nummaygrid = round((xmax/10),0)
nummingrid = nummaygrid / 10


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

ax.set_xlabel("milliseconds in $ms$")
ax.set_ylabel("acceleration in $m/s^2$")
ax.set_title("Acceleration of X, Y and Z Axis from\n" + str(min(date)) + " at " + str(min(time)))

ax.set_frame_on(False)

ax.set_aspect('auto')

ax.plot(timestampnorm, xdata, label='x acceleration', linewidth=0.6, color = "#A95260")
ax.plot(timestampnorm, ydata, label='y acceleration', linewidth=0.6, color = "#E7BE2B")
ax.plot(timestampnorm, zdata, label='z acceleration', linewidth=0.6, color = "#496391")

# Size
fig.set_size_inches(16, 6)
fig.tight_layout()

# Legend
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.x1 * 0.95, box.height * 0.9]) # shrink plot for legend [1]
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), frameon = False, ncol = 3)


#plt.show()
figname = "plot_" + str(min(date)) + "_" + str(min(time) + ".png")
figname = figname.replace("/", "_")
plt.savefig(str(figname), dpi=300, transparent=False)



#[1] https://stackoverflow.com/questions/4700614/how-to-put-the-legend-out-of-the-plot
#[2] https://stackoverflow.com/questions/4918425/subtract-a-value-from-every-number-in-a-list-in-python
