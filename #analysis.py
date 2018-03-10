import os

###############
# PREPARATION #
###############

# Delete old database
if (os.path.isfile('loggerdata.sqlite') == True):
    os.remove('loggerdata.sqlite')

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


############
# ANALYSIS #
############

# Prompt
print ("\n\nBeginning with data analysis\n")

# Create Directories
print ("Creating new directory for results. Please find all results there.")
if (os.path.isfile('results') == False):
    os.system('mkdir results')
print ("Creating new directory for visuals. Please find all visualizations there.")

visualpath = r'results\visual'
if (os.path.exists(visualpath) == False):
    os.makedirs(visualpath)
if (os.path.exists('results/visual/drops') == False):
    os.makedirs('results/visual/drops')
if (os.path.exists('results/visual/alldata') == False):
    os.makedirs('results/visual/alldata')
if (os.path.exists('results/move') == False):
    os.makedirs('results/move')

# Drops
print("\nFinding drops...")
import analysis.finddrops_aPrepare
import analysis.finddrops_bFind
import analysis.finddrops_cSave
import analysis.finddrops_dOutput
import analysis.finddrops_eVisualize

# Peaks
import analysis.findpeaks

print("\nFinding movement...")
import analysis.getmovement

print("Gnerating diagrams for all data...")
import visual.visual_all

