###################################################################
# this document contains all important variables for the analysis #
###################################################################



# DROPS
droplimit = 0.4             # threshold when something should be considered as drop
dropdiff = 20               # when a drop is considered as a new drop
dropboundary = 2000         # how many milliseconds before and after a drop should be visualized
nodrop = 2                  # threshold in ms to exclude fale-positive drop. 0 for off

# RESTS
restthreshold = .2          # difference between average x, y or z value in the samplesize and the current sample. 
                            # If smaller, a rest is detected. 
restconcurthres = 10        # threshold how far away two values can be 
                            # and still being still detected as _one_ movement / resting period
