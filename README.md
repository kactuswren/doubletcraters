# doubletcraters

Files for doublet crater research performed in preparation for the LPSC 2017. 
Associated with study area on Ceres bounded by 250 to 270 longitude and -10 to
-30 latitude.


3km_craters2.csv        This file is exported from the Crater Counting layer in JMARS,
                        specifically the one associated with saved session Ceres_13.jmars.
                        It contains all craters in the study area >= 3km in diameter.
                    
                        3 Columns: longitude, latitude, diameter in meters.  Already
                        sorted in JMARS by ascending diameter.
                    
separations_shapes.py   Python script which reads 3km_craters2.csv, and creates three
                        new output files:
                        
                        craters.csv, crater_pairs.csv, crater_pairs_shapefile.csv
                        
                        This program identified all unique pairs of craters from the
                        3km_craters2.csv file which are < 20km separated.
                        
                        It also tallies all crater pairs with separations <= 100 km into
                        ten logarithmic bins and reports the totals for each bin to the
                        screen.

craters.csv             Contains all the craters read from 3km_craters2.csv, numbered
                        from 1 to n.
                        
                        4 columns: crater number, longitude, latitude, diameter in meters.


crater_pairs.csv        Contains all unique pairings of the craters in 3km_craters2.csv.

                        7 columns: first crater number, first longitude, first latitude,
                                   second crater number, second longitude, second latitude,
                                   separation in km


crater_pair_shapefile.csv   A custom shape file (readable by JMARS) that will draw the
                            lines between each crater pair < 20km separated, and label the
                            lines with the assigned crater numbers found in file
                            craters.csv.
                            
montecarlo.py           A Python program which generates a number (equal to the number
                        of craters in input file 3km_craters2.csv) of random crater
                        locations within the study area.
                        
                        It then identifies all unique pairings of these randomly generated
                        craters whose separation is <= 100 km, and tallies these pairs into
                        10 logarithmic bins.
 
                        The above simulation is executed 100 times, and the tallies from
                        all runs averaged.  The average bin totals are reported to the
                        screen.
                        
                        NOTE: Each run of the program will produce slightly different
                              results.
                              

172_crater_pairs_20km.xlsx  An enhanced version of the output file crater_pairs.csv sorted
                            by separation, which also includes hand-entered scoring and
                            evaluation of each of the 172 crater pairs.

