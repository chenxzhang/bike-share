import csv
import operator
import pygeodesy
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

def read_csv_dict(filename, station):
    if station == "starting": row_index = 4
    elif station == "ending": row_index = 7
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

def readCSVSkipOneLine2(filename):
    result=0
    number_of_entries = 0
    first=True
    with open(filename) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            if first == True:
                first = False
                continue
            number_of_entries += 1

            if row[5] == "" or row[6] == "" or row[8] == "" or row[9] == "":
                number_of_entries-=1
                continue
            #Starting station same as ending station
            if (row[5] == row[8]) and (row[6] == row[9]):
                number_of_entries-=1
                continue
            lat1 = float(row[5])
            long1 = float(row[6])
            lat2 = float(row[8])
            long2 = float(row[9])
            #use pygeodesy module to calculate distance between two coordinates
            result+=pygeodesy.haversine(lat1, long1, lat2, long2, 
                radius=6371008.77141, wrap=False)
           
    return result/number_of_entries



