import csv
import math
import numpy as np

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




input_rows = []     # [ longitude, latitude, radius ]


crater_pairs = []   # [ crater_num1, lon1, lat1, crater_num2, lon2, lat2, separation ]


# read in crater records
f = open('3km_craters2.csv')
csv_f = csv.reader(f)
for row in csv_f:
    input_rows.append(row)
  
num_rows = len(input_rows)

# write out craters only = [ crater_num, lon, lat, radius ]
out1 = open('craters.csv', 'w')
csvwriter = csv.writer(out1, delimiter=',')

count = 1  
for x in range (0, num_rows): 
    #    print count, input_rows[x][0], input_rows[x][1], input_rows[x][2]
    csvwriter.writerow([count, input_rows[x][0], input_rows[x][1], input_rows[x][2]])
    count = count + 1
        

binnable_sep = []
out2 = open('crater_pairs.csv', 'w')
csvwriter = csv.writer(out2, delimiter=',')

# create crater pairs and separations        
for x in range (0, num_rows):
    for y in range (x+1, num_rows):
        n1 = x+1
        lon1 = input_rows[x][0]
        lat1 = input_rows[x][1]
        n2 = y+1
        lon2 = input_rows[y][0]
        lat2 = input_rows[y][1]
        sep = separation(lon1, lat1, lon2, lat2)
        #sep = float(int(sep*10)) / 10.0
        print sep
        csvwriter.writerow([n1, lon1, lat1, n2, lon2, lat2, sep])
        if sep <= 100:
            binnable_sep.append(sep)

# bin, baby!

log_bins = np.logspace(0.0, 1.3, num=11)     # 10 bins across range from 0 to 20 km
binned = np.histogram( binnable_sep, bins=log_bins)
print " "
print "Bin bounds:", binned[1]
print " "
print "Bin counts:", binned[0]

