import sqlite3

sqlite_file = 'loggerdata.sqlite'    # name of the sqlite database file
table_name = 'loggerdata'  # name of the table to be created


#colums: counter, timestamp, date, time, cap, x, y, z, temp, pressure, humidity


# Connecting to the database file
conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

#int = INTEGER

# Creating a new SQLite table with 1 column
#c.execute("CREATE TABLE {tn} ('{cn}' {ct} PRIMARYKEY)"\
c.execute("CREATE TABLE {tn} ('{cn}' {ct})"\
        .format(tn=table_name, cn='counter', ct='INTEGER'))

# Adding the columns
c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='timestamp', ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='date', ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='time', ct='TEXT'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='cap', ct='REAL'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='x', ct='REAL'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='y', ct='REAL'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='z', ct='REAL'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='temp', ct='REAL'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='preassure', ct='REAL'))

c.execute("ALTER TABLE {tn} ADD COLUMN {cn} {ct}"\
        .format(tn=table_name, cn='humidity', ct='REAL'))

# Committing changes and closing the connection to the database file
conn.commit()
conn.close()
