import csv, sqlite3, os
import glob

con = sqlite3.connect('loggerdata.sqlite')
cur = con.cursor()
#cur.execute("CREATE TABLE t (col1, col2);") # use your column names here

datadir = "data/"

newfile = True

# get files
searchpath = datadir + "*.csv"
files = glob.glob(searchpath)

for filenum in range (0, len(files)):
    filelocation = files[filenum]
    if (os.path.isfile(filelocation) == True):
        with open(filelocation,'rb') as fin: # `with` statement available in 2.5+
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin, ['counter', 'timestamp', 'date', 'time', 'cap', 'x', 'y', 'z', 'xyzsum']) # comma is default delimiter
            to_db = [(i['counter'], i['timestamp'], i['date'], i['time'], i['cap'], i['x'], i['y'], i['z'], i['xyzsum']) for i in dr]

        cur.executemany("INSERT INTO loggerdata ('counter', 'timestamp', 'date', 'time', 'cap', 'x', 'y', 'z', 'xyzsum') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
        con.commit()
        print ("File " + str(filenum + 1) + " saved in database")
        filenum = filenum + 1
    else:
        newfile = False
con.close()
print ("All files are imported")


# counter,timestamp,date,time,cap,x,y,z,

