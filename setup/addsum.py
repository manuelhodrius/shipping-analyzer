import csv, sqlite3, os

c = sqlite3.connect('loggerdata.sqlite')
cur = c.cursor()
#cur.execute("PRAGMA synchronous = OFF")
#cur.execute("PRAGMA journal_mode = OFF")
#cur.execute("isolation_level = NONE")
#cur.execute("ALTER TABLE loggerdata ADD COLUMN xyzsum REAL")
datadir = "data/"

#cur.execute("CREATE INDEX x_ind ON loggerdata(x)")
#cur.execute("CREATE INDEX y_ind ON loggerdata(y)")
#cur.execute("CREATE INDEX z_ind ON loggerdata(z)")

print ("index created")

cur.execute('SELECT COUNT(*) FROM loggerdata')
num, = cur.fetchall()[0]
print ("Adding the sums of " + str(num) + " cells")

limit = num

#Add the values
cur.execute("SELECT (sum(abs(x) + abs(y) + abs(z))) FROM loggerdata WHERE counter < ? GROUP BY rowid ", (limit,))
values = cur.fetchall()
#print (values)

# Add them to column xyzsum
c.execute("BEGIN TRANSACTION")
cur.executemany("UPDATE loggerdata SET xyzsum = ?", values,)

# Test
cur.execute("SELECT * FROM loggerdata WHERE counter < ?", (limit,))
print (cur.fetchall())


c.commit()
c.close()

print ("Sum added")


# counter,timestamp,date,time,cap,x,y,z,

