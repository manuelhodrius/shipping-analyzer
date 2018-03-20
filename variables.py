###################################################################
# this document contains all important variables for the analysis #
###################################################################



# DROPS
droplimit = 0.35            # threshold when something should be considered as drop
dropdiff = 4                # size of gap between two drop entries that determines if a drop is considered as a new drop
dropboundary = 200          # how many milliseconds before and after a drop should be visualized
nodrop = 30                 # threshold in ms to exclude false-positive drops. 0 for off
maxdropdur = 3000			# threshold in ms for the maximum drop duration. Sometimes no data is recorded and a drop seems to be endlessly long. Those should be excluded. 

# RESTS
restthreshold = .2          # difference between average x, y or z value in the samplesize and the current sample. 
                            # If smaller, a rest is detected. 
restconcurthres = 10        # threshold how far away two values can be 
                            # and still being still detected as _one_ movement / resting period
# VISUALS
sectionlength = 30			# length of section for visualizing _all_ data

# PEAKS
peakthres = 2				# threshold for peak detection



