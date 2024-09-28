#!/usr/bin/python

import sqlite3
#import pylab
import matplotlib.pyplot as pylab
import numpy, math
import sys

from collections import defaultdict

def gps_distance(lat1, long1, lat2, long2):
    lat1 = float(lat1) / 180 * math.pi
    lat2 = float(lat2) / 180 * math.pi
    long1 = float(long1) / 180 * math.pi
    long2 = float(long2) / 180 * math.pi

    distr = math.acos( math.sin(lat1)*math.sin(lat2) + math.cos(lat1)*math.cos(lat2)*math.cos(long2-long1) )
    dist = 3963.191 * distr
#    distm = 6371 * 1000 * distr

    return dist

def within_gps_distance(conn, lat, long, distance, where="1=1"):
    found = []
    with conn:
        c = conn.cursor()

        sql = "select ride_id, start_position_lat, start_position_long from rides where start_position_lat is not null and (%s)" % (where)
        for row in c.execute(sql):
            if abs(gps_distance(lat, long, row[1], row[2])) < distance: 
                found.append(row[0])

    return found


conn = sqlite3.connect('example.db')

speed = {
    'secteur': [],
    'tarmac': [],
}

power = {
    'secteur': [],
    'tarmac': [],
}

hist = {
    'secteur': defaultdict(int),
    'tarmac': defaultdict(int),
}

with conn:
    # veloway
    rides = within_gps_distance(conn, 30.2684508870675, -97.7460586641664, 1000+.25)

    # mozarts?
    #rides = within_gps_distance(conn, 30.29545, -97.78338, .25)

    print rides

    c = conn.cursor()


    a = {
        'interval': 60*1,
        'ride_ids': ','.join([str(x) for x in rides]),
        }


    #and strftime("%%Y-%%m-%%d", ride_stamp) > '2013-01-01' 
    sql = '''
	select strftime("%%s", data_stamp)/%(interval)d, avg(speed) as speed, avg(power) as power
	from rides join ride_data using (ride_id)
	where ride_id in (%(ride_ids)s)
        and bike_id=(select bike_id from bikes where name='%(bike)s')
	group by strftime("%%s", data_stamp)/%(interval)d
	having avg(power) > 100 and avg(power) < 300 and sum(power < 5) < count(*)*.10 and count(*) > %(interval)d*.8
    ''' 

    for bike in power.keys():
        a['bike'] = bike
        print sql % a
        for row in c.execute(sql % a):
            speed[bike].append(row[1])
            power[bike].append(row[2])

            hist[bike][round(row[1])] += 1

print numpy.average(speed['secteur']), numpy.std(speed['secteur']), len(speed['secteur'])
print numpy.average(speed['tarmac']), numpy.std(speed['tarmac']), len(speed['tarmac'])

x = numpy.array(power['secteur'])
y = numpy.array(speed['secteur'])
A = numpy.vstack([x, numpy.ones(len(x))]).T
m, c = numpy.linalg.lstsq(A, y)[0]

x2 = numpy.array(power['tarmac'])
y2 = numpy.array(speed['tarmac'])
A2 = numpy.vstack([x2, numpy.ones(len(x2))]).T
m2, c2 = numpy.linalg.lstsq(A2, y2)[0]


xx1 = sorted(hist['secteur'].keys())
yy1 = [hist['secteur'][x] for x in sorted(hist['secteur'].keys())]


n, bins, patches = pylab.hist([speed['secteur'], speed['tarmac']], 40, normed=1)
#pylab.hist(secx, hist['tarmac'], color='blue')

#pylab.plot(power['secteur'], speed['secteur'], linestyle='', color='red', marker='o')
#pylab.plot(power['tarmac'], speed['tarmac'], linestyle='', color='blue', marker='o')
#pylab.plot(x, m*x + c, color='red')
#pylab.plot(x2, m2*x2 + c2, color='blue')

pylab.show()

n, bins, patches = pylab.hist([power['secteur'], power['tarmac']], 40, normed=1)
pylab.show()
