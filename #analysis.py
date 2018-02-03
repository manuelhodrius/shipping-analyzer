import os

# Delete old database
if (os.path.isfile('loggerdata.sqlite') == True):
    os.system('rm loggerdata.sqlite')

# Fix files
print("Searching for corrupt files...")
import setup.findNull

# Create database
import setup.createdb
import setup.data2sqlite
execfile('setup/dbtest.py')

print ('\nFinished with preparing the database.')

#import setup.ordertable

execfile('setup/dbtest.py')


# Analyze data
print ("\n\nBeginning with data analysis\n")

print ("Creating new directory for results. Please find all results there.")
if (os.path.isfile('results') == False):
    os.system('mkdir results')

print("\nFinding drops...")
import analysis.finddrops

print("\nFinding rests...")
import analysis.findrests

