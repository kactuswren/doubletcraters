import csv
import math
import numpy as np


# **************************************************************************
# * Function to compute estimated impactor diameter using crater scaling law
# * from: Zahnle K. et al. (2003) Icarus, 163(2), 263-289, using assumed
# * parameters for v, g, pp, and pt provided in Wren P. F. and Fevig R. A.
# * (2017) LPS XXXXVIII. Abstract #2407. 
# **************************************************************************
def impact_diameter( crater_diameter ):

    crater_diameter = float(crater_diameter)
    v = 4.57    # impactor velocity in km/s
    g = 28      # Ceres gravity in cm/s^2
    pp = 2.788  # projectile density in g/cm^3
    pt = 1.287  # Ceres crustal density in g/cm^3
    
    exp1 = 0.217
    exp2 = 0.333
    exp3 = 1.277
    
    d = ( crater_diameter / (11.9 * ((v*v/g)**exp1) * ((pp/pt)**exp2)))**exp3
    
    return d



offset = 0    # no offset needed -- processing all craters

input_rows = []     # [ longitude, latitude, radius ]

crater_pairs = []   # [ crater_num1, lon1, lat1, crater_num2, lon2, lat2, separation ]


# read in crater records
f = open('test_crater1.csv', 'rU')
csv_f = csv.reader(f)
for row in csv_f:
    input_rows.append(row)
  
num_rows = len(input_rows)

# write out craters only = [ crater_num, lon, lat, diameter, impactor_diam ]
out1 = open('impactor_diam.csv', 'w')
csvwriter = csv.writer(out1, delimiter=',')

count = 1
binnable_diam = []
for x in range (0, num_rows):
    diam = float(input_rows[x][2]) / 1000.0 # convert to km
    if (diam <= 15.0):
        impactor_diameter = impact_diameter(diam) * 1000.0   # convert back to meters
        binnable_diam.append(impactor_diameter)
        #    print count, input_rows[x][0], input_rows[x][1], input_rows[x][2]
        csvwriter.writerow([count, input_rows[x][0], input_rows[x][1], input_rows[x][2], impactor_diameter])
    count = count + 1

min = 100.0
max = 1100.0
bins_linear = np.linspace(min, max, num=11)
binned = np.histogram( binnable_diam, bins=bins_linear )
print (" ")
print ("Bin bounds:", binned[1])
print (" ")
print ("Bin counts:", binned[0])

out1.close()
