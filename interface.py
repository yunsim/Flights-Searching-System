import wx
import sqlite3 as db
import Graph
from IDs import *
from math import *

class interface(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, frame_id, 'flight tool', size=(1000,500))
        self.graph = Graph.Graph()
        '''
        panels
        '''
        self.panel1 = wx.Panel(self,panel1_id,style=wx.BORDER)
        self.panel2 = wx.Panel(self,panel2_id,style=wx.BORDER)
        self.panel3 = wx.Panel(self,panel3_id,style=wx.BORDER)
        self.panel4 = wx.Panel(self,panel4_id,style=wx.BORDER)
        self.panel5 = wx.Panel(self,panel5_id,style=wx.BORDER)
        self.panel6 = wx.Panel(self,panel6_id,style=wx.BORDER)
        
        #panel sizer
        vSizer1 = wx.BoxSizer(wx.VERTICAL)
        vSizer1.Add(self.panel1,3,wx.EXPAND)
        vSizer1.Add(self.panel2,2,wx.EXPAND)
        vSizer1.Add(self.panel3,8,wx.EXPAND)
        vSizer1.Add(self.panel4,1,wx.EXPAND)
        vSizer2 = wx.BoxSizer(wx.VERTICAL)
        vSizer2.Add(self.panel5,3,wx.EXPAND)
        vSizer2.Add(self.panel6,1,wx.EXPAND)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(vSizer1,1,wx.EXPAND)
        hSizer.Add(vSizer2,4,wx.EXPAND)
        self.SetSizer(hSizer)
        
        
        '''
        panel1
        '''
        self.stDep = wx.StaticText(self.panel1, sTextDep_id, label="departure:")
        self.stDes = wx.StaticText(self.panel1, sTextDes_id, label="destination")
        self.cbDep = wx.ComboBox(self.panel1, cBoxDep_id, choices = self.graph.getAirportCodes())
        self.cbDes = wx.ComboBox(self.panel1, cBoxDes_id, choices = self.graph.getAirportCodes())
        self.btRvs = wx.Button(self.panel1, btRvs_id, label='reverse direction')
        #sizer
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer1.Add(self.stDep, 1, wx.ALIGN_CENTER)
        hSizer1.Add(self.cbDep, 1, wx.ALIGN_CENTER)
        hSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer2.Add(self.stDes, 1, wx.ALIGN_CENTER)
        hSizer2.Add(self.cbDes, 1, wx.ALIGN_CENTER)
        hSizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer3.Add(self.btRvs, 1, wx.ALIGN_CENTER)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(hSizer1, 1, wx.EXPAND)
        vSizer.Add(hSizer2, 1, wx.EXPAND)
        vSizer.Add(hSizer3, 1, wx.ALIGN_CENTER)
        self.panel1.SetSizer(vSizer)
        
        '''
        panel2
        '''
        self.btSchS = wx.Button(self.panel2, btSchS_id, label='search shortest')
        self.btSchA = wx.Button(self.panel2, btSchA_id, label='search all')
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.btSchS, 1, wx.ALIGN_CENTER)
        vSizer.Add(self.btSchA, 1, wx.ALIGN_CENTER)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(vSizer,1,wx.ALIGN_CENTER)
        self.panel2.SetSizer(hSizer)
        
        '''
        panel3
        '''
        self.btRV = wx.Button(self.panel3, btRV_id, label='reset view')
        #self.btRefresh = wx.Button(self.panel3, -1, label='refresh')
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.btRV, 1, wx.ALIGN_CENTER)
        #vSizer.Add(self.btRefresh, 1, wx.ALIGN_CENTER)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(vSizer,1,wx.ALIGN_CENTER)
        self.panel3.SetSizer(hSizer)
    
        
        '''
        panel4
        '''
        self.btQuit = wx.Button(self.panel4, btQuit_id, label='quit')
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.btQuit, 1, wx.ALIGN_CENTER)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(vSizer,1,wx.ALIGN_CENTER)
        self.panel4.SetSizer(hSizer)
        
        '''
        panel5
        '''
        self.panel5.Bind(wx.EVT_PAINT, self.onPaint)
        self.panel5.Bind(wx.EVT_SIZE, self.onSize)
        
        '''
        panel6
        '''
        self.tc = wx.TextCtrl(self.panel6, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.SUNKEN_BORDER)
        vSizer = wx.BoxSizer(wx.VERTICAL)
        vSizer.Add(self.tc, 1, wx.EXPAND)
        hSizer = wx.BoxSizer(wx.HORIZONTAL)
        hSizer.Add(vSizer,1,wx.EXPAND)
        self.panel6.SetSizer(hSizer)
        '''
        global variables
        '''
        # the shortest path
        self.shortestPath = []
        self.lineList = self.graph.getLineEndPositions()
        '''
        sources
        '''
        self.img = wx.Image('map.png')
        
        
        '''
        event
        '''
       
        wx.EVT_BUTTON(self, btRvs_id, self.onRvsDirection)
        wx.EVT_BUTTON(self, btSchS_id, self.onSchShortest)
        wx.EVT_BUTTON(self, btSchA_id, self.onSchAll)
        wx.EVT_BUTTON(self, btRV_id, self.onResetView)
        wx.EVT_BUTTON(self, btQuit_id, self.onQuit)
        wx.EVT_TEXT(self, cBoxDep_id, self.onClear)
        wx.EVT_TEXT(self, cBoxDes_id, self.onClear)
        #self.btRefresh.Bind(wx.EVT_BUTTON, self.onRefresh)
        self.Show()
        
        
    def onSize(self,e):
        self.Refresh()
     
    def onClear(self, e):
        '''
        When either comobox is set to a new value, or the button reverse direction is clicked,
        clear the textbox and the shortest line in the graph 
        '''
        self.tc.Clear()
        dc = wx.ClientDC(self.panel5)
        img = self.img
        pnSize = self.panel5.GetSize()
        imgSize = img.GetSize()
        newPosLength = 0
        newPosHeight = 0
        if (imgSize[0]*1.0/imgSize[1]>pnSize[0]*1.0/pnSize[1]):
            # if the image l/b larger than that of panel
            # the image's length should be the same as that of the panel
            newImgLength = pnSize[0]
            newImgHeight = pnSize[0]*imgSize[1]/imgSize[0]
            newPosHeight = (pnSize[1]-newImgHeight)/2
        else:
            newImgHeight = pnSize[1]
            newImgLength = pnSize[1]*imgSize[0]/imgSize[1]
            newPosLength = (pnSize[0]-newImgLength)/2
        #print newPosLength, newPosHeight
        img = img.Scale(newImgLength, newImgHeight)
        png = img.ConvertToBitmap()
        dc.DrawBitmapPoint(png, (newPosLength, newPosHeight))
        # draw dots
        
        # draw lines
        unit=(pnSize[0]+pnSize[1])/100
        k=unit
        #k is the coefficient for the middle point of the spline
        #initialize the previous positions 
        (x1, x2, y1, y2)=(0, 0, 0, 0)
        dc.SetPen(wx.Pen('BLUE'))
        for item in self.lineList:
            (bPosX, bPosY) = self.convPosition((newImgLength, newImgHeight),(item[0],item[1]))
            (ePosX, ePosY) = self.convPosition((newImgLength, newImgHeight),(item[2],item[3]))
            (x3,y3, x4, y4) = (bPosX+newPosLength, bPosY+newPosHeight, ePosX+newPosLength, ePosY+newPosHeight)
            if (x1==x3 and x2==x4 and y1==y3 and y2==y4):
                k=k+unit
            else:
                k=unit
            x1=x3
            x2=x4
            y1=y3
            y2=y4
            #(xm, ym)is the middle point for spline 
            xm=(x1+x2)/2
            ym=(y1+y2)/2
            (rx, ry)=self.verticalVect(x1, y1, x2, y2)
            '''
            (rx,ry)is a vector with length of 1 vertical to the vector from 1 to 2
            '''
            xm=xm+k*rx
            ym=ym+k*ry
            dc.DrawSpline(((x1,y1),(xm,ym),(x2,y2)))
        dc.SetPen(wx.Pen('Black'))
        airportList = self.graph.getAirportPositions()
        for item in airportList:
            imgPos = self.convPosition((newImgLength, newImgHeight),(item[1],item[2]))
            dc.DrawCircle(imgPos[0]+newPosLength, imgPos[1]+newPosHeight,5)
            dc.DrawText(item[0],imgPos[0]+newPosLength+5, imgPos[1]+newPosHeight+5 )
            
        
        
    def onRvsDirection(self,e):
        '''
        button reverse direction
        reset the choice for two combo box
        '''
        temp=self.cbDep.GetValue()
        self.cbDep.SetValue(self.cbDes.GetValue())
        self.cbDes.SetValue(temp)
        self.onClear(e)
        
    
    def onSchShortest(self,e):
        '''
        button search shortest
        1. get the choice from combo box
        2. find the shortest path using self.graph
        3. return text output and set to textCtrl value
        4. get the coordinates of the cities along the path
        5. call function convPosition() to convert from longitute/latitute to screen coordinates and save them to global variables
        6. draw lines on bitmap
        '''
        '''
        draw original map and lines
        ???why need draw here
        '''
        
        dc = wx.ClientDC(self.panel5)
        img = self.img
        pnSize = self.panel5.GetSize()
        imgSize = img.GetSize()
        newPosLength = 0
        newPosHeight = 0
        if (imgSize[0]*1.0/imgSize[1]>pnSize[0]*1.0/pnSize[1]):
            # if the image l/b larger than that of panel
            # the image's length should be the same as that of the panel
            newImgLength = pnSize[0]
            newImgHeight = pnSize[0]*imgSize[1]/imgSize[0]
            newPosHeight = (pnSize[1]-newImgHeight)/2
        else:
            newImgHeight = pnSize[1]
            newImgLength = pnSize[1]*imgSize[0]/imgSize[1]
            newPosLength = (pnSize[0]-newImgLength)/2
        #print newPosLength, newPosHeight
        img = img.Scale(newImgLength, newImgHeight)
        png = img.ConvertToBitmap()
        dc.DrawBitmapPoint(png, (newPosLength, newPosHeight))
        # draw dots
        
           
        # draw lines
        unit=(pnSize[0]+pnSize[1])/100
        k=unit
        #k is the coefficient for the middle point of the spline
        #initialize the previous positions 
        (x1, x2, y1, y2)=(0, 0, 0, 0)
        dc.SetPen(wx.Pen('BLUE'))
        for item in self.lineList:
            (bPosX, bPosY) = self.convPosition((newImgLength, newImgHeight),(item[0],item[1]))
            (ePosX, ePosY) = self.convPosition((newImgLength, newImgHeight),(item[2],item[3]))
            (x3,y3, x4, y4) = (bPosX+newPosLength, bPosY+newPosHeight, ePosX+newPosLength, ePosY+newPosHeight)
            if (x1==x3 and x2==x4 and y1==y3 and y2==y4):
                k=k+unit
            else:
                k=unit
            x1=x3
            x2=x4
            y1=y3
            y2=y4
            #(xm, ym)is the middle point for spline 
            xm=(x1+x2)/2
            ym=(y1+y2)/2
            (rx, ry)=self.verticalVect(x1, y1, x2, y2)
            '''
            (rx,ry)is a vector with length of 1 vertical to the vector from 1 to 2
            '''
            xm=xm+k*rx
            ym=ym+k*ry
            dc.DrawSpline(((x1,y1),(xm,ym),(x2,y2)))
         
        departure = self.cbDep.GetValue()
        destin = self.cbDes.GetValue()
        
        if departure == destin:
            self.tc.SetValue('Departure airport and destination airport are the same!')
        else:
            # set txtCtrl value
            schResult = self.graph.findShortestPath(departure, destin)
            self.shortestPath = schResult[1]
            self.tc.SetValue(schResult[0])
            dc.SetPen(wx.Pen('RED'))
            for item in schResult[1]:
                # draw lines
                (bPosX, bPosY) = self.convPosition((newImgLength, newImgHeight),(item[0],item[1]))
                (ePosX, ePosY) = self.convPosition((newImgLength, newImgHeight),(item[2],item[3]))
                (x1,y1, x2, y2) = (bPosX+newPosLength, bPosY+newPosHeight, ePosX+newPosLength, ePosY+newPosHeight)
                xm=(x1+x2)/2
                ym=(y1+y2)/2
                (rx, ry)=self.verticalVect(x1, y1, x2, y2)
                xm=xm+unit*rx
                ym=ym+unit*ry
                dc.DrawSpline(((x1,y1),(xm,ym),(x2,y2)))
                dc.SetTextForeground('Red')
                dc.DrawText(item[4], xm, ym)
                dc.SetTextForeground('Black')
        dc.SetPen(wx.Pen('Black'))
        airportList = self.graph.getAirportPositions()
        for item in airportList:
            imgPos = self.convPosition((newImgLength, newImgHeight),(item[1],item[2]))
            dc.DrawCircle(imgPos[0]+newPosLength, imgPos[1]+newPosHeight,5)
            dc.DrawText(item[0],imgPos[0]+newPosLength+5, imgPos[1]+newPosHeight+5 )
         
         
            
    def verticalVect(self, x1, y1, x2, y2):
        e=(y2-y1)/(x1-x2)
        if (y1-y2>0):
            ry=sqrt(1/(1+e*e))
        else:
            ry=-sqrt(1/(1+e*e))
        rx=ry*(y2-y1)/(x1-x2)
        return (rx, ry)
    
    def onSchAll(self,e):
        '''
        button search shortest
        1. get the choice from combo box
        2. find all the path using self.graph
        3. return text output and set to textCtrl value
        '''
        departure = self.cbDep.GetValue()
        destin = self.cbDes.GetValue()
        if departure == destin:
            self.tc.SetValue('Departure airport and destination airport are the same!')
        else:
            # set txtCtrl value
            schResult = self.graph.findAll(departure, destin)
            self.tc.SetValue(schResult)
        
    #def onRefresh(self,e):
     #   self.Refresh()
    
    def onResetView(self,e):
        '''
        button reset view
        reset window size
        '''
        fullSize = wx.DisplaySize()
        self.SetSize((fullSize[0]/2, fullSize[1]/2))
        self.Center()
        self.Refresh()
    
    def onQuit(self,e):
        '''
        button close window
        '''
        self.Close()
    
    def onPaint(self,e):
        '''
        draw sth on panel5
        '''
        # set dc
        dc = wx.PaintDC(self.panel5)
        #dc.Clear()
        img=self.img.Copy()
        # plot picture
        pnSize = self.panel5.GetSize()
        imgSize = img.GetSize()
        newPosLength = 0
        newPosHeight = 0
        if (imgSize[0]*1.0/imgSize[1]>pnSize[0]*1.0/pnSize[1]):
            # if the image l/b larger than that of panel
            # the image's length should be the same as that of the panel
            newImgLength = pnSize[0]
            newImgHeight = pnSize[0]*imgSize[1]/imgSize[0]
            newPosHeight = (pnSize[1]-newImgHeight)/2
        else:
            newImgHeight = pnSize[1]
            newImgLength = pnSize[1]*imgSize[0]/imgSize[1]
            newPosLength = (pnSize[0]-newImgLength)/2
        #print newPosLength, newPosHeight    
        img = img.Scale(newImgLength, newImgHeight)
        png = img.ConvertToBitmap()
        dc.DrawBitmapPoint(png, (newPosLength, newPosHeight))
        # draw blue lines
        dc.SetPen(wx.Pen('BLUE'))
        unit=(pnSize[0]+pnSize[1])/100
        k=unit
        (x1, x2, y1, y2)=(0, 0, 0, 0)
        for item in self.lineList:
            (bPosX, bPosY) = self.convPosition((newImgLength, newImgHeight),(item[0],item[1]))
            (ePosX, ePosY) = self.convPosition((newImgLength, newImgHeight),(item[2],item[3]))
            (x3,y3, x4, y4) = (bPosX+newPosLength, bPosY+newPosHeight, ePosX+newPosLength, ePosY+newPosHeight)
            if (x1==x3 and x2==x4 and y1==y3 and y2==y4):
                k=k+unit
            else:
                k=unit
            x1=x3
            x2=x4
            y1=y3
            y2=y4
            #(xm, ym)is the middle point for spline 
            xm=(x1+x2)/2
            ym=(y1+y2)/2
            (rx, ry)=self.verticalVect(x1, y1, x2, y2)
            '''
            
            #(rx,ry)is a vector with length of 1 vertical to the vector from 1 to 2
            e=(y2-y1)/(x1-x2)
            ry=sqrt(1/(1+e*e))
            rx=ry*(y2-y1)/(x1-x2)
            '''
            xm=xm+k*rx
            ym=ym+k*ry
            dc.DrawSpline(((x1,y1),(xm,ym),(x2,y2)))
            
        # draw red lines: shortestpath
        dc.SetPen(wx.Pen('RED'))
        (x1, x2, y1, y2)=(0, 0, 0, 0)
        for item in self.shortestPath:
            (bPosX, bPosY) = self.convPosition((newImgLength, newImgHeight),(item[0],item[1]))
            (ePosX, ePosY) = self.convPosition((newImgLength, newImgHeight),(item[2],item[3]))
            (x1,y1, x2, y2) = (bPosX+newPosLength, bPosY+newPosHeight, ePosX+newPosLength, ePosY+newPosHeight)
            xm=(x1+x2)/2
            ym=(y1+y2)/2
            (rx, ry)=self.verticalVect(x1, y1, x2, y2)
            xm=xm+unit*rx
            ym=ym+unit*ry
            dc.DrawSpline(((x1,y1),(xm,ym),(x2,y2)))
            dc.SetTextForeground('Red')
            dc.DrawText(item[4], xm, ym)
            dc.SetTextForeground('Black')
        # draw dots
        dc.SetPen(wx.Pen('Black'))
        airportList = self.graph.getAirportPositions()
        for item in airportList:
            imgPos = self.convPosition((newImgLength, newImgHeight),(item[1],item[2]))
            dc.DrawCircle(imgPos[0]+newPosLength, imgPos[1]+newPosHeight,5)
            dc.DrawText(item[0],imgPos[0]+newPosLength+5, imgPos[1]+newPosHeight+5 )
        
        
        
    def convPosition(self, imgSize, pos):
        '''
        convert longitute/latitude to location on Screen
        each item in posList is a tuple containing longitute and latitute of the city/airport
        '''
        xLeft = 128.26
        yTop = 53.00
        xRight = 65.16
        yBottom = 23.62  
        x =  (pos[0]-xLeft)*imgSize[0]/(xRight-xLeft)
        y =  (pos[1]-yTop)*imgSize[1]/(yBottom-yTop)
        return (x,y)
        
ftApp = wx.App()
ftFrame = interface()
ftApp.MainLoop()    