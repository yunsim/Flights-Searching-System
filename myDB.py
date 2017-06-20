'''
Created on Nov 13, 2016

@author: yunsimou
'''
import sqlite3 as DBI

# Create a database named 'Graph.db' if not exist and create a cursor for this database
conn = DBI.connect('Graph.db')
c = conn.cursor()

# Create four empty tables for Cities, Airports, Airlines and Flights in the database
c.execute('DROP TABLE IF EXISTS Cities;')
c.execute('DROP TABLE IF EXISTS Airports;')
c.execute('DROP TABLE IF EXISTS Airlines;')
c.execute('DROP TABLE IF EXISTS Flights;')
c.execute('CREATE TABLE Cities(ID integer not null primary key, name char(30), state char(10));')
c.execute('CREATE TABLE Airports(ID integer not null primary key, name char(30), cityID integer unsigned, longitude float, latitude float, x float, y float);')
c.execute('CREATE TABLE Airlines(ID integer not null primary key, operator char(30));')
c.execute('CREATE TABLE Flights(ID integer not null primary key, name char(30), airlineID integer unsigned, fromID integer unsigned, toID int unsigned, dTime char(30), aTime char(30));')

# Read AirportData.txt and store all data in the Airportdata list
Airportdata = []  
try:
    f = open('../AirportData.txt', 'r')  
except IOError:
    print("Could not open file for reading")

line = f.readline() 
for line in f:
    words = line.rstrip().split('\t')
    Airportdata.append(words)
    
f.close() 

# Read FlightData.txt and store all data in the Flightdata list
Flightdata = []  
try:
    f = open('../FlightData.txt', 'r')  
except IOError:
    print("Could not open file for reading")

line = f.readline() 
for line in f:
    words = line.rstrip().split('\t')
    Flightdata.append(words)
    
f.close()

# Test the lists I created for storing data
print Airportdata
print Flightdata

# Insert data into Cities
cityID = 1
cities = []
for element in Airportdata:
    if element[1] not in cities:
        c.execute('INSERT INTO Cities (ID, name, state) VALUES(?, ?, ?)',
              (cityID, element[1], element[2]))
        cityID += 1
        cities.append(element[1])
    
# Insert data into Airlines    
airlineID = 1
airlines = []
for element in Flightdata:
    if element[1] not in airlines:
        c.execute('INSERT INTO Airlines (ID, operator) VALUES(?, ?)',
              (airlineID, element[1]))
        airlineID += 1
        airlines.append(element[1])

# Insert data into Airports
airportID = 1
for element in Airportdata:
    c.execute('SELECT Ci.ID FROM Cities as Ci WHERE Ci.name = ?;', (element[1],))
    cityid = c.fetchone()[0]
    c.execute('INSERT INTO Airports (ID, name, CityID, longitude, latitude, x, y) VALUES(?, ?, ?, ?, ?, ?, ?)',
              (airportID, element[0], cityid, element[3], element[4], element[5], element[6])) 
    airportID += 1
 
# Insert data into Flights   
flightID = 1
for element in Flightdata:
    c.execute('SELECT Ail.ID FROM Airlines as Ail WHERE Ail.operator = ?;', (element[1],))
    airlineid = c.fetchone()[0]
    c.execute('SELECT Aip.ID FROM Airports as Aip WHERE Aip.name = ?;',(element[2],))
    fromid = c.fetchone()[0]
    c.execute('SELECT Aip.ID FROM Airports as Aip WHERE Aip.name = ?;',(element[3],))
    toid = c.fetchone()[0]
    c.execute('INSERT INTO Flights (ID, name, airlineID, fromID, toID, dTime, aTime) VALUES(?, ?, ?, ?, ?, ?, ?)',
              (flightID, element[0], airlineid, fromid, toid, element[4], element[5]))
    flightID += 1
  
conn.commit()
conn.close()
    