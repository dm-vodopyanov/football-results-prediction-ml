import os

import csv

dir = "..\\datasets"

def takeCSV(dir):
	for name in os.listdir(dir):
	    path = os.path.join(dir, name)
	    if os.path.isfile(path):
	        if name.endswith("csv"):
	        	parseCSV(path)
	    else:
	        takeCSV(dir)

def parseCSV(path):
	print path + " was parsed"

if __name__ == '__main__':
    takeCSV(dir) 

