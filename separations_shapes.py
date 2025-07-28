import csv
import math
# import numpy as np
import sys
import os
from datetime import datetime as dt

#
# separations_shapes.py <input_file> <body> <m or km> <min crater diam> <max crater diameter> <min lon> <max lon> <min lat> <max lat>
#

# *******************************************************************
# * Function to filter the original crater list by min/max crater diameter
# *******************************************************************
def filter_craters(crater_file, filtered_file, min_diam, max_diam, min_lon, max_lon, min_lat, max_lat):
    
    crater_file = str(crater_file)
    filtered_file = str(filtered_file)
    min_diam = float(min_diam)    
    max_diam = float(max_diam)
    min_lon = float(min_lon)
    max_lon = float(max_lon)
    min_lat = float(min_lat)
    max_lat = float(max_lat)
    
    # read in crater records
    ff = open(crater_file, 'r')
    csv_ff = csv.reader(ff)
    out = open(filtered_file, 'w')
    csvwriter = csv.writer(out, delimiter=',')

    for row in csv_ff:
        print("Cell 0: ", row[0])
        print("Cell 1: ", row[1])
        print("Cell 2: ", row[2])
        if ((float(row[2]) >= min_diam) and (float(row[2]) <= max_diam) and (float(row[0]) >= min_lon) and (float(row[0]) <= max_lon) and (float(row[1]) >= min_lat) and (float(row[1]) <= max_lat)):
            csvwriter.writerow([row[0], row[1], row[2]])
    out.close()
    


