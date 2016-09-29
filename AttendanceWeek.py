##This script is used to find average weekly attendance across all labs for each week

##Import libraries and force floating division
from __future__ import division
import csv

##Path for the input file
readpath = 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/results.csv'

file = open(readpath, 'rb')
input = csv.reader(file)

##Creates two lists two store the total attendance per lab, and the number
##of labs contributing to that total
labs = []
average = []
for i in range(0,14):
    average.append(0)
    labs.append(0)

##Fills the lists with data
count = 0
for row in input:
    row = row[0].split('\t')
    if ('COSC' in row[0] and row[0]!='COSC406 -L01'):
        average[count] += round(int(row[4])/int(row[5]), 2)
        labs[count] = labs[count] + 1
        count +=1
    else:
        count = 0

##Prints the average per week across all labs
for i in range(0, len(labs)):
    print round(average[i]/labs[i],2)
    
print 'Script Completed'
