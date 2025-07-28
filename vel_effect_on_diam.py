import sys
import csv
import math
# import numpy as np


# **************************************************************************
# * Function to compute estimated impactor diameter using crater scaling law
# **************************************************************************
def impact_diameter( crater_diameter, velocity ):

    crater_diameter = float(crater_diameter)
#    v = 4.57    # impactor velocity in km/s
    velocity = float(velocity)
    g = 28      # Ceres gravity in cm/s^2
    pp = 2.788  # projectile density in g/cm^3
    pt = 1.287  # Ceres crustal density in g/cm^3
    
    exp1 = 0.217
    exp2 = 0.333
    exp3 = 1.277
    
    d = ( crater_diameter / (11.9 * ((velocity*velocity/g)**exp1) * ((pp/pt)**exp2)))**exp3
    
    return d



# **************************************************************************
# * MAIN
# **************************************************************************

# arg 0 = input file name (for this, use a single impact crater)
# arg 1 = minimum velocity to test, in kilometers/second
# arg 2 = maximum velocity to test, in kilometers/second
# arg 3 = number of sample intervals between min and max vdlocity

args = sys.argv[1:]
input_crater_file = args[0]
arg_1 = args[1]
arg_2 = args[2]
arg_3 = args[3]
min_velocity = float(arg_1)
max_velocity = float(arg_2)
interval = float(arg_3)


offset = 0    # no offset needed -- processing all craters
input_rows = []     # [ longitude, latitude, radius ]


# read in crater records
f = open(input_crater_file, 'rU')
csv_f = csv.reader(f)
for row in csv_f:
    input_rows.append(row)
  
num_rows = len(input_rows)

# write out craters only = [ crater_num, lon, lat, diameter, impactor_diam ]
out1 = open('vel_effect_on_diam_results.csv', 'w')
csvwriter = csv.writer(out1, delimiter=',')

count = 1
binnable_diam = []
for x in range (0, num_rows):
    diam = float(input_rows[x][2]) / 1000.0 # convert to km
    diff = (max_velocity-min_velocity) / interval
    vel = min_velocity
    while (vel < max_velocity):
        impactor_diameter = impact_diameter(diam, vel) * 1000.0   # convert back to meters
        binnable_diam.append(impactor_diameter)
        #    print count, input_rows[x][0], input_rows[x][1], input_rows[x][2]
        csvwriter.writerow([count, input_rows[x][0], input_rows[x][1], input_rows[x][2], vel, impactor_diameter])
        vel += diff
    count = count + 1


out1.close()