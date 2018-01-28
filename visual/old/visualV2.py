# counter,timestamp,date,time,cap,x,y,z,xyzsum
# helpful: http://www.labri.fr/perso/nrougier/teaching/matplotlib/

import sqlite3
import matplotlib.pyplot as plt


# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()

graphArray = []


cur.execute("SELECT x, y, z, timestamp FROM loggerdata WHERE rowid > ? AND rowid < ?", (0, 200))
data = cur.fetchall()
#print ([x[0] for x in data])
xdata = [x[0] for x in data]
ydata = [x[1] for x in data]
zdata = [x[2] for x in data]
#xyzsum = [x[3] for x in data]
#counter = [x[4] for x in data]
timestamp = [x[3] for x in data]
xmax = len(data)

#plt.plot([1,2,3,4])
#lines = plt.plot(data)

fig = plt.figure(figsize=(20,4), frameon=False, linewidth = 0.1, tight_layout = True)
#ax = fig.add_subplot(111)

#fig.add_axes(label='axes1')

plt.plot(xdata, timestamp, linewidth=0.5, color = '#0000ff', label="x acceleration")
#plt.plot(ydata, linewidth=0.5, color = '#00ff00', label="y acceleration")
#plt.plot(zdata, linewidth=0.5, color = '#ff0000', label="z acceleration")

# diagram options
plt.tick_params(width=.2)
#plt.minorticks_on()
plt.grid(True, linewidth=0.1, color = '#aaaaaa',which='both')
plt.xlim(0, xmax)

ax = plt.subplots(1)
ax.set_yticks(timestamp)

# labels
plt.title('Acceleration Data')
plt.xlabel('cycles')
plt.ylabel('acceleration in m/s^2')
plt.legend()


#fig.plot(xdata)
fig.savefig('fig1.png', dpi = 600)

#plt.savefig("exercice_2.png", dpi=300, transparent=True)

plt.show()



#plt.hist(xdata)


#xyzsum, counter, timestamp 
