import csv, sqlite3, os

con = sqlite3.connect('loggerdata.sqlite')
cur = con.cursor()
#cur.execute("CREATE TABLE t (col1, col2);") # use your column names here

datadir = "data/"

newfile = True
num = 1

while(newfile == True):
    filename = "loggerdata_2018-01-22_" + str(num) + ".csv"
    filelocation = datadir + filename
    if (os.path.isfile(filelocation) == True):
        with open(filelocation,'rb') as fin: # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin, ['counter', 'timestamp', 'date', 'time', 'cap', 'x', 'y', 'z']) # comma is default delimiter
            to_db = [(i['counter'], i['timestamp'], i['date'], i['time'], i['cap'], i['x'], i['y'], i['z']) for i in dr]

        cur.executemany("INSERT INTO loggerdata ('counter', 'timestamp', 'date', 'time', 'cap', 'x', 'y', 'z') VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        print ("File " + str(num) + " saved in database")
        num = num + 1
    else:
        newfile = False
con.close()
print ("All files are imported")


# counter,timestamp,date,time,cap,x,y,z,

