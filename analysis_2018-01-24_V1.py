import os

#delete old database
if (os.path.isfile('loggerdata.sqlite') == True):
    os.system('rm loggerdata.sqlite')

#crete database
import createdb
import data2sqlite
execfile('dbtest.py')

print ('\nFinished with writing database.')

#Analyze data

import readfile

# Drops

