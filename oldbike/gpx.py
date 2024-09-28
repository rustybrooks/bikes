#!/usr/bin/python

import sys, string
from xml.dom import minidom, Node

class GPXParser:
    def __init__(self, filename):
        self.track = {}
        try:
            doc = minidom.parse(filename)
            doc.normalize()
        except:
            return # handle this properly later
        gpx = doc.documentElement
        for node in gpx.getElementsByTagName('trk'):
            self.parseTrack(node)
  
    def parseTrack(self, trk):
        name = trk.getElementsByTagName('name')[0].firstChild.data

        for trkseg in trk.getElementsByTagName('trkseg'):
            for trkpt in trkseg.getElementsByTagName('trkpt'):
                lat = float(trkpt.getAttribute('lat'))
                lon = float(trkpt.getAttribute('lon'))
                ele = float(trkpt.getElementsByTagName('ele')[0].firstChild.data)
                rfc3339 = trkpt.getElementsByTagName('time')[0].firstChild.data
                self.track[rfc3339]={'lat':lat,'lon':lon,'ele':ele}
  
    def getTrack(self):
        times = self.track.keys()
        print times
        points = [self.track[time] for time in sorted(times)]
        return [(point['lat'],point['lon']) for point in points]

g = GPXParser(sys.argv[1])
g.getTrack()
