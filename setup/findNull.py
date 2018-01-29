import csv, sqlite3, os
import glob
import sys

con = sqlite3.connect('loggerdata.sqlite')
cur = con.cursor()
#cur.execute("CREATE TABLE t (col1, col2);") # use your column names here

datadir = "data/"

newfile = True

# get files
searchpath = datadir + "*.csv"
files = glob.glob(searchpath)


# [1] https://stackoverflow.com/questions/7894856/line-contains-null-byte-in-csv-reader-python
# https://stackoverflow.com/questions/4166070/python-csv-error-line-contains-null-byte
#https://stackoverflow.com/questions/17176542/remove-specific-character-from-a-csv-file-and-rewrite-to-a-new-file




for filenum in range (0, len(files)):
    filelocation = files[filenum]
    reader = csv.reader(open(filelocation, "rb"))
    try:
        for row in reader:
            #print 'Row read successfully!', row
            dfdfs = 0
    except csv.Error, e:
        print("\n/!\ \nCorrupt file found: " + filelocation)
        #print repr(open(filelocation, 'rb').read(200)) # dump 1st 200 bytes of file
        #data = open(filelocation, 'rb').read()
        #errpos = data.find('\x00')
        #print ("None value near " + errpos)
        print ("Please look into this file (there might be corrupt caracters at the end) or delete it, thereafter start the analysis again.")
        sys.exit()                      # I did not have the ressources to solve this. Fixing by hand was the quickest solution. Sorry. 

'''        # delete last line
        f = open(filelocation, "r+w")
        lines=f.readlines()
        lines=lines[:-1]

        new_lines = [x if (x != '\0') else '' for x in lines]
        
        cWriter = csv.writer(f, delimiter=',')
        for line in new_lines:
            cWriter.writerow(new_lines)
'''

'''
        for line in csv.reader(filelocation):
            line = str(line)
            new_line = str.replace(line,'','')
            writer = csv.writer(filelocation)
            writer.writerow(new_line.split(','))
'''

        #print('file %s, line %d: %s' % (filename, reader.line_num, e))

#    reader = csv.reader(x.replace('\0', '') for x in fin) # for errors because of None character. [1]
'''
    if (os.path.isfile(filelocation) == True):
        with open(filelocation,'rb') as fin: # `with` statement available in 2.5+ also: [1]
            # csv.DictReader uses first line in file for column headings by default
            dr = csv.DictReader(fin, ['counter', 'timestamp', 'date', 'time', 'cap', 'x', 'y', 'z', 'xyzsum']) # comma is 
   '''         
            
            

# counter,timestamp,date,time,cap,x,y,z,
# [1] https://stackoverflow.com/questions/7894856/line-contains-null-byte-in-csv-reader-python
