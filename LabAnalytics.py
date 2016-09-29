##This is the main script. It combs through the lab schedule and
##lab usage snapshots to compile results on usage for each lab

##Import libraries
from __future__ import division
import csv
import time
from datetime import datetime
from datetime import timedelta
##Takes an input string and returns the read path for that file
##NOTE: No data for ART 110, may need to add later
def getFilePath(input):
    if (input=='ART215'):
        return 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/ART215_AE1_LabUsage_aug2014-July292015.csv'
    if (input=='ASC165'):
        return 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/ASC165_GE1_LabUsage_aug2014-July292015.csv'
    if (input=='EME2205'):
        return 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/EME2205_HS1_LabUsage_sept2015-July292015.csv'
    if (input=='FIP129'):
        return 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/FIP129_FS1_LabUsage_sept2014-july292015.csv'
    if (input=='SCI126'):
        return 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/SCI126_SC2_LabUsage_aug2014-july292015.csv'
    if (input=='SCI234'):
        return 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/sci234-cs1-july-1-2014-to-july-9-2015-user-usage.csv'

##Takes a date format and returns it in a standard form
def convertDate(input):
    if ('-' in input):
        input = datetime.strptime(input, '%m-%d-%Y')
    else:
        input = datetime.strptime(input, '%m/%d/%Y')
    return input

##Takes a 12-hour time input and returns the standard representation
def convertTime(input):
    newTime = time.strptime(input, '%I:%M %p')
    return newTime    
        
##Read path for the master schedule and write path for results
readpath = 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/labdata/labs.csv'
writepath = 'C:/Users/Shayne/Documents/COSC 448A/Lab Usage/results.csv'

##Read in the lab schedule and skip the header
masterFile = open(readpath,'rb')
masterInput = csv.reader(masterFile)
next(masterInput, None)

##Creates the output list and appends the header
write = []
header = ['Lab', 'Date', 'Start Time', 'End Time', 'Students Attended', 'Students Registered']
statsHeader = ['Max Attendance', 'Average Attendance']
write.append(header)

##Iterate through the lab sections 
for lab in masterInput:
    ##If the room is defined, not in ART 110, and not COSC 315
    if (lab[22].strip()!='' and lab[23].strip()!='110'and lab[0].strip()!='315'):
        enrolled = lab[9].strip()
        ##Take the start and end dates for the lab and convert them to a standard format
        startDate = convertDate(lab[6].strip())
        endDate = convertDate(lab[7].strip())
        ##Take the start and end times for the lab and convert them to a standard format
        startTime = convertTime(lab[4].strip())
        endTime = convertTime(lab[5].strip())
        ##Day of the lab (abbreviated)
        meet = lab[3].strip()
        ##Open the appropriate file and skip the header
        room = lab[22].strip()+lab[23].strip()
        path = getFilePath(room)
        file = open(path, 'rb')
        input = csv.reader(file)
        next(input, None)
        ##Find the date of the first lab
        tempDate = startDate
        tempDay = tempDate.strftime('%A')
        if (tempDay == 'Thursday'):
            tempDay = 'R'
        else:
            tempDay = tempDay[0]
        while (tempDay!=meet):
            tempDate += timedelta(days=1)
            tempDay = tempDate.strftime('%A')
            if (tempDay == 'Thursday'):
                tempDay = 'R'
            else:
                tempDay = tempDay[0]
        curDate = tempDate
        ##Iterate through the room file for the current lab until the date is past the ending date for that lab
        attendList = []
        maxAttendence = 0
        while (curDate <= endDate):
            students = []
            attending = 0
            for row in input:
                ##Find the time and student number in the record
                temp = row[2].split()
                logDate = convertDate(temp[0].strip())
                logTime = convertTime(temp[1].strip()+' '+temp[2].strip())
                studentNum = row[3].strip()
                ##If the record is in the correct time interval and the student has not been accounted for, increment attendence counter
                if ((curDate == logDate) and (logTime >= startTime and logTime <= endTime) and (studentNum not in students)):
                    students.append(studentNum)
                    attending +=1
            attendList.append(attending)
            maxAttendence = max(maxAttendence, attending)
            ##Append row to output writer, increment the date by one week, return to start of the file, and skip the header
            row = [lab[15].strip(), str(curDate).split()[0], lab[4].strip(), lab[5].strip(), attending, enrolled]
            print row
            write.append(row)
            curDate += timedelta(days=7)
            file.seek(0)
            next(input, None)
        ##Once the dates have been cycled through for that lab, close the room file
        write.append(statsHeader)
        write.append([maxAttendence, round(sum(attendList)/len(attendList), 3)])
        write.append([])
        file.close()

##Write the results to output file
with open(writepath, 'wb') as writefile:
    out = csv.writer(writefile, quoting=csv.QUOTE_ALL)
    out.writerows(write)
    

print 'Script Completed'
