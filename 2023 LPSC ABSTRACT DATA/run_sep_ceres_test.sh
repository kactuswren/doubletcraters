#!/bin/bash
#
# args: <input_file> <body> <diam_units> <diam_min>
#
#   input_file - CSV with lon, lat, diameter, [doesn't matter after first 3 columns]
#   body - Currently, "vesta", "moon", "ceres", "mercury" [not case-sensitive]
#   diam_units - what are the units for 3rd column? "m" for meters, "k" for kilometers
#   diam_min - Minimum diameter in km. Craters smaller than this will be ignored.
#   diam_max = MAximum diameter in km.
#   
#
python3 ~/Dropbox/Py/working/separations_shapes.py\
    toyokawa_test_craters.csv ceres m 3 15 0 110 -30 10
