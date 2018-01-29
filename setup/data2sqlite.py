# counter,timestamp,date,time,cap,x,y,z,xyzsum

import csv, sqlite3, os
import glob

# connect to database
con = sqlite3.connect('loggerdata.sqlite')
cur = con.cursor()

# select directory and set newfile to true
datadir = "data/"
newfile = True

# get files
searchpath = datadir + "*.csv"
files = glob.glob(searchpath)

# loop through files, get number by counting return from glob
for filenum in range (0, len(files)):
    filelocation = files[filenum]

    # test if file exist and proceed if true
    if (os.path.isfile(filelocation) == True):

        # Set column titles for csv reader
        columntitles = ['counter', 'timestamp', 'date', 'time', 'cap', 'x', 'y', 'z','xyzsum']

        # open file
        with open(filelocation) as fin:
            # get csv dictreader element. Delimiter would not be necesary
            dr = csv.DictReader(fin, fieldnames = columntitles, delimiter=',')

            # loop through lines an write them into csvcontent
            csvcontent = [(row['counter'], row['timestamp'], row['date'], row['time'], row['cap'], row['x'], row['y'], row['z'], row['xyzsum']) for row in dr]
            
            # save to_db into database
        cur.executemany("INSERT INTO loggerdata ('counter', 'timestamp', 'date', 'time', 'cap', 'x', 'y', 'z', 'xyzsum') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", csvcontent)

        # commit to database
        con.commit()
        
        # prompt info to console
        print ("File " + filelocation + " saved in database")
        filenum = filenum + 1
    
    # stop loop by making newfile False
    else:
        newfile = False

# close database connection
con.close()

# prompt to console
print ("All files are imported")

