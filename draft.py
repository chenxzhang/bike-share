import csv
import operator
import pygeodesy
import geopy.distance
import math


def distance(coordinate1, coordinate2):
    return geopy.distance.vincenty(coordinate1, coordinate2).miles

def readCSVSkipOneLine2(filename):
    result=[]
    first=True
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        if (csvReader == None):
            print("FAILED")
            return
        for row in csvReader:
            if first:
                first=False
                continue
            result.append(row)
    return result

#Most popular starting station
def popular_starting(filename):
    row_index = 4
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = dict()
        for row in reader:
            if row[row_index] in mydict:
                mydict[row[row_index]] += 1
            else:
                mydict[row[row_index]] = 1
    station = max(mydict.items(), key=operator.itemgetter(1))[0]
        #mydict = {rows[0]:rows[1] for rows in reader}
    return station

#Most popular ending station
def popular_ending(filename):
    row_index = 7
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        mydict = dict()
        for row in reader:
            if row[row_index] in mydict:
                mydict[row[row_index]] += 1
            else:
                mydict[row[row_index]] = 1
    station = max(mydict.items(), key=operator.itemgetter(1))[0]
        #mydict = {rows[0]:rows[1] for rows in reader}

    return station

def write_distance_frequence(dic):
    w = csv.writer(open("output.csv", "w"))
    for key, val in dic.items():
        w.writerow([key, val])


def distance_frequency(dic, distance):
    distance = math.floor(distance*10)/10
    if distance not in dic: dic[distance] = 1
    else: 
        dic[distance] = dic[distance] + 1
    
#Average distance travelled
def average_distance(filename):
    result=0
    number_of_entries = 0
    first=True
    station_dictionary = dict()
    distance_dictionary = dict()
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            #Skipping the first row(titles)
            if first == True:
                first = False
                continue
            number_of_entries += 1
            start_station_id = row[4]
            end_station_id = row[7]
            lat1 = row[5]
            lon1 = row[6]
            lat2 = row[8]
            lon2 = row[9]
            #Not enough information given
            if (start_station_id == "" or end_station_id == "" or lat1 == ""
                or lat1 == "0" or lon1 == "" or lon1 == "0" or lat2 == "" 
                or lat2 == "0"):
                number_of_entries-=1
                continue
            #Starting station same as ending station (round trip)
            if (start_station_id == end_station_id):
                number_of_hours = int(row[1])/60/60
                #Average biking speed is 9.6 miles/hr
                result+=9.6*number_of_hours;
                continue
            else:
                if start_station_id in station_dictionary:
                    start_station = station_dictionary[start_station_id]
                elif start_station_id not in station_dictionary:
                    lat1 = float(lat1)
                    lon1 = float(lon1)
                    start_station = (lat1, lon1)
                    station_dictionary[start_station_id] = start_station
                if end_station_id in station_dictionary:
                    end_station = station_dictionary[end_station_id]
                elif end_station_id not in station_dictionary:
                    lat2 = float(lat2)
                    lon2 = float(lon2)
                    end_station = (lat2, lon2)
                    station_dictionary[end_station_id] = end_station
                trip_distance = distance(start_station,end_station)
                distance_frequency(distance_dictionary, trip_distance)
                result+=trip_distance
    write_distance_frequence(distance_dictionary)
    return result/number_of_entries

def number_of_regulars(filename):
    pass_index = 13
    number = 0
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            if row[pass_index]=="Flex Pass" or row[pass_index]=="Monthly Pass":
                number+=1
    return number
