<div itemscope itemtype="https://schema.org/Person"><a itemprop="sameAs" content="https://orcid.org/0000-0002-2750-2866" href="https://orcid.org/0000-0002-2750-2866" target="orcid.widget" rel="noopener noreferrer" style="vertical-align:top;"><img src="https://orcid.org/sites/default/files/images/orcid_16x16.png" style="width:1em;margin-right:.5em;" alt="ORCID iD icon">orcid.org/0000-0002-2750-2866</a></div>

# ContinuousWaterLibraryData
Script to download continuous water level data from the California department of water resources water data library

put state well IDs (SWIDs) in a text file in the same folder as the script, with one SWID per line and run the script.
Pass the script the name of the file with the SWIDs and the year you want data for.

listOfWellIDSGlenn.txt is an example containing every SWID for Glenn county.

Use of the script would be to execute the following from a terminal:<br/>
**$ python downloadContinuousWellData.py listOfWellIDSGlenn.txt 2018<br/>**
That would download the well report information and put it into a text file named wellReports.txt and put the
data for 2018 into a file called wellData.csv
