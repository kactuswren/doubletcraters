#!/bin/bash
#
# args: <input_file> <min_velocity> <max_velocity> <intervals>
#
#   input_file - CSV with lon, lat, diameter, [doesn't matter after first 3 columns]
#   min_velocity - in km/s
#   max_velocity - in km/s
#   intervals - number of intervals between min and max
#
python3 ~/Dropbox/Py/working/vel_effect_on_diam.py\
    one_test_crater.csv 1 7 10 