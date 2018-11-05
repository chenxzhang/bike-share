import csv
import operator
import pygeodesy
import geopy.distance
import math

import plotly.plotly as py
import plotly.graph_objs as go

import numpy as np
import matplotlib.pyplot as plt


def distance(coordinate1, coordinate2):
    return geopy.distance.vincenty(coordinate1, coordinate2).miles

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
    #Sort the dictionary to a list
    sorted_dict = sorted(mydict, key=mydict.get, reverse=True)
    station_ids = []
    number_of_trips = []
    y_pos = np.arange(10)
    for i in range(10):
        station_id =sorted_dict[i]
        station_ids.append(station_id)
        number_of_trips.append(mydict[station_id])
    #Plot
    plt.bar(y_pos, number_of_trips, align='center', alpha=0.35)
    plt.xticks(y_pos, tuple(station_ids))
    plt.ylabel('Number of Trips')
    plt.xlabel('Station ID')
    plt.title('Top Ten Most Popular Starting Station')
    plt.savefig("static/graphs/popular_starting.png", bbox_inches="tight", format="png",)


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
    #Sort the dictionary to a list            
    sorted_dict = sorted(mydict, key=mydict.get, reverse=True)
    station_ids = []
    number_of_trips = []
    y_pos = np.arange(10)
    for i in range(10):
        station_id =sorted_dict[i]
        station_ids.append(station_id)
        number_of_trips.append(mydict[station_id])
    #Plot
    plt.bar(y_pos, number_of_trips, align='center', alpha=0.35)
    plt.xticks(y_pos, tuple(station_ids))
    plt.xlabel('Station ID')
    plt.ylabel('Number of Trips')
    plt.title('Top Ten Most Popular Ending Station')
    plt.savefig("static/graphs/popular_ending.png", bbox_inches="tight", format="png",)



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
            lat1,lon1 = row[5], row[6]
            lat2,lon2 = row[8], row[9]
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
    #Sort the dictionary to a list
    sorted_dict = sorted(distance_dictionary.items(), key=operator.itemgetter(0))
    average = result/number_of_entries
    average_distance = []
    frequency = []
    for i in range(len(sorted_dict)):
        xdistance = sorted_dict[i][0]
        average_distance.append(xdistance)
        frequency.append(sorted_dict[i][1])
    # Create data
    N = len(distance_dictionary)
    x = average_distance
    y = frequency
    y_pos = np.arange(N)
    colors = (0,0,0)
    area = np.pi*3
    # Plot
    plt.plot(x, y, linestyle='-')
    plt.title('Distance Distribution')
    plt.xlabel('Distance(miles)')
    plt.ylabel('Frequency')
    plt.savefig("static/graphs/distance.png", bbox_inches="tight", format="png",)
    return result/number_of_entries

def number_of_regulars(filename):
    pass_index = 13
    number = 0
    total = 0
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            total+=1
            if row[pass_index]=="Flex Pass" or row[pass_index]=="Monthly Pass":
                number+=1
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'Regular', 'Non-Regular'
    sizes = [number, total-number]
    #Plot
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.set_title("Regular vs. Non-Regular Riders")
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig("static/graphs/regular_rider.png", bbox_inches="tight", format="png",)
    return number

#Labels the double bar graph
def autolabel(rects, ax, xpos='center'):
    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

#Trip Route Category-Passholder type 
def trip_route_pass_type(filename):
    pass_index = 13
    trip_index = 12
    one_way = [0,0,0,0]
    round_trip = [0,0,0,0]
    with open(filename, mode='r') as infile:
        reader = csv.reader(infile)
        for row in reader:
            pass_type = row[pass_index]
            trip_type = row[trip_index]
            if row[pass_index]=="Flex Pass" and row[trip_index] == "One Way":
                one_way[0] += 1
            elif row[pass_index]=="Flex Pass" and row[trip_index] == "Round Trip":
                round_trip[0] += 1
            elif row[pass_index]=="Monthly Pass" and row[trip_index] == "One Way":
                one_way[1] += 1
            elif row[pass_index]=="Monthly Pass" and row[trip_index] == "Round Trip":
                round_trip[1] += 1
            elif row[pass_index]=="Staff Annual" and row[trip_index] == "One Way":
                one_way[2] += 1
            elif row[pass_index]=="Staff Annual" and row[trip_index] == "Round Trip":
                round_trip[2] += 1
            elif row[pass_index]=="Walk-up" and row[trip_index] == "One Way":
                one_way[3] += 1
            elif row[pass_index]=="Walk-up" and row[trip_index] == "Round Trip":
                round_trip[3] += 1
    one_way_data = tuple(one_way)
    round_trip_data = tuple(round_trip)
    
    #Create data
    width = 0.35
    ind = np.arange(4) 
    #Plot
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, one_way_data, width, 
                    color='SkyBlue', label='One Way')
    rects2 = ax.bar(ind + width/2, round_trip_data, width,
                    color='IndianRed', label='Round Trip')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of Trips')
    ax.set_title('Trip Route Category-Passholder type')
    ax.set_xticks(ind)
    ax.set_xticklabels(('Flex Pass', 'Montly Pass', 'Staff Annual', 'Walk-up'))
    ax.set_xlabel('Pass Type')
    ax.legend()

    autolabel(rects1, ax, "left")
    autolabel(rects2, ax, "right")

    plt.savefig("static/graphs/trip_pass.png", bbox_inches="tight", format="png",)


