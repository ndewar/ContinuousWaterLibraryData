# -*- coding: utf-8 -*-
"""
Created on Wed April 17, 2019

@author: Noah Dewar

takes in a text file containing one state well ID per line, then downloads the well reports and continous water level data 
for the given year and makes one big CSV from all the data. if the year is given as POR instead of a year it will grab the 
whole period of record.
"""

# import what we need
import pandas as pd
import os
import time
import requests
import sys
import re

def getWDLContinuous(swid, year):
    
	#reads period of record data from DWR continuous site on water data library
	#Input is the State Well ID (SWID)
	url_GWSE = ('http://wdl.water.ca.gov/waterdatalibrary/docs/Hydstra/docs/' +
	            swid + '/' + year + '/GW_ELEVATION_POINT_DATA.CSV')
	df = pd.read_csv(url_GWSE, index_col=False, parse_dates=[0], skiprows=2,
	                 usecols=[0, 1])
	df.columns = ['Date', 'GWSE_ft']
	
	# convert the type of the date column to a string
	df['Date']=df['Date'].astype(str)
	
	if year != "POR":
		# split the column at the space
		new = df["Date"].str.split(" ", n = 1, expand = True) 
	
		# making seperate day column from new data frame 
		df["Day"]= new[0] 
	
		# making seperate time column from new data frame 
		df["Time"]= new[1] 
	
		# Dropping old date column
		df=df.drop(['Date'], axis=1)
	
	# add a column that just has the swid
	df["SWID"]=swid
	
	# put the swid column first
	df_copy=df["SWID"]
	df=df.drop(["SWID"], axis=1)	
	df=pd.concat([df_copy, df], axis=1)
	return df

def getWellReport(swid):
    
	# reads the well report text file line by line and gets the important information
	# outputs an array where the lines are
	
	# gets the file from the url
	url_GWSE = ('http://wdl.water.ca.gov/waterdatalibrary/docs/Hydstra/docs/' +
	            swid + '/POR/Site_Report.txt')
	response = requests.get(url_GWSE)
	lines=response.text.splitlines()
	info=[]
	info.append(swid)
	
	# find the lines that start with certain strings and then pull the information from those lines
	for currLine in lines:
		try:
			temp=currLine.split()
			if temp[0]=="Latitude:":
				latitude=temp[1]
			if temp[0]=="Longitude:":
				longitude=temp[1]
			if temp[0]=="Site:":
				screen=temp[3]
			if temp[0]=="Elevation:":
				elevation=temp[1]
			if temp[1]=="RP":
				readingPoint=temp[8]
		except:
			pass
	
	# append everything to the info list
	info.append(latitude)
	info.append(longitude)
	info.append(elevation)
	info.append(readingPoint)
	info.append(screen)
	
	# change it into one string with commas seperating values
	s=","
	info=s.join(info)
	print(info)

	return info

if __name__ == "__main__":
	IDFileName=sys.argv[1]
	year=sys.argv[2]
	# load the state well IDs from the given text file
	file = open(IDFileName, "r")
	swidArray = []
	if file.mode == 'r':
		contents = file.readlines()
		for swid in contents:
			swidArray.append(re.sub(r'\n','',swid))

	# import the data, try and except loops are for wells missing 2018 data
	createFlagReport = 0
	createFlagData = 0
	for swid in swidArray:
	
		# do the reports first, do it in a try except block so if there any reports are missing it catches the error
		try:
			report = getWellReport(swid)
			if createFlagReport == 0:
				f = open("wellReports.txt","w+")
				f.write("wellID,lat,long,elevationFT,RPFT,screenInterval\n")
				f.write(report + '\n')
				f.close
				createFlagReport = 1
			else:
				f=open("wellReports.txt", "a+")
				f.write(report + '\n')
				f.close
		except:
			if createFlagReport == 0:
				f = open("wellReports.txt","w+")
				f.write("wellID,lat,long,elevationFT,RPFT,screenInterval\n")
				f.write(swid + ",NoData,NoData,NoData,NoData,NoData\n")
				f.close
				createFlagReport = 1
			else:
				f=open("wellReports.txt", "a+")
				f.write(swid + ",NoData,NoData,NoData,NoData,NoData\n")
				f.write(report)
				f.close
		
		# do the data now    
		try:
			data = getWDLContinuous(swid,year)
			if createFlagData == 0:
				data.to_csv('wellData.csv', index=False)
				createFlagData = 1
			else:
				data.to_csv('wellData.csv', index=False, mode='a', header=False)
		except:
			if createFlagData == 0:
				f = open("wellData.csv","w+")
				f.write("SWID,GWSE_ft,Day,Time\n")
				f.write(swid + ",NoData,NoData,NoData\n")
				createFlagData = 1
			else:
				f = open("wellData.csv","a+")
				f.write(swid + ",NoData,NoData,NoData\n")
		
		# sleep just in case the DWR server thinks this is a DDOS attack
		time.sleep(0.1)