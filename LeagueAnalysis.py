##The purpose of this script is to analyze a baseball league schedule for 'fairness', i.e.
##home and away games played per team, estimated driving distances and cost, etc.

##Import the library to read csv files
import csv

##Returns the distance between two fields
##TODO Switch to a geocoding library to generalize function for arbitrary locations
def getDistance(home, away):
    if ((home=='Kelowna' and away=='Penticton') or (home=='Penticton' and away=='Kelowna')):
        return 81.8
    if ((home=='Kelowna' and away=='Summerland') or (home=='Summerland' and away=='Kelowna')):
        return 65.0
    if ((home=='Kelowna' and away=='Vernon') or (home=='Vernon' and away=='Kelowna')):
        return 38.5
    if ((home=='Kelowna' and away=='Sicamous') or (home=='Sicamous' and away=='Kelowna')):
        return 114
    if ((home=='Kelowna' and away=='West') or (home=='West' and away=='Kelowna')):
        return 26.0
    if ((home=='Kelowna' and away=='Enderby') or (home=='Enderby' and away=='Kelowna')):
        return 76.3
    if ((home=='Penticton' and away=='Summerland') or (home=='Summerland' and away=='Penticton')):
        return 20.2
    if ((home=='Penticton' and away=='Vernon') or (home=='Vernon' and away=='Penticton')):
        return 119.5
    if ((home=='Penticton' and away=='Sicamous') or (home=='Sicamous' and away=='Penticton')):
        return 193.0
    if ((home=='Penticton' and away=='West') or (home=='West' and away=='Penticton')):
        return 54.0
    if ((home=='Penticton' and away=='Enderby') or (home=='Enderby' and away=='Penticton')):
        return 154.0
    if ((home=='Summerland' and away=='Vernon') or (home=='Vernon' and away=='Summerland')):
        return 109.5
    if ((home=='Summerland' and away=='Sicamous') or (home=='Sicamous' and away=='Summerland')):
        return 179.5
    if ((home=='Summerland' and away=='West') or (home=='West' and away=='Summerland')):
        return 45.6
    if ((home=='Summerland' and away=='Enderby') or (home=='Enderby' and away=='Summerland')):
        return 138.0
    if ((home=='Vernon' and away=='Sicamous') or (home=='Sicamous' and away=='Vernon')):
        return 74.7
    if ((home=='Vernon' and away=='West') or (home=='West' and away=='Vernon')):
        return 62.4
    if ((home=='Vernon' and away=='Enderby') or (home=='Enderby' and away=='Vernon')):
        return 37.6
    if ((home=='Sicamous' and away=='West') or (home=='West' and away=='Sicamous')):
        return 137.0
    if ((home=='Sicamous' and away=='Enderby') or (home=='Enderby' and away=='Sicamous')):
        return 38.5
    if ((home=='West' and away=='Enderby') or (home=='Enderby' and away=='West')):
        return 99.7
    if (home==away):
        return 0
    
##Read in the file and skip the header
readpath = 'C:/Users/Shayne/Documents/COSC 448A/Baseball Stuff/schedule_csv.csv'
writepath = 'C:/Users/Shayne/Documents/COSC 448A/Baseball Stuff/results.csv'
file = open(readpath,'rb')
input = csv.reader(file)
next(input, None)

##Creates a list to be written to the results file and appends title row to it
write = []
row = ['Team Name', 'Number of Games', 'Home Games', 'Away Games', 'Meet in the Middle Games', 'Estimated Travel Distance (km/player)', 'Average Distance per Game(km/player)', 'Estimated Travel Cost ($/player)', 'Travel Saved by Meet in the Middle Games(km/player)']
write.append(row)

##Creates a list of all teams involved
teams = []
for row in input:
    row = row[0].split('\t')
    if (row[0].strip() not in teams):
        teams.append(row[0].strip())
    if (row[1].strip() not in teams):
        teams.append(row[1].strip())

##Iterates through the list of teams and collects data
travelled = []
for team in teams:
    home = 0
    away = 0
    middle = 0
    middleDistance = 0
    distance = 0
    file.seek(0)
    next(input, None)
    for row in input:
        row = row[0].split('\t')
        ##If the current team is playing
        if (row[0].strip()==team or row[1].strip()==team):
            ##Increment either home team or away team
            if (row[0].strip()==team):
                home+=1
            else:
                away+=1
            ##Get the distance between the current team's city and the location of the game
            current = team.split()
            current = current[0]
            distance += getDistance(current,row[8].strip())*2
            ##If it is a meet in the middle game, increment counter and find distance saved
            if  (row[9]=='yes'):
                middle+=1
                ##Distance saved = (normal distance - middle distance)*2
                middleDistance += (getDistance(current,row[6].strip()) - getDistance(current,row[8].strip()))*2
    travelled.append(distance)
    ##Estimated cost is equal to the distance travelled*12 cars travelling*estimated cost/km
    ##Estimates cost/km is based on average of city and highway driving for the most common passenger vehicle from 2013 (Hyundai Elantra)
    cost = distance*0.0884
    ##Appends team's data to the write list 
    row = [team, home+away, home, away, middle, distance, round(distance/(home+away),2), round(cost,2), middleDistance]
    write.append(row)
##Writes the list of data to the results file
with open(writepath,'wb') as writefile:
    out = csv.writer(writefile, quoting=csv.QUOTE_ALL)
    out.writerows(write)

##Find the average distance travelled 
average = 0
for num in travelled:
    average += num
average = average / len(travelled)

##Finds teams who travel more than 20% of the average distance
print '\nTeams travelling more than 20% of the average:'
for i in range(0,len(travelled)-1):
    if (travelled[i] >= average*1.2):
        print teams[i]+'. Estimated additional cost: $'+str((travelled[i]-average)*(0.0884*12))

##Finds teams who travel less than 20% of the average distance
print '\nTeams travelling less than 20% of the average:'
for i in range(0,len(travelled)-1):
    if (travelled[i] <= average*0.8):
        print teams[i]+'. Estimated savings: $'+str((average-travelled[i])*(0.0884*12))

print 'Script Completed'
