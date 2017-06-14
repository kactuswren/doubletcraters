import csv
import math
import numpy as np
import random

# *******************************************************************
# * Function to compute distance between two lat/lon points on Ceres
# *******************************************************************
def separation( lon1, lat1, lon2, lat2 ):
    radius = 473       # Ceres mean radius in km
    lon1 = float(lon1)
    lat1 = float(lat1)
    lon2 = float(lon2)
    lat2 = float(lat2)
    
    diflat = math.radians(lat2-lat1)
    diflon = math.radians(lon2-lon1)
    
    a = math.sin(diflat/2) * math.sin(diflat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(diflon/2) * math.sin(diflon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d



# *******************************************************************
# * Function to compute 80 random impacts and bin them
# *******************************************************************
def sim_impacts(log_bins):
    random_craters = []     # [ longitude, latitude ]
    crater_pairs = []   # [ crater_num1, lon1, lat1, crater_num2, lon2, lat2, separation ]

    # randomized crater records
    num_craters = 80
    minlon = 250.0
    maxlon = 270.0
    minlat = -30.0
    maxlat = -10.0

    for x in range(0, num_craters):
        randlon = random.uniform(minlon, maxlon)
        randlat = random.uniform(minlat, maxlat)
        row = [randlon, randlat]
        random_craters.append(row)
  
    num_rows = len(random_craters)

    binnable_sep = []	
    # create crater pairs and separations        
    for x in range (0, num_rows):
        for y in range (x+1, num_rows):
			n1 = x+1
			lon1 = random_craters[x][0]
			lat1 = random_craters[x][1]
			n2 = y+1
			lon2 = random_craters[y][0]
			lat2 = random_craters[y][1]
			sep = separation(lon1, lat1, lon2, lat2)
			# sep = int(sep)
			if sep <= 20:
				binnable_sep.append(sep)

	# bin, baby!
    binned = np.histogram( binnable_sep, bins=log_bins)
#    print binned[0]
    return binned[0]

# *************************** MAIN *************************************

out2 = open('montecarlo.csv', 'w')
csvwriter = csv.writer(out2, delimiter=',')

# Create the bins
bins = np.logspace(0.0, 1.3, num=11)     # 10 bins across range from 0 to 20 km
csvwriter.writerow(bins)

# Execute the simulation runs
number_runs = 1000;
sim_runs = []
for i in range(0, number_runs):
    binned_seps = sim_impacts(bins)
    sim_runs.append(binned_seps)
    csvwriter.writerow(binned_seps)

# Compute means for all bins

bin_sums  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
bin_means = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

for one_run in sim_runs:
    for j in range(0,len(bins)-1):
        bin_sums[j] = bin_sums[j] + one_run[j]
    #print one_run

for j in range(0,len(bins)-1):
    bin_means[j] = float(bin_sums[j]) / float(number_runs)

csvwriter.writerow(bin_means)
        
print bin_sums
print bin_means

