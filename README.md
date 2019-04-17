# ContinuousWaterLibraryData
Script to download continuous water level data from the California department of water resources water data library

put state well IDs (SWIDs) in a text file in the same folder as the script, with one SWID per line and run the script.
Pass the script the name of the file with the SWIDs and the year you want data for.

listOfWellIDSGlenn.txt is an example containing every SWID for Glenn county.

Use of the script would be to execute the following from a terminal:
$ python downloadContinuousWellData.py listOfWellIDSGlenn.txt 2018
That would download the well report information and put it into a text file named wellReports.txt and put the
data into a file called wellData.csv
