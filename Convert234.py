##This script converts the timestamps in the SCI 234 file to a 12 hour system to match the formatting of the other data

##Import libraries
import csv
from datetime import datetime

##Read and write paths for input and output files
readpath = 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/sci234-cs1-july-1-2014-to-july-9-2015-user-usage.csv'
writepath = 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/sci234-cs1-july-1-2014-to-july-9-2015-user-usage_new.csv'

file = open(readpath, 'rb')
input = csv.reader(file)
next(input, None)

##Append header to the output list
write = []
header = ['Interval', 'Interval Number', 'Interval String', 'studentID']
write.append(header)

##Read in the 24 hour time and convert it to a 12 hour time
for row in input:
    time = row[2].strip().split()
    newtime = datetime.strptime(time[1], "%H:%M").strftime("%I:%M %p")
    write.append([row[0].strip(), row[1].strip(), time[0]+' '+newtime, row[3]])

##Write to output file
with open(writepath, 'wb') as writefile:
    out = csv.writer(writefile, quoting=csv.QUOTE_ALL)
    out.writerows(write)

print 'Script Completed'
