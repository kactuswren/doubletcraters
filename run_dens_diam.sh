#!/bin/bash
#
# args: <input_file> <min_density> <max_density> <intervals>
#
#   input_file - CSV with lon, lat, diameter, [doesn't matter after first 3 columns]
#   min_velocity - in g/cm3
#   max_velocity - in g/cm3
#   intervals - number of intervals between min and max
#
python3 ~/Dropbox/Py/working/dens_effect_on_diam.py\
    one_test_crater.csv 1.0 4.5 10