# counter,timestamp,date,time,cap,x,y,z,xyzsum
# helpful: http://www.labri.fr/perso/nrougier/teaching/matplotlib/

import sqlite3
import matplotlib.pyplot as plt


# connect to database
conn = sqlite3.connect('loggerdata.sqlite')
cur = conn.cursor()

graphArray = []


cur.execute("SELECT x, y, z FROM loggerdata WHERE rowid > ? AND rowid < ?", (0, 20000))
data = cur.fetchall()
#print ([x[0] for x in data])
xdata = [x[0] for x in data]
ydata = [x[1] for x in data]
zdata = [x[2] for x in data]
#xyzsum = [x[3] for x in data]
#counter = [x[4] for x in data]
#timestamp = [x[5] for x in data]
xmax = len(data)

#plt.plot([1,2,3,4])
#lines = plt.plot(data)


plt.plot(xdata, linewidth=0.5, color = '#0000ff', label="x acceleration")
plt.plot(ydata, linewidth=0.5, color = '#00ff00', label="y acceleration")
plt.plot(zdata, linewidth=0.5, color = '#ff0000', label="z acceleration")
# diagram options
plt.tick_params(width=1)
plt.grid(True, linewidth=0.5, color = '#aaaaaa')
plt.xlim(0, xmax)
# labels
plt.title('Acceleration Data')
plt.xlabel('cycles')
plt.ylabel('acceleration in m/s^2')
plt.legend()


ax.plot(xdata)
fig.savefig('fig1.png', dpi = 300)

#plt.savefig("exercice_2.png", dpi=300, transparent=True)

plt.show()
#plt.savefig('myfig', )



#plt.hist(xdata)


#xyzsum, counter, timestamp 
