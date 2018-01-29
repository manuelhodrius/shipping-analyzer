# source: https://stackoverflow.com/questions/4568154/sort-an-entire-sqlite-table

#colums: counter, timestamp, date, time, cap, x, y, z, xyzsum

import sqlite3

print ("Improving table structure...")

# Connecting to the database file
conn = sqlite3.connect("loggerdata.sqlite")
c = conn.cursor()

# create new table
c.execute("CREATE TABLE sorted (counter INTEGER,timestamp TEXT,date TEXT, time TEXT, 'cap' 'REAL', 'x' 'REAL', 'y' 'REAL', 'z' 'REAL', 'xyzsum' 'REAL')")

# insert ordered values from loggedata
c.execute("INSERT INTO sorted (counter, timestamp, date, time, cap, x, y, z, xyzsum) SELECT counter, timestamp, date, time, cap, x, y, z, xyzsum FROM loggerdata ORDER BY timestamp")

# delete old table
c.execute("DROP TABLE loggerdata")

# rename ordered table into old obe
c.execute("ALTER TABLE sorted RENAME TO loggerdata")

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
print ("Database sorted and ready.")
