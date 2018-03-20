# Variables


###########
# LOGGING #
###########

# File handling ##
filenamebase = "loggerdata"
subfoldername = "loggerdata"
filebreak = 10000

## Thresholds for logging ##
alwayslog = True                # if set True, every value is logged. If false, new movement has to be detected for logging. 

# only important if alwayslog = False
axthres = 0.2                   # Threshold for difference between two intervals. If difference is larger, logging is triffered
dropthres = 0.4                 # If values are smaller than this threshold, values are logged
abuse = 3                       # If values are larger than this, values are logged
