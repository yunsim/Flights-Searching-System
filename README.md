UW CEE 505 Engineering Computing
Final Project: Data Visualization Tool

# Flights-Searching-System
A SQL-based Commuting Flights Searching System 

Develop a graphic representation of the graph problem using wx.DC (in a frame).
Functionality:
1. Read a graph (air traffic problem) from an SQL database using sqlite3.
2. Design and implement a graphical user interface (GUI) that allows you to
a. Plot the entire graph (2D drawing using black or blue lines and points)
b. Select start and end points from pull-down menus
c. Display a list of shortest path or found paths, depending on user selection 
(utilize your graph class and add methods to get the information, if not yet implemented)
d. If the user selects “shortest path”, plot that path using a red line
e. Make sure scaling the window does not mess up your plot!
f. Draw a map image (USmap.png) behind the flight paths using wx.DrawBitmap. 
You will need to load the map as device independent wx.Image and convert that to wx.Bitmap before drawing the map. 
Make sure map and plot align (scaling problem). 
The provided map requires an alternative mapping of longitude and latitude as follows:
x = R * (longitude0 – longitude)
y = R * (tan(latitude) – tan(latitude0))
with R the radius of Earth and longitude0 the longitude of the left edge of the map, 
and latitude0 the latitude of the bottom of the map.
