#!/usr/bin/python

import sqlite3
import matplotlib.pyplot as pylab
import matplotlib.dates as dates
import optparse
import time, datetime
import numpy, math
import sys

def window(data, length):
    w=numpy.ones(length,'d')
    x = numpy.array([a[1] for a in data])

    if len(w) > len(x): return 0

    #s=numpy.r_[2*x[0] - x[length:1:-1], x, 2*x[-1]-x[-1:-length:-1]]
    s=x
#    print len(s), len(x), len(w), s.shape
    y=numpy.convolve(w/w.sum(),s,mode='same')
    return max(y)

def speed_window(data, length):
    if length >= len(data): return 0

    x = numpy.array([a[2] for a in data])
    tm = numpy.array([a[0] for a in data])
    distw = x[length:] - x[:-length]
    tmw = tm[length:] - tm[:-length]
    speed = distw/(tmw/(60*603600.0))
    return max(speed)

def process_power_curve(conn, ride_id):
    print "Starting power", ride_id

    t1 = time.time()
    with conn:
        c = conn.cursor()

        c.execute("select count(*) as count from power_curve where ride_id=?", (ride_id, ) )
        row = c.fetchone()
        if row[0] > 0: 
            return

        segments = []
        this_segment = []
        c = conn.cursor()
        sql = "select strftime('%s', data_stamp) as data_stamp, power from ride_data where ride_id=? order by data_stamp"
        last = None
        first = None
        for row in c.execute(sql, (ride_id, )):
            try:
                row = (float(row[0]), row[1] if row[1] is not None else 0)
            except TypeError:
    #            print row, float(row[0])
                continue
                               
            if last:
                diff = row[0] - last[0]
    
                if abs(diff) > 15: 
    #                print row[0] - first, diff, row
                    segments.append(this_segment)
                    this_segment = []
                elif abs(diff) > 1:
                    for i in range(1, int(diff)):
                        this_segment.append((last[0]+i, last[1]))
    
                this_segment.append(row)
            else:
                first = row[0]
    
            last = row
            #print row[0]
        segments.append(this_segment)
    
        max_seconds = row[0] - first

        results = []
        for win in range(10,int(max_seconds),10):
            val = max([window(s, win) for s in segments])
            if val == 0: continue
            results.append([None, win, val, ride_id])


        c.executemany("insert into power_curve(power_curve_id, interval_length, power, ride_id) values(?, ?, ?, ?)", results)
        print ride_id, "took", time.time() - t1

def process_power_curves(conn):
    with conn:
        sql = """
            select ride_id 
            from rides o 
            where not exists (select ride_id from power_curve i where i.ride_id=o.ride_id)
            and exists (select ride_id from ride_data i2 where i2.ride_id=o.ride_id and power>0)
        """

        c = conn.cursor()
        for row in c.execute(sql):
            process_power_curve(conn, row[0])


def fetch_power_curve(conn, date_start, date_end):
    c = conn.cursor()

    sql = "select interval_length/60.0, max(power) from power_curve join rides using(ride_id) where ride_stamp >= '%s' and ride_stamp <= '%s' group by interval_length" % (date_start, date_end)
    print sql

    x = []; y = []
    for row in c.execute(sql):
        x.append(row[0])
        y.append(row[1])

    #pylab.xscale('log')
    pylab.plot(x, y)
    pylab.show()

def best_power(conn, date_start, date_end, window, rolling_window_days=7):
    rolling_window_time=7*60*60*24

    sql = """
        select strftime('%%s', ride_stamp), power 
        from power_curve 
        join rides using(ride_id) 
        where ride_stamp >= '%s' and ride_stamp <= '%s' 
        and interval_length = %d order by ride_stamp
    """ % (date_start, date_end, window)

    c = conn.cursor()

    xxx = []
    for row in c.execute(sql):
        xxx.append((datetime.datetime.fromtimestamp(float(row[0])), row[1]))
    print xxx

    x = []
    y = []

    d = xxx[0][0]
    last = xxx[-1][0]
    while d <= last:
        d += datetime.timedelta(days=1)
        dx = d - datetime.timedelta(days=rolling_window_days)
        days = [a for a in xxx if a[0]>dx and a[0]<=d]
        if days:
            x.append(d)
            y.append( max([val[1] for val in days]) )
        #else:
        #    y.append(0)

    return x, y



