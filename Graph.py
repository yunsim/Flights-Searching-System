import sqlite3 as dbi
import sys
from copy import deepcopy

class Graph (object):
    def __init__(self, foldername='Graph.db'):
        try:
            self.db = dbi.connect(foldername)
            self.cu=self.db.cursor()
            #print 'success'
        except:
            #print 'failed'
            sys.exit()
    #return a list of all the airports codes    
    def getAirportCodes(self):
        cmd="""SELECT Name FROM Airports ORDER BY Name"""
        self.cu.execute(cmd)
        l=[]
        for li in self.cu.fetchall():
            l.append(li[0])
        return l
    def getAirportPositions(self):
        self.cu.execute(
        '''
        SELECT A.name, A.long, A.lati
        FROM Airports as A
        ''')
        #l=[]
        #for li in self.cu.fetchall():
        #    l.append(li[0])
        #return l
        return self.cu.fetchall()
    
    def getLineEndPositions(self):#make the result order by fa.long to make the line drawing easy
        self.cu.execute(
        '''
        SELECT FA.long, FA.lati, TA.long, TA.lati
        FROM Airports as FA, Airports as TA, Flights as F
        WHERE
        F.FromAir = FA.Name
        AND F.ToAir = TA.Name
        ORDER BY FA.Name, TA.Name
        ''')
        l=[]
        #for li in self.cu.fetchall():
        #    l.append(li[0])
        #return l
        return self.cu.fetchall()
    
        
    #return a list of flights.ID going out from the cityName    
    def getAttachedLines(self, aptName):
        cmd="""SELECT ID FROM Flights
               WHERE FromAir='{}'"""
        self.cu.execute(cmd.format(aptName))
        l=[]
        for li in self.cu.fetchall():
            l.append(li[0])
        return l
    #return the cities.Name reached by the flightsID
    def getAttachedNodes(self, fltID):  
        cmd="""SELECT ToAir FROM Flights
               WHERE ID='{}' """
        self.cu.execute(cmd.format(fltID)) 
        return self.cu.fetchone()
    #helper function getting city and state of airport from airportName
    def getCityofAirport(self,AptName):
        cmdgetcity="""SELECT c.Name, c.State FROM Cities AS c, Airports AS a 
                   WHERE a.cityID=c.ID AND A.Name='{}'"""
        self.cu.execute(cmdgetcity.format(AptName))
        return self.cu.fetchone()
    #helper function getting necessary information of flight for given flight ID and return a string in a format of print 
    def printFlightInfo(self, fltID):
        
        cmdgetflightinfo="""SELECT f.Number, fc.Name, fc.State, fa.Name, f.DepartTime, tc.Name, tc.State, ta.Name, f.ArrivalTime
                          FROM Flights AS f, Airlines AS al, Airports AS fa, Airports AS ta, Cities AS fc, Cities AS tc
                          WHERE al.ID=f.OperatorID AND f.FromAir=fa.Name AND fa.cityID=fc.ID AND f.ToAir=ta.Name AND ta.CityID=tc.ID
                                AND f.ID={}"""
        self.cu.execute(cmdgetflightinfo.format(fltID))
        fl = self.cu.fetchone()
        s="""on Flight Number {} from {}, {}, ({}) at {}:{:02d}, arrive at {}, {} ({}) at {}:{:02d} \n"""\
                 .format(fl[0], fl[1],fl[2],fl[3],fl[4]/60,fl[4]%60,fl[5], fl[6], fl[7], fl[8]/60,fl[8]%60)
        return s
    #helper function getting necessary information of flight for given flight ID and return a list of the infos rather than string
    def FlightInfo(self, fltID):
        cmdgetflightinfo="""SELECT f.Number, fc.Name, fc.State, fa.Name, f.DepartTime, tc.Name, tc.State, ta.Name, f.ArrivalTime
                          FROM Flights AS f, Airlines AS al, Airports AS fa, Airports AS ta, Cities AS fc, Cities AS tc
                          WHERE al.ID=f.OperatorID AND f.FromAir=fa.Name AND fa.cityID=fc.ID AND f.ToAir=ta.Name AND ta.CityID=tc.ID
                                AND f.ID={}"""
        self.cu.execute(cmdgetflightinfo.format(fltID))
        return self.cu.fetchone()
        
    def __str__(self):  
        cmd="""SELECT c.Name, a.Name, a.X, a.Y
               FROM Airports AS a, Cities AS c
               WHERE a.cityID=c.ID"""
        self.cu.execute(cmd)
        allApts=self.cu.fetchall()
        s='*Airports: \n'
        for apt in allApts:
            s+="""{} : {} at ({} miles, {} miles) \n""".format(apt[0], apt[1], apt[2], apt[3])
            
        s+='* Flights:\n'
        
        cmd="""SELECT f.Number, al.Name, fc.Name, fc.State, fa.Name, f.DepartTime, tc.Name, tc.State, ta.Name, f.ArrivalTime
               FROM Flights AS f, Airlines AS al, Airports AS fa, Airports AS ta, Cities AS fc, Cities AS tc
               WHERE al.ID=f.OperatorID AND f.FromAir=fa.Name AND fa.cityID=fc.ID AND f.ToAir=ta.Name AND ta.CityID=tc.ID"""
        self.cu.execute(cmd) 
        allFlights=self.cu.fetchall()
        
        for fl in allFlights:
            s+="""Flight Number {} operated by {}: leaving {}, {}, ({}) at {}:{:02d} to {}, {} ({}) arriving at {}:{:02d} \n"""\
                 .format(fl[0], fl[1],fl[2],fl[3],fl[4],fl[5]/60,fl[5]%60,fl[6], fl[7], fl[8], fl[9]/60,fl[9]%60)
        return s
        
    
           
    def findPath(self, startName, endName):
        cmdtogetapt = """SELECT Name FROM Airports"""
        self.cu.execute(cmdtogetapt)
        aptList = self.cu.fetchall()
        apts=[]
        for l in aptList:
            apts.append(l[0])
        
        if startName not in apts :
            print "unknown AirportName=%s" % startName
        if endName not in apts :
            print "unknown AirportName=%s" % endName
        global pathlist
        (traveledLines, traveledNodes)=([],[])
        path= dict (nodepath=[], linepath=[], length= 0.0)
        pathlist=[]
        startName=str(startName)
        endName=str(endName)
        self.findPathInside(startName,endName, path,traveledNodes[:], traveledLines[:])
        return pathlist
    #method to print out all the paths from start to end
    def findAll(self, startName, endName):    
        pathlist=self.findPath(startName, endName)
        startInfo=self.getCityofAirport(startName)
        endInfo=self.getCityofAirport(endName)
        s=''
        for spath in pathlist:
            firstline=self.FlightInfo(spath['linepath'][0])
            lastline=self.FlightInfo(spath['linepath'][len(spath['linepath'])-1])
            s+='\n Trip: {}: {}, {} to {}: {}, {}\n departs at {}:{:02d}, arrives at {}:{:02d} after travelling for {}:{:02d} hours\n'\
            .format(startName, startInfo[0], startInfo[1], endName, endInfo[0], endInfo[1], firstline[4]/60, firstline[4]%60,\
                    lastline[8]/60, lastline[8]%60, int(spath['length'])/60, int(spath['length'])%60)
            for f in spath['linepath']:
                s+=self.printFlightInfo(f)
            #position of start and end airports
        return s
    
    def findPathInside(self, startName, endName, path, GtraveledNodes, GtraveledLines):

        if startName not in GtraveledNodes:
            #traveledNodes=GtraveledNodes[:]
            GtraveledNodes.append(startName)
            
            
            cmdtogettrvltime = """SELECT DepartTime, ArrivalTime  FROM Flights
                                      WHERE ID='{}'"""
            #get all the path has went through
            lastpath=path['linepath']
            if len(lastpath) >0:
                #get the time information for the previous path has travelled
                self.cu.execute(cmdtogettrvltime.format(lastpath[len(lastpath)-1]))
                lastDETime = self.cu.fetchone()[0]
                self.cu.execute(cmdtogettrvltime.format(lastpath[len(lastpath)-1]))
                lastARTime = self.cu.fetchone()[1]
            else:
                lastARTime=-1
                
            for l in self.getAttachedLines(startName):
                self.cu.execute(cmdtogettrvltime.format(l))
                newDETime= self.cu.fetchone()[0]
                self.cu.execute(cmdtogettrvltime.format(l))
                newARTime = self.cu.fetchone()[1]
        
                traveledNodes = GtraveledNodes[:]
                traveledLines = GtraveledLines[:]
            
                if (l not in traveledLines):
                    traveledLines.append(l)
                    #print type(l)
                    #print type(self.getAttachedNodes(l))
                    for n in  self.getAttachedNodes(l):
                        if n not in traveledNodes:
                            pathInside=deepcopy(path)
                            pathInside['nodepath'].append(startName)
                            pathInside['linepath'].append(l)
                            if lastARTime==-1:
                                T1=0
                            else:
                                T1=newDETime-lastARTime
                                if T1 <=0 :
                                    T1=T1+24*60
                            pathInside['length']+=T1+newARTime-newDETime
                            if n==endName:     
                                pathInside['nodepath'].append(endName)
                                pathlist.append(pathInside)
                            else:
                                self.findPathInside(n, endName, pathInside,traveledNodes, traveledLines)
    
    
    def findShortestPath(self, startName, endName):
        allPath=self.findPath(startName, endName)
        #print allPath
        shortestLen=allPath[0]['length']
        j=0
        for i in range(1,len(allPath)):
            if allPath[i]['length']<shortestLen:
                j=i
                shortestLen=allPath[i]['length']
        #do all the strings for the print
        #get the start, end airport information and the first and last flight in the path for the first print line
        spath=allPath[j]
        startInfo=self.getCityofAirport(startName)
        endInfo=self.getCityofAirport(endName)
        firstline=self.FlightInfo(spath['linepath'][0])
        lastline=self.FlightInfo(spath['linepath'][len(spath['linepath'])-1])
        
        s='Trip: {}: {}, {} to {}: {}, {}\n departs at {}:{:02d}, arrives at {}:{:02d} after travelling for {}:{:02d} hours\n'\
           .format(startName, startInfo[0], startInfo[1], endName, endInfo[0], endInfo[1], firstline[4]/60, firstline[4]%60,\
                   lastline[8]/60, lastline[8]%60, int(spath['length'])/60, int(spath['length'])%60)
        #add each flight information to the printout string and start and end position of the flight
        flightpos=[]
        for f in spath['linepath']:
            s+=self.printFlightInfo(f)
            #position of start and end airports
            self.cu.execute(
            '''
            SELECT FA.long, FA.lati, TA.long, TA.lati,F.Number
            FROM Airports as FA, Airports as TA, Flights as F
            WHERE
            F.FromAir = FA.Name
            AND F.ToAir = TA.Name
            AND F.ID='{}'
            '''.format(f))
            flightpos.append(self.cu.fetchone())
        
        return [s, flightpos]

    
    def numNodes(self):
        cmd="""SELECT count(Name) FROM Airports"""
        self.cu.execute(cmd)
        return self.cu.fetchone()[0]
    
    def numLines(self):
        cmd="""SELECT count(ID) FROM Flights"""
        self.cu.execute(cmd)
        return self.cu.fetchone()[0]