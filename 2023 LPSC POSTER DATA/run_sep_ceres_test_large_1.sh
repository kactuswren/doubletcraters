#!/bin/bash
#
# args: <input_file> <body> <diam_units> <diam_min>
#
#   input_file - CSV with lon, lat, diameter, [doesn't matter after first 3 columns]
#   body - Currently, "vesta", "moon", "ceres", "mercury" [not case-sensitive]
#   diam_units - what are the units for 3rd column? "m" for meters, "k" for kilometers
#   diam_min - Minimum diameter. Craters smaller than this will be ignored.
#   diam_max - Maximum diameter.
#   lon_min - longitude minimum (degrees) 0-360
#   lon_max - longitude maximum (deg) 0-360
#   lat_min - latitude minimum (deg) -90 to 90
#   lat_max - latitude maximum (deg) -90 to 90  
#
python3 ~/Dropbox/Py/working/separations_shapes.py\
    toyokawa_test_craters.csv ceres m 3 15 0 359.9 -60 60