def process_speed_curve(conn, ride_id, delete=False):
    print "Starting speed", ride_id

    t1 = time.time()
    with conn:
        c = conn.cursor()

        if delete:
            c.execute("delete from speed_curve where ride_id=?", (ride_id, ))

        c.execute("select count(*) as count from speed_curve where ride_id=?", (ride_id, ) )
        row = c.fetchone()
        if row[0] > 0: 
            return

        segments = []
        this_segment = []
        c = conn.cursor()
        sql = "select strftime('%s', data_stamp) as data_stamp, speed, distance from ride_data where ride_id=? order by data_stamp"
        last = None
        first = None
        for row in c.execute(sql, (ride_id, )):
            try:
                row = (float(row[0]), row[1] if row[1] is not None else 0, row[2] if row[2] is not None else 0)
            except TypeError:
    #            print row, float(row[0])
                continue
                               
            if last:
                diff = row[0] - last[0]
    
                if abs(diff) > 15: 
    #                print row[0] - first, diff, row
                    segments.append(this_segment)
                    this_segment = []
                elif abs(diff) > 1:
                    for i in range(1, int(diff)):
                        this_segment.append((last[0]+i, last[1], last[2]))
    
                this_segment.append(row)
            else:
                first = row[0]
    
            last = row
            #print row[0]
        segments.append(this_segment)
    
        max_seconds = row[0] - first

        results = []
        for win in range(10,int(max_seconds),10):
            #val = max([window(s, win) for s in segments])
            val = max([speed_window(s, win) for s in segments])

            #if val > 0 and (abs(val2 - val) / val) > 0.01:
            #    print win, val, val2
            if val == 0: continue
            results.append([None, win, val, ride_id])


        c.executemany("insert into speed_curve(speed_curve_id, interval_length, speed, ride_id) values(?, ?, ?, ?)", results)
        print ride_id, "took", time.time() - t1

def process_speed_curves(conn):
    with conn:
        sql = """
            select ride_id 
            from rides o 
            where not exists (select ride_id from speed_curve i where i.ride_id=o.ride_id)
            and exists (select ride_id from ride_data i2 where i2.ride_id=o.ride_id and speed>0)
        """

        c = conn.cursor()
        for row in c.execute(sql):
            process_speed_curve(conn, row[0])
            #break


def fetch_speed_curve(conn, date_start, date_end):
    c = conn.cursor()

    sql = "select interval_length/60.0, max(speed) from speed_curve join rides using(ride_id) where ride_stamp >= '%s' and ride_stamp <= '%s' group by interval_length" % (date_start, date_end)
    print sql

    x = []; y = []
    for row in c.execute(sql):
        x.append(row[0])
        y.append(row[1])

    #pylab.xscale('log')
    pylab.plot(x, y)
    pylab.show()

def best_speed(conn, date_start, date_end, window, rolling_window_days=7):
    rolling_window_time=7*60*60*24

    sql = """
        select strftime('%%s', ride_stamp), speed 
        from speed_curve 
        join rides using(ride_id) 
        where ride_stamp >= '%s' and ride_stamp <= '%s' 
        and interval_length = %d order by ride_stamp
    """ % (date_start, date_end, window)

    c = conn.cursor()

    xxx = []
    for row in c.execute(sql):
        xxx.append((datetime.datetime.fromtimestamp(float(row[0])), row[1]))
    print xxx

    x = []
    y = []

    d = xxx[0][0]
    last = xxx[-1][0]
    while d <= last:
        d += datetime.timedelta(days=1)
        dx = d - datetime.timedelta(days=rolling_window_days)
        days = [a for a in xxx if a[0]>dx and a[0]<=d]
        if days:
            x.append(d)
            y.append( max([val[1] for val in days]) )
        #else:
        #    y.append(0)

    return x, y




parser = optparse.OptionParser()
parser.add_option("-d", "--database", default="./example.db")
parser.add_option("-r", "--ride-id", default="None")
(options, args) = parser.parse_args()

conn = sqlite3.connect(options.database)
#process_speed_curve(conn, 1, True)
process_power_curves(conn)
process_speed_curves(conn)
#fetch_curve(conn, "2014-02-27", "2014-04-05")
#fetch_speed_curve(conn, "2014-02-27", "2014-04-05")
#fetch_curve(conn, "2013-01-01", "2013-12-31")
dw = 7*4
first="2013-09-01"


fig = pylab.figure(num=1, figsize=(18, 10.5), dpi=80)
pylab.subplot(111)

#x1, y1 = best_power(conn, first, "2014-12-31", 1*60, dw)
#pylab.plot(x1, y1, linestyle='-')

#x2, y2 = best_power(conn, first, "2014-12-31", 5*60, dw)
#pylab.plot(x2, y2, linestyle='-')

#x3, y3 = best_power(conn, first, "2014-12-31", 10*60, dw)
#pylab.plot(x3, y3, linestyle='-')

#x4, y4 = best_power(conn, first, "2014-12-31", 20*60, dw)
#pylab.plot(x4, y4, linestyle='-')

########################################

x1, y1 = best_power(conn, "2014-01-01", "2014-12-31", 20*60, dw)
pylab.plot(x1, y1, linestyle='-')

x2, y2 = best_power(conn, "2013-01-01", "2013-05-01", 20*60, dw)
x2 = [x + datetime.timedelta(days=365) for x in x2]
pylab.plot(x2, y2, linestyle='-')

########################################

#x1, y1 = best_speed(conn, "2014-01-01", "2014-12-31", 30*60, dw)
#pylab.plot(x1, y1, linestyle='-')

#x2, y2 = best_speed(conn, "2013-01-01", "2013-05-01", 30*60, dw)
#x2 = [x + datetime.timedelta(days=365) for x in x2]
#pylab.plot(x2, y2, linestyle='-')



fig.autofmt_xdate(rotation=-30, ha='left')
pylab.show()