# ********************************************************************************
# * Function to compute distance between two lat/lon points on a planetary surface
# ********************************************************************************
def separation( lon1, lat1, lon2, lat2, radius ):
#    radius = 473       # Ceres mean radius in km
    lon1 = float(lon1)
    lat1 = float(lat1)
    lon2 = float(lon2)
    lat2 = float(lat2)
    radius = float(radius)
    
    diflat = math.radians(lat2-lat1)
    diflon = math.radians(lon2-lon1)
    
    try:    
        a = math.sin(diflat/2) * math.sin(diflat/2) + \
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
            math.sin(diflon/2) * math.sin(diflon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
       
    # Check for negative sqrt call
    except:  #  if (a < 0 or a > 1):
        c = 1
        print ("ValueError for sqrt(a)")
        print ("a = ", a)
        print ("lon1 = ", lon1)
        print ("lat1 = ", lat1)
        print ("lon2 = ", lon2)
        print ("lat2 = ", lat2)
        print ("radius = ", radius)
        print (" ")
            
    d = radius * c
    return d



#========================= MAIN ==================================

# GENERAL CONSTANTS
margin = 0.2    # margin of 100 meters allowed between crater rims.
max_diam = 100.0  # max diameter  in KILOMETERS to consider for pairing
# max_bin_separation = 100
min_DsDp = 0.5

input_rows = []     # [ longitude, latitude, radius ]

crater_pairs = []   # [ crater_num1, lon1, lat1, crater_num2, lon2, lat2, separation ]

# get command line arguments
#
# arg 0 = input file name
# arg 1 = target body ("ceres", "vesta", "mercury", "moon","mars", "venus")
# arg 2 = units ("m" = meters, default=km)
# arg 3 = minimum crater diameter in km
# arg 4 = maximum crater diameter in km
# arg 5 = minimum longitude in degrees
# arg 6 = maximum longitude in degrees
# arg 7 = minimum latitude in degrees
# arg 8 = maximum latitude in degrees

#
args = sys.argv[1:] # skip first arg... that's the script name
input_crater_file = args[0]
target_body = args[1].lower()
units = args[2].lower()
min = args[3]
max = args[4]
min_lon = args[5]
max_lon = args[6]
min_lat = args[7]
max_lat = args[8]


prefix = os.path.splitext(input_crater_file)[0]+'_'+min+'_'+max+'_'+min_lon+'E, '+min_lat+'N'+max_lon+'E, '+max_lat+'N'

if (target_body == "ceres"):
    target_radius = 473
elif (target_body == "vesta"):
    target_radius = 262.7
elif (target_body == "mercury"):
    target_radius = 2439.7
elif (target_body == "moon"):
    target_radius = 1737.4
elif (target_body == "mars"):
    target_radius = 3389.5
elif (target_body == "venus"):
    target_radius = 6051.8
else:
    sys.exit("Invalid target body name.")

# Default units are kilometers, but we allow meters.
units_factor = 1
if (units == "m"):
    units_factor = 0.001
 
# Set the minimum and maximum crater diameter we are interested in
min_diam = float(min) / units_factor
max_diam = float(max) / units_factor

# Filter the input file by min/max diameter
filtered_crater_file = prefix+"_filtered.csv"
filter_craters(input_crater_file, filtered_crater_file, min_diam, max_diam, min_lon, max_lon, min_lat, max_lat)
   
# read in crater records
f = open(filtered_crater_file, 'r')
csv_f = csv.reader(f)
for row in csv_f:
    input_rows.append(row)

num_rows = len(input_rows)

# write out craters only = [ crater_num, lon, lat, radius ]
output_craters_name = prefix+'_craters.csv'
out1 = open(output_craters_name, 'w')
csvwriter = csv.writer(out1, delimiter=',')

# write out craters only as a CSV SHAPE FILE = [ crater_num, lon, lat, radius ]
output_craters_name = prefix+'_craters_shape.csv'
out1shape = open(output_craters_name, 'w')
csvwritershape = csv.writer(out1shape, delimiter=',')
csvwritershape.writerow(['Label','longitude','latitude','Radius:double'])


count = 1  
for x in range (0, num_rows): 
    #    print count, input_rows[x][0], input_rows[x][1], input_rows[x][2]
#    if ((float(input_rows[x][2]) >= min_diam) and (float(input_rows[x][2]) <= max_diam)):
    csvwriter.writerow([count, input_rows[x][0], input_rows[x][1], input_rows[x][2]])
    csvwritershape.writerow([count, input_rows[x][0], input_rows[x][1], input_rows[x][2]])
    count = count + 1
print (count)        

#binnable_sep = []

output_shape_name = prefix+'_pairs_shapefile.csv'
output_human_name = prefix+'_pairs_human.csv'
output_log_name = prefix+'.log'

#out2 = open('crater_pairs.csv', 'w')
out3 = open(output_shape_name,'w')
out4 = open(output_human_name, 'w')
out5 = open(output_log_name, 'w')

#csvwriter = csv.writer(out2, delimiter=',')
csvwriter20k = csv.writer(out4, delimiter=',')

# write Log file header info
py_path = os.path.abspath(__file__)
now = dt.now()
dts = now.strftime("%d/%m/%Y %H:%M:%S")
out5.write(py_path+'\n'+dts+'\n\n')
out5.write('Input file:            '+input_crater_file+'\n')
out5.write('Target body:           '+target_body+'\n')
out5.write('Meters or kilometers:  '+units+'\n')
out5.write('minimum diameter (km): '+min+'\n')
out5.write('maximum diameter (km): '+max+'\n')
out5.write('lower left:  '+min_lon+'E, '+min_lat+'N'+'\n')
out5.write('upper right: '+max_lon+'E, '+max_lat+'N'+'\n')

# Summary statistics
total_craters = 0
filtered_craters = 0
candidates = 0

# write shape file header
out3.write('geometry,Feature:string,Label:string\r\n')
double_quote = '"'

# write out candidate crater report file header
csvwriter20k.writerow(["crater 1", "lon", "lat", "crater 2", "lon", "lat", "separation"])

# create crater pairs and separations (and the shape file, while we're at it)      
for x in range (0, num_rows):
	total_craters += 1
	diam = float(input_rows[x][2])
#    if ((diam >= min_diam) and (diam <= max_diam)):
#	filtered_craters += 1
#	print ("processing crater ",x)
	for y in range (x+1, num_rows):
#		if ((float(input_rows[y][2]) >= min_diam) and (float(input_rows[y][2]) <= max_diam)):
		n1 = x+1
		lon1 = input_rows[x][0]
		lat1 = input_rows[x][1]
		diam1 = float(input_rows[x][2]) * units_factor
		n2 = y+1
		lon2 = input_rows[y][0]
		lat2 = input_rows[y][1]
		diam2 = float(input_rows[y][2]) * units_factor
		sep = separation(lon1, lat1, lon2, lat2, target_radius)
		# Determine ratio of smaller to larger crater
#		print (x, y, "diam1=", diam1, " diam2=", diam2)
		if (diam1 > diam2):
			DsDp = diam2 / diam1
		else:
			DsDp = diam1 / diam2

		maxsep = (diam1+diam2+margin)/2.0   # craters must touch or overlap
		#sep = float(int(sep*10)) / 10.0
		#csvwriter.writerow([n1, lon1, lat1, n2, lon2, lat2, sep])
		if (DsDp > min_DsDp and sep <= maxsep): # and diam1 <= max_diam and diam2 <= max_diam):
			candidates = candidates + 1
			label_string = str(n1) + '-' + str(n2)
			out_string = double_quote + "LINESTRING (" + str(lon1) + " " + str(lat1) + \
						  ", " + str(lon2) + " " + str(lat2) + ")" + double_quote + \
						  ",polyline," + label_string + "\r\n"
			out3.write(out_string)
			csvwriter20k.writerow([n1, lon1, lat1, n2, lon2, lat2, sep])
#                if sep <= max_bin_separation:
#                    binnable_sep.append(sep)

#out2.close()
out3.close()
out4.close()

#write out summary stats to log file
out5.write('\nSummary:\n')
out5.write('Total craters used:     '+str(total_craters)+'\n')
#out5.write('Total craters used:     '+str(filtered_craters)+'\n')
out5.write('Total candidates found: '+str(candidates)+'\n')
done = dt.now()
dts = done.strftime("%d/%m/%Y %H:%M:%S")
out5.write('End processing: '+dts+'\n')
out5.close()

# bin, baby!
#min = 0.0
#max = np.log10(max_bin_separation)
#log_bins = np.logspace(min, max, num=11)     # 10 bins across range from 1 (10^0) to 100 (10^@) km
#binned = np.histogram( binnable_sep, bins=log_bins)
#print " "
#print "Bin bounds:", binned[1]
#print " "
#print "Bin counts:", binned[0]