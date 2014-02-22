'''
Created on Jun 2, 2013

@author: Matthew
'''
import Tkinter as tk
import tkMessageBox as tkm
import math
import random
import itertools

def event_lambda(f, *args, **kwds ): # function found online for arguments in binding
    return lambda event, f=f, args=args, kwds=kwds : f( *args, **kwds )

def createhexagonCoords(ccX, ccY, SideLength): # cc = center coordinate  
    ccx = float(ccX)
    ccy = float(ccY)
    s = float(SideLength)
    topLeftX = ccx-(s/2.0)
    topLeftY = ccy-(s*math.sqrt(3.0)/2.0)
    topRightX = ccx+(s/2.0)
    topRightY = ccy-(s*math.sqrt(3.0)/2.0)
    RightX = ccx+s
    RightY = ccy
    bottomRightX = ccx+(s/2.0)
    bottomRightY = ccy+(s*math.sqrt(3.0)/2.0)
    bottomLeftX = ccx-(s/2.0)
    bottomLeftY = ccy+(s*math.sqrt(3.0)/2.0)
    LeftX = ccx-s
    LeftY = ccy
    return [topLeftX,topLeftY,topRightX,topRightY,RightX,RightY,bottomRightX,bottomRightY,bottomLeftX,bottomLeftY,LeftX,LeftY]    
                             
def createCenterCoordList(ccX, ccY, SideLength, NumOfRings):             
    returnList= []
    ccx = float(ccX)
    ccy = float(ccY)
    s = float(SideLength)
    for ring in range(0, NumOfRings):
        if ring == 0:
            returnList.append([ccx, ccy])
        else:            
            startX = ccx
            startY = ccy-(ring*s*math.sqrt(3.0))
            for hexagon in range(0, ring): # top right side
                startX = startX+(s*1.5)
                startY = startY+(s*math.sqrt(3.0)/2.0)
                returnList.append([round(startX*1000000.0)/1000000.0, round(startY*1000000.0)/1000000.0])
            for hexagon in range(0, ring): # right side
                startX = startX
                startY = startY+(s*math.sqrt(3.0))
                returnList.append([round(startX*1000000.0)/1000000.0, round(startY*1000000.0)/1000000.0])
            for hexagon in range(0, ring): # bottom right side
                startX = startX-(s*1.5)
                startY = startY+(s*math.sqrt(3.0)/2.0)
                returnList.append([round(startX*1000000.0)/1000000.0, round(startY*1000000.0)/1000000.0])
            for hexagon in range(0, ring): # bottom left side
                startX = startX-(s*1.5)
                startY = startY-(s*math.sqrt(3.0)/2.0)
                returnList.append([round(startX*1000000.0)/1000000.0, round(startY*1000000.0)/1000000.0])
            for hexagon in range(0, ring): # left side
                startX = startX
                startY = startY-(s*math.sqrt(3.0))
                returnList.append([round(startX*1000000.0)/1000000.0, round(startY*1000000.0)/1000000.0])
            for hexagon in range(0, ring): # top left side
                startX = startX+(s*1.5)
                startY = startY-(s*math.sqrt(3.0)/2.0)
                returnList.append([round(startX*1000000.0)/1000000.0, round(startY*1000000.0)/1000000.0])
    return returnList 
class CataanGUI():
    def __init__(self, root, players, rings):                
        HexCount = 1                    
        self.chanceDict = {}        
        self.windowHeight = 500.0          
        self.windowWidth = self.windowHeight
        self.NumofRings = rings
        self.sideLength = round((self.windowHeight/(2.0*self.NumofRings*math.sqrt(3.0)))*1000000.0)/1000000.0  
        self.NumofPlayers = players
        self.playerColorDict = {"1":"red","2":"blue","3":"tan","4":"light green","5":"aquamarine","6":"purple","7":"dodger blue","8":"salmon","9":"magenta",\
"10":"sea green","11":"turquoise","12":"violet","13":"khaki","14":"chocolate","15":"maroon","16":"gold","17":"plum","18":"thistle","19":"coral",\
"20":"firebrick","21":"pink","22":"sienna","23":"azure","24":"snow","25":"aquamarine","26":"azure","27":"lavender","28":"seashell",\
"29":"mint cream","30":"pale turquoise", "31":"brown"}             
        self.turn = 1
        self.player = "1"
        self.currentPlayer = self.turn % self.NumofPlayers        
        self.diceRolled = False
        self.mouseFocus = False
        self.beginSettlement = False        
        self.beginRoad = False
        self.roadCard = 3
        self.justPickedCards = []
        self.beginCity = False
        self.nextStage = False
        self.robberMove = False
        self.steal = False
        self.losingCards = False
        self.playersToLoseCards = {}
        self.knight = False
        self.monopoly = False
        self.takeCards = 0
        self.reverseOrder = 1
        self.firstTrader = 1
        self.secondTrader = None
        self.CityDictionary = {}
        self.PortDictionary = {}       
        self.largestArmy = ["None",0]
        self.longestRoad = ["None",0]
        self.longestRoadPlayer = None
        self.currentcardList = [] # list of cards in player display window
        self.window = tk.Frame(root)
        self.window.pack()
        self.mapAndTradeFrame = tk.Frame(self.window)
        self.mapAndTradeFrame.pack(side=tk.TOP)
        self.mapFrame = tk.Frame(self.mapAndTradeFrame)
        self.mapFrame.pack(side=tk.LEFT)        
        self.map = tk.Canvas(self.mapFrame, height=self.windowHeight, width=self.windowWidth)    
        self.map.bind("<Button-1>", self.buildAll)
        self.map.pack()    
########### Settlement Coordinates Creation                   
        self.SettlementCoordPairs = []
        self.SettlementCoordinates = []
        self.SettlementItemToCoordDict = {}
        self.SettlementItemToHexCoordDict = {}
        self.centerX = self.windowWidth/2.0
        self.centerY = self.windowHeight/2.0
        for CoordPair in createCenterCoordList(self.centerX, self.centerY, self.sideLength, self.NumofRings):
            for XorY in createhexagonCoords(CoordPair[0], CoordPair[1], self.sideLength):
                AccurateXorY = round(XorY*1000000.0)/1000000.0 # makes accurate to 6 decimals
                self.SettlementCoordinates.append(AccurateXorY) # adds each coordinate to a giant list        
        while len(self.SettlementCoordinates): # not 0 aka False
            if (self.SettlementCoordinates[0], self.SettlementCoordinates[1]) not in self.SettlementCoordPairs:
                self.SettlementCoordPairs.append((self.SettlementCoordinates[0], self.SettlementCoordinates[1]))
            self.SettlementCoordinates.pop(0) # pops X
            self.SettlementCoordinates.pop(0) # pops Y           
##################### Hex Creation      
        self.hexCoordDict = {}
        self.hexResourceDict = {}
        self.textFromCoordDict = {}
        for CoordPair in createCenterCoordList(self.windowWidth/2.0, self.windowHeight/2.0, self.sideLength, self.NumofRings):             
            resource = random.randint(1,6) 
            while resource == 6 and self.chanceDict.has_key(7): # makes sure there's only one desert
                resource = random.randint(1,6)
            if HexCount == len(createCenterCoordList(1,1,1, self.NumofRings)) and not self.chanceDict.has_key(7): # guarantees a desert. 1s are placeholders. Num of Rings is only important factor
                resource = 6
            if resource != 6: # if not desert
                diceRollNum = random.randint(2,12.0) 
                while diceRollNum == 7: # retries for non-desert number
                    diceRollNum = random.randint(2,12.0)    
            self.resourceDict = {1:["green", "wood"], 2:["brown", "clay"], 3:["white","wool"], 4:["grey", "ore"],5:["yellow", "corn"], 6:["khaki","desert"]}            
            
            hexagon = self.map.create_polygon(createhexagonCoords(CoordPair[0], CoordPair[1], self.sideLength), fill=self.resourceDict[resource][0], tags="hex")                                                          
            self.hexCoordDict[hexagon] = [CoordPair[0], CoordPair[1]]
            self.hexResourceDict[str([CoordPair[0], CoordPair[1]])] = self.resourceDict[resource][1] # sets it to string of material
            if resource != 6:
                self.map.addtag_withtag(str(diceRollNum), str(HexCount)) # adds roll number to the hex 
                text = self.map.create_text(CoordPair[0], CoordPair[1], text=str(diceRollNum))  
                self.textFromCoordDict[(CoordPair[0],CoordPair[1])] = [text, str(diceRollNum)]                          
                if self.chanceDict.has_key(diceRollNum): # makes a dictionary with coords of all hexes with certain roll                     
                    newList = self.chanceDict[diceRollNum] 
                    newList.append(CoordPair)
                    self.chanceDict[diceRollNum] = newList
                else:                    
                    self.chanceDict[diceRollNum] = [CoordPair]                
            else: # only for the one desert
                text = self.map.create_text(CoordPair[0], CoordPair[1], text="R")   
                self.textFromCoordDict[(CoordPair[0],CoordPair[1])] = [text, "D"]                     
                self.chanceDict[7] = [CoordPair] 
                self.robberCoords = CoordPair # place first Robber                
                self.robberPreviousText = "D"
            HexCount += 1            
############### Dev Card List
        self.VictoryPointCardList = ["Palace", "University", "Chapel", "Market", "Library"]
        self.ImprovementCardList = ["Monopoly", "Road Building", "Discovery"]
        self.DevCardUnusedList = []
        for iterative in range(self.NumofPlayers*5):
            self.DevCardUnusedList.append("Knight")
        for card in self.ImprovementCardList:
            for iterative in range(self.NumofPlayers/2):
                self.DevCardUnusedList.append(card)
############### Road Building
        self.RoadDictionary = {}         
        for CoordPair in self.SettlementCoordPairs:   
            for NearbyCoordPair in self.SettlementCoordPairs:
                if math.fabs(CoordPair[0]-NearbyCoordPair[0]) <= self.sideLength+1 and math.fabs(CoordPair[1]-NearbyCoordPair[1]) <= \
(math.sqrt(3.0)*self.sideLength/2.0)+1: # if adjacent
                    roadNumber = self.map.create_line(CoordPair[0], CoordPair[1], NearbyCoordPair[0], NearbyCoordPair[1], fill="black", tags="UnRoad")
                    self.RoadDictionary[roadNumber] = (CoordPair[0], CoordPair[1], NearbyCoordPair[0], NearbyCoordPair[1])          
        self.deleteRoads()      
############## Settlement Building here so roads don't show in settlement graphic square   
        for CoordPair in self.SettlementCoordPairs:
            if CoordPair not in self.SettlementItemToCoordDict.values(): #no copies                                
                nearbyHexCoords = []
                settlementNumber = self.map.create_rectangle(CoordPair[0]-9.0, CoordPair[1]-9.0, CoordPair[0]+9.0, CoordPair[1]+9.0, fill="black", tags="UnSettle")             
                self.SettlementItemToCoordDict[str(settlementNumber)] = CoordPair 
                for item in self.map.find_overlapping(CoordPair[0]-10.0, CoordPair[1]-10.0, CoordPair[0]+10.0, CoordPair[1]+10.0):
                    if "hex" in self.map.gettags(item):
                        nearbyHexCoords.append(self.hexCoordDict[item])                                    
                self.SettlementItemToHexCoordDict[item] = nearbyHexCoords                                                
############## Port Building
        self.portList = []     
        startX = self.centerX+(self.sideLength/2.0)      
        startY = self.centerY-((self.NumofRings*2-1)*(self.sideLength*math.sqrt(3.0)/2.0))             
        OverlapList = self.map.find_overlapping(startX, startY, startX, startY)                
        for item in OverlapList:            
            if item in self.map.find_withtag("UnSettle"):
                self.portList.append(str(item))          
        self.startX = self.SettlementItemToCoordDict[str(self.portList[0])][0]# string of item number is key, first part of tuple value is X
        self.startY = self.SettlementItemToCoordDict[str(self.portList[0])][1]# first settlement is starter   
        for iterative in range(1, self.NumofRings*2-1): #### Can't do a function because comparison is in input, but input must be after pair
            for pair in self.SettlementItemToCoordDict.items():   # TOP RIGHT 
                if iterative % 2 == 0:             
                    self.addPort(abs((pair[1][0]-self.startX)-self.sideLength) < .0001, abs(pair[1][1]-self.startY) < .00001, pair)                                                                
                if iterative % 2 == 1: #2nd and 4th ports
                    self.addPort(abs((pair[1][0]-self.startX)-self.sideLength/2.0) < .0001, abs((pair[1][1]-self.startY)-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)
        for iterative in range(0, self.NumofRings*2-1):      
            for pair in self.SettlementItemToCoordDict.items():   # RIGHT 
                if iterative % 2 == 1: #2nd and 4th ports
                    self.addPort(abs((self.startX-pair[1][0])-self.sideLength/2.0) < .0001, abs((pair[1][1]-self.startY)-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)
                if iterative % 2 == 0:             
                    self.addPort(abs((pair[1][0]-self.startX)-self.sideLength/2.0) < .0001, abs((pair[1][1]-self.startY)-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)                                                                                    
        for iterative in range(0, self.NumofRings*2-1):      
            for pair in self.SettlementItemToCoordDict.items():   # BOTTOM RIGHT 
                if iterative % 2 == 1:    #2nd and 4th ports          
                    self.addPort(abs((self.startX-pair[1][0])-self.sideLength) < .0001, abs(pair[1][1]-self.startY) < .00001, pair)                                                                
                if iterative % 2 == 0:
                    self.addPort(abs((self.startX-pair[1][0])-self.sideLength/2.0) < .0001, abs((pair[1][1]-self.startY)-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)
        for iterative in range(0, self.NumofRings*2-1):      
            for pair in self.SettlementItemToCoordDict.items():   # BOTTOM LEFT 
                if iterative % 2 == 1:    #2nd and 4th ports          
                    self.addPort(abs((self.startX-pair[1][0])-self.sideLength/2.0) < .0001, abs((self.startY-pair[1][1])-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)                                                                
                if iterative % 2 == 0:
                    self.addPort(abs((self.startX-pair[1][0])-self.sideLength) < .0001, abs(pair[1][1]-self.startY) < .00001, pair)
        for iterative in range(0, self.NumofRings*2-1):      
            for pair in self.SettlementItemToCoordDict.items():   # LEFT 
                if iterative % 2 == 1:    #2nd and 4th ports          
                    self.addPort(abs((pair[1][0]-self.startX)-self.sideLength/2.0) < .0001, abs((self.startY-pair[1][1])-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)                                                                
                if iterative % 2 == 0:
                    self.addPort(abs((self.startX-pair[1][0])-self.sideLength/2.0) < .0001, abs((self.startY-pair[1][1])-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)
        for iterative in range(0, self.NumofRings*2-1):      
            for pair in self.SettlementItemToCoordDict.items():   # TOP LEFT
                if iterative % 2 == 1:    #2nd and 4th ports          
                    self.addPort(abs((pair[1][0]-self.startX)-self.sideLength) < .0001, abs(pair[1][1]-self.startY) < .00001, pair)                                                                
                if iterative % 2 == 0:
                    self.addPort(abs((pair[1][0]-self.startX)-self.sideLength/2.0) < .0001, abs((self.startY-pair[1][1])-(self.sideLength*math.sqrt(3)/2.0)) < .00001, pair)        
        for port in self.portList:
            if self.portList.index(port) % 3 == 0: # one port every 3 coasts, or every other 2 settlements
                resource = random.randint(1,6)
                if str(resource) not in self.PortDictionary.keys():
                    self.PortDictionary[str(resource)] = [port, self.portList[self.portList.index(port)+1]] # creates port dictionary
                else:                    
                    newList = self.PortDictionary[str(resource)]
                    newList.append(port)
                    newList.append(self.portList[self.portList.index(port)+1])
                    self.PortDictionary[str(resource)] = newList # creates port dictionary        
        for key in self.PortDictionary.keys():
            resource = int(key)
            if resource == 1: # creates different resource types
                for index in range(0,len(self.PortDictionary[key]),2): # grabs every other port 
                    self.addPortText(key, index, "2:1 Wood", "green")                       
            elif resource == 2: # creates different resource types
                for index in range(0,len(self.PortDictionary[key]),2): # grabs every other port 
                    self.addPortText(key, index, "2:1 Clay", "brown")
            elif resource == 3: # creates different resource types
                for index in range(0,len(self.PortDictionary[key]),2): # grabs every other port 
                    self.addPortText(key, index, "2:1 Wool", "white")
            elif resource == 4: # creates different resource types
                for index in range(0,len(self.PortDictionary[key]),2): # grabs every other port 
                    self.addPortText(key, index, "2:1 Ore", "grey")
            elif resource == 5: # creates different resource types
                for index in range(0,len(self.PortDictionary[key]),2): # grabs every other port 
                    self.addPortText(key, index, "2:1 Corn", "yellow")
            elif resource == 6: # creates different resource types
                for index in range(0,len(self.PortDictionary[key]),2): # grabs every other port 
                    self.addPortText(key, index, "3:1 All", "khaki")
        self.portToResourceDict = {"1":"wood", "2":"clay", "3":"wool", "4":"ore", "5":"corn", "6":"all"}
############### Player Frame Creations        
        for row in range(int(math.ceil(self.NumofPlayers/16.0))):
            setattr(self, "playerFrame"+str(row), tk.Frame(self.window))
            getattr(self, "playerFrame"+str(row)).pack(side=tk.TOP)
        for player in range(1,self.NumofPlayers+1): # so starts at one, not zero
            stringPlayer = "player"+str(player)
            setattr(self, stringPlayer+"Frame", tk.Frame(getattr(self, "playerFrame"+str(player//16))))
            getattr(self, stringPlayer+"Frame").pack(side=tk.LEFT)
            setattr(self, stringPlayer+"Button", tk.Button(getattr(self,stringPlayer+"Frame"), text="Player "+str(player)+" VP: 2", relief=tk.RAISED))
            getattr(self, stringPlayer+"Button").bind("<Button-1>", event_lambda(self.changePlayerCards, stringPlayer))
            getattr(self, stringPlayer+"Button").config(bg=self.playerColorDict[str(player)])
            getattr(self, stringPlayer+"Button").pack(side=tk.TOP)
            setattr(self, stringPlayer+"BuildDict", {})
        getattr(self, "player1Button").config(fg="white") 
############## Building Utility Frame            
        self.utilityFrame = tk.Frame(self.window)
        self.utilityFrame.pack(side=tk.TOP)
        
        self.diceFrame = tk.Frame(self.utilityFrame)
        self.diceFrame.pack(side=tk.LEFT)
        self.diceButton = tk.Button(self.diceFrame, text = "Roll Dice")
        self.diceButton.bind("<Button-1>", self.rollDice)
        self.diceButton.pack(side=tk.TOP)
        self.diceLabel = tk.Label(self.diceFrame, text = "")
        self.diceLabel.pack(side=tk.TOP)    
        self.robberLabel = tk.Label(self.diceFrame, text = "Robber")
        self.robberLabel.pack(side=tk.TOP)     
        self.largestArmyLabel = tk.Label(self.diceFrame, text = "Largest Army")
        self.largestArmyLabel.pack(side=tk.TOP)
        self.diceRoll = None # only makes the variable
        
        self.turnFrame = tk.Frame(self.utilityFrame)        
        self.turnFrame.pack(side=tk.LEFT)
        self.turnButton = tk.Button(self.turnFrame, text = "End Turn")
        self.turnButton.bind("<Button-1>", self.endTurn)
        self.turnButton.pack()
        
        self.recipeFrame = tk.Frame(self.utilityFrame)
        self.recipeFrame.pack(side=tk.LEFT)
        self.settlementRecipe = tk.Label(self.recipeFrame, text="Wood, Clay, Corn, Wool")
        self.settlementRecipe.pack(side=tk.TOP)
        self.roadRecipe = tk.Label(self.recipeFrame, text="Wood, Clay")
        self.roadRecipe.pack(side=tk.TOP)
        self.cityRecipe = tk.Label(self.recipeFrame, text="Corn, Corn, Ore, Ore, Ore")
        self.cityRecipe.pack(side=tk.TOP)
        self.devCardRecipe = tk.Label(self.recipeFrame, text="Ore, Corn, Wool")
        self.devCardRecipe.pack(side=tk.TOP)
        
        self.buildFrame = tk.Frame(self.utilityFrame)
        self.buildFrame.pack(side=tk.LEFT)
        self.buildSettlementButton = tk.Button(self.buildFrame, text = "Build Settlement", width=15)
        self.buildSettlementButton.bind("<Button-1>", self.BeginBuildSettlement)
        self.buildSettlementButton.pack()        
        self.buildRoadButton = tk.Button(self.buildFrame, text = "Build Road", width=15)
        self.buildRoadButton.bind("<Button-1>", self.BeginBuildRoad)
        self.buildRoadButton.pack()
        self.buildCityButton = tk.Button(self.buildFrame, text = "Build City", width=15)
        self.buildCityButton.bind("<Button-1>", self.BeginBuildCity)
        self.buildCityButton.pack()
        self.pickCardButton = tk.Button(self.buildFrame, text = "Pick Card", width=15)
        self.pickCardButton.bind("<Button-1>", self.pickCard)
        self.pickCardButton.pack()
        
        self.defaultBG = self.buildSettlementButton.cget("bg") # allows for reset to originial background
################ Building Display Frame                        
        self.displayFrame = tk.Frame(self.utilityFrame)
        self.displayFrame.pack(side=tk.LEFT)
        self.resourceCardFrame = tk.Frame(self.displayFrame)
        self.resourceCardFrame.pack(side=tk.TOP)   
        self.devCardFrame = tk.Frame(self.displayFrame)
        self.devCardFrame.pack(side=tk.TOP)     
            
        for player in range(1,self.NumofPlayers+1):
            setattr(self, "player"+str(player)+"SettleList", [])
            setattr(self, "player"+str(player)+"CityList", [])
            setattr(self, "player"+str(player)+"DevCardList", [])
            setattr(self, "player"+str(player)+"ResourceCardList", [])
            setattr(self, "player"+str(player)+"RoadList", [])
            setattr(self, "player"+str(player)+"UsedKnightNumber", 0) 
            setattr(self, "player"+str(player)+"VP", 2) # two settle to start with
            setattr(self, "player"+str(player)+"RoadLength", 1) # two settle to start with
        setattr(self, "player"+str(self.NumofPlayers+1)+"ResourceCardList", ["wood", "wool", "ore", "corn", "clay"])
        self.changePlayerCards("player"+self.player)
        self.beginGame()
################ Building Trading Frame        
        self.tradeFrame = tk.Frame(self.mapAndTradeFrame)
        self.tradeFrame.pack(side=tk.LEFT)
        self.firstPlayerFrame = tk.Frame(self.tradeFrame)
        self.firstPlayerFrame.pack(side=tk.TOP)         
        self.currentTraderLabel = tk.Label(self.firstPlayerFrame, text="Current Player") # Current Player must be one of the traders
        self.currentTraderLabel.pack(side=tk.LEFT)
        self.firstResourceFrame = tk.Frame(self.tradeFrame)
        self.firstResourceFrame.pack(side=tk.TOP)
        for color, resource in self.resourceDict.values(): # all the resources for the top trader
            if resource != "desert":
                setattr(self, resource+"FirstResourceTradeFrame", tk.Frame(self.firstResourceFrame))
                getattr(self, resource+"FirstResourceTradeFrame").pack(side=tk.LEFT)
                setattr(self, resource+"FirstButton", tk.Button(getattr(self, resource+"FirstResourceTradeFrame"), text=resource, bg=color, width=6))
                getattr(self, resource+"FirstButton").bind("<Button-1>", event_lambda(self.stealMonopoly, resource))                
                getattr(self, resource+"FirstButton").pack(side=tk.TOP) 
                setattr(self, resource+"Amount1", tk.StringVar(root)) # creates variable for optionMenu
                getattr(self, resource+"Amount1").set(0)
                setattr(self, resource+"FirstMenuButton", tk.OptionMenu(getattr(self, resource+"FirstResourceTradeFrame"), \
getattr(self, resource+"Amount1"), 0,1,2,3,4)) 
                getattr(self, resource+"FirstMenuButton").pack(side=tk.LEFT)                                            
        for row in range(int(math.ceil(self.NumofPlayers/8.0))):
            setattr(self, "secondPlayerFrame"+str(row), tk.Frame(self.tradeFrame))
            getattr(self, "secondPlayerFrame"+str(row)).pack(side=tk.TOP)
        for player in range(1,self.NumofPlayers+2): # all the buttons for bottom trader
            if player == self.NumofPlayers+1:
                nameString = "CaravanRadioButton"
                textString = "Caravan"
            else:
                nameString = "Player"+str(player)+"RadioButton"
                textString = "Player "+str(player)
            setattr(self, nameString, tk.Radiobutton(getattr(self, "secondPlayerFrame"+str(player//8)), text=textString, \
variable=self.secondTrader, value=player))
            getattr(self, nameString).config(bg=self.playerColorDict[str(player)], indicatoron=0)
            getattr(self, nameString).bind("<Button-1>", event_lambda(self.updateTradeOptions, player))
            getattr(self, nameString).pack(side=tk.LEFT)
            if str(player) == self.player:
                getattr(self, nameString).config(state=tk.DISABLED)
        self.secondResourceFrame = tk.Frame(self.tradeFrame)
        self.secondResourceFrame.pack(side=tk.TOP)
        for color, resource in self.resourceDict.values(): # all the resources for the bottom trader
            if resource != "desert":
                setattr(self, resource+"SecondResourceTradeFrame", tk.Frame(self.secondResourceFrame))
                getattr(self, resource+"SecondResourceTradeFrame").pack(side=tk.LEFT)
                setattr(self, resource+"SecondButton", tk.Button(getattr(self, resource+"SecondResourceTradeFrame"), text=resource, bg=color, width=6))                
                getattr(self, resource+"SecondButton").bind("<Button-1>", event_lambda(self.DiscoverResource, resource))
                getattr(self, resource+"SecondButton").pack(side=tk.TOP) 
                setattr(self, resource+"Amount2", tk.StringVar(root)) # creates variable for optionMenu
                getattr(self, resource+"Amount2").set(0)
                setattr(self, resource+"SecondMenuButton", tk.OptionMenu(getattr(self, resource+"SecondResourceTradeFrame"), \
getattr(self, resource+"Amount2"), 0,1,2,3,4))                
                getattr(self, resource+"SecondMenuButton").pack(side=tk.LEFT) 
        self.tradeAndResetFrame = tk.Frame(self.tradeFrame)
        self.tradeAndResetFrame.pack(side=tk.TOP)
        self.tradeButton = tk.Button(self.tradeAndResetFrame, text="Trade", command=self.trade) # command instead of bind keeps buttons from staying sunken with dialogue
        self.tradeButton.pack(side=tk.LEFT)
        self.resetButton = tk.Button(self.tradeAndResetFrame, text="Reset", command=self.resetTrade) # command instead of bind keeps buttons from staying sunken with dialogue
        self.resetButton.pack(side=tk.LEFT)
#################################################################################################################### FUNCTIONS           
    def beginGame(self):
        self.beginGame = True
        self.beginSettlement = True                                            
    def addPort(self, Comparison1, Comparison2, pair):                    
        if Comparison1 and Comparison2:            
            self.portList.append(pair[0]) # finds the first and last ports in the circle
            self.startX = pair[1][0]
            self.startY = pair[1][1] 
    def addPortText(self, key, index, textStr, fillStr):
        value = self.PortDictionary[key][index]
        value2 = self.PortDictionary[key][index+1]                                                                     
        centerCoord = [(self.SettlementItemToCoordDict[value][0]+self.SettlementItemToCoordDict[value2][0])/2, \
(self.SettlementItemToCoordDict[value][1]+self.SettlementItemToCoordDict[value2][1])/2]   
        changeY = (math.sqrt(3)*self.sideLength/4.0)-(abs(self.SettlementItemToCoordDict[value][1]-self.SettlementItemToCoordDict[value2][1]))/2.0 # mid between points if vertically apart, else above/below              
        centerCoord[0] += 27*(centerCoord[0]-self.centerX)/abs(centerCoord[0]-self.centerX) # only changes the sign.
        centerCoord[1] += changeY*(centerCoord[1]-self.centerY)/abs(centerCoord[1]-self.centerY) 
        self.map.create_text(centerCoord[0],centerCoord[1],text=textStr)      
########## Utility Functions        
    def updateTradeOptions(self, player):   
        self.secondTrader=str(player) # makes available to other functions
    def resetTrade(self):
        if tkm.askquestion("Reset", "Reset all resource values?") == "yes":
            for color, resource in self.resourceDict.values(): # all the resources for the bottom trader
                if resource != "desert":
                    getattr(self, resource+"Amount1").set(0)
                    getattr(self, resource+"Amount2").set(0)
    def trade(self):
        if not self.beginCity and not self.beginRoad and not self.beginSettlement and not self.robberMove and not self.steal and not self.losingCards \
and self.diceRolled and not self.monopoly and self.takeCards == 0:
            trade = True
            firstTraderDict = {} # here to be available to caravan trade too
            firstTradeStr = ""
            secondTraderDict = {}
            secondTradeStr = ""
            if self.secondTrader == None:            
                tkm.showerror("Error", "You can't trade with nonexistent entities!") # elif statements, no trade = False necessary           
            elif self.secondTrader == str(self.NumofPlayers+1): # if caravan
                caravanGiving = 0.0
                playerGiving = 0.0
                ratioString = ""
                for key in self.portToResourceDict.keys():
                    setattr(self, self.portToResourceDict[key], False) # can I trade for better ratio?
                for key, valueList in self.PortDictionary.items():
                    for settlement in getattr(self, "player"+self.player+"SettleList"):
                        if str(settlement) in valueList:
                            setattr(self, self.portToResourceDict[key], True) # yes I can trade for better ratio.
                for color, resource in self.resourceDict.values():
                    if resource != "desert": 
                        caravanGiving += int(getattr(self, resource+"Amount2").get()) # finds out how many resources the player is receiving                
                for color, resource in self.resourceDict.values():
                    if resource != "desert":
                        if getattr(self, "player"+self.player+"ResourceCardList").count(resource) >= int(getattr(self, resource+"Amount1").get()):
                            if getattr(self, resource): # if tradable at 2:1
                                playerGiving += float(getattr(self, resource+"Amount1").get())/2.0 # playerGiving should equal caravanGiving because of this
                                ratioString += resource+" 2:1\n"                                
                            elif getattr(self, "all"): # if tradable at 3:1
                                playerGiving += float(getattr(self, resource+"Amount1").get())/3.0 # playerGiving should equal caravanGiving because of this
                                ratioString += resource+" 3:1\n"
                            else: # no ports
                                playerGiving += float(getattr(self, resource+"Amount1").get())/4.0 # playerGiving should equal caravanGiving because of this                            
                                ratioString += resource+" 4:1\n"                            
                            if getattr(self, resource+"Amount1").get() != "0": # has cards already established by bigger if
                                firstTraderDict[resource] = getattr(self, resource+"Amount1").get()
                            if getattr(self, resource+"Amount2").get() != "0":
                                secondTraderDict[resource] = getattr(self, resource+"Amount2").get()
                        elif getattr(self, "player"+self.player+"ResourceCardList").count(resource) < int(getattr(self, resource+"Amount1").get()):
                            trade = False
                            tkm.showerror("Error", "Player "+self.player+" does not have enough "+resource)
                if playerGiving != caravanGiving and trade: # the "and trade" keeps double erroring from occurring. Here the player has the resources but isn't trading correctly
                    trade = False
                    if playerGiving < caravanGiving:
                        tkm.showerror("Error", "The caravan traders want more. They'll trade with you at the following ratios:\n"+ratioString)
                    if playerGiving > caravanGiving:
                        tkm.showerror("Error", "You are giving the caravan traders too much. They'll trade with you at the following ratios:\n"+ratioString)
                for key in firstTraderDict.keys():
                    firstTradeStr += firstTraderDict[key]+" "+key
                    if firstTraderDict.keys().index(key) != len(firstTraderDict.keys())-1: # if not the last resource
                        firstTradeStr += " and "   
                for key in secondTraderDict.keys():
                    secondTradeStr += secondTraderDict[key]+" "+key
                    if secondTraderDict.keys().index(key) != len(secondTraderDict.keys())-1: # if not the last resource
                        secondTradeStr += " and "
                if trade and tkm.askquestion("Trade", "Please confirm this trade:\n"+\
                                "Player "+self.player+" is giving "+firstTradeStr+" to \n"\
                                "the caravan traders who are giving back "+secondTradeStr) == "yes":
                    for color, resource in self.resourceDict.values():
                        if resource != "desert":
                            number = int(getattr(self, resource+"Amount1").get())                            
                            for index in range(int(getattr(self, resource+"Amount2").get())):
                                getattr(self, "player"+self.player+"ResourceCardList").append(resource)
                            self.useUpCards(number, resource)
            else: # trade with other players                
                for color, resource in self.resourceDict.values(): # discovers which resources and how many are being traded
                    if resource != "desert":                                        
                        if getattr(self, resource+"Amount1").get() != "0":
                            if getattr(self, "player"+self.player+"ResourceCardList").count(resource) >= int(getattr(self, resource+"Amount1").get()):
                                firstTraderDict[resource] = getattr(self, resource+"Amount1").get()
                            else:
                                tkm.showerror("Error", "Player "+self.player+" does not have enough "+resource)
                        if getattr(self, resource+"Amount2").get() != "0":
                            if getattr(self, "player"+str(self.secondTrader)+"ResourceCardList")\
.count(resource) >= int(getattr(self, resource+"Amount2").get()):
                                secondTraderDict[resource] = getattr(self, resource+"Amount2").get()
                            else:
                                tkm.showerror("Error", "Player "+str(self.secondTrader)+" does not have enough "+resource)
                for key in firstTraderDict.keys():
                    firstTradeStr += firstTraderDict[key]+" "+key
                    if firstTraderDict.keys().index(key) != len(firstTraderDict.keys())-1: # if not the last resource
                        firstTradeStr += " and "
                if firstTradeStr == "":
                    firstTradeStr = "nothing" # outright giving is possible.
                for key in secondTraderDict.keys():
                    secondTradeStr += secondTraderDict[key]+" "+key
                    if secondTraderDict.keys().index(key) != len(secondTraderDict.keys())-1: # if not the last resource
                        secondTradeStr += " and "
                if secondTradeStr == "":
                    secondTradeStr = "nothing"
                if tkm.askquestion("Trade", "Please confirm this trade:\n"+\
                                "Player "+self.player+" is giving "+firstTradeStr+" to \n"\
                                "Player "+str(self.secondTrader)+", who is giving back "+secondTradeStr) == "yes": # if agreed to
                    for resource, amount in firstTraderDict.items():
                        self.useUpCards(int(amount), resource, True, self.player, str(self.secondTrader))                                         
                    for resource, amount in secondTraderDict.items():
                        self.useUpCards(int(amount), resource, True, str(self.secondTrader), self.player)
        elif self.beginGame:
            tkm.showerror("Error", "You must finish starting the game.")          
        elif not self.diceRolled:
            tkm.showerror("Error", "You must roll first.")  
        elif self.knight or self.robberMove or self.steal or self.losingCards or self.monopoly or self.takeCards > 0:
            tkm.showerror("Error", "You must finish moving the robber or taking cards.") 
        elif self.beginCity or self.beginRoad or self.beginSettlement:
            tkm.showerror("Error", "You must finish building.")
    def rollDice(self, event):
        if not self.diceRolled and not self.beginGame:
            self.diceRoll = random.randint(1,6)+random.randint(1,6) # keeps normal pattern of probability instead of even across the board        
            self.diceLabel.config(text=str(self.diceRoll))
            self.diceRolled = True
            self.changePlayerCards("player"+self.player)
            if self.diceRoll in self.chanceDict.keys():  # sometimes the roll will not be on the map                                        
                for hexCoordPair in self.chanceDict[self.diceRoll]: # for each hex giving resources this turn                                         
                    if self.hexResourceDict[str(hexCoordPair)] != "desert" and self.robberCoords != hexCoordPair:                        
                        for number in range(1,self.NumofPlayers+1): #List of each player's settlements                        
                            for settlement in getattr(self, "player"+str(number)+"SettleList"): # for each settlement of each player                                
                                if hexCoordPair in self.SettlementItemToHexCoordDict[settlement]: # if settlement on that hex                                                              
                                    getattr(self, "player"+str(number)+"ResourceCardList").append(self.hexResourceDict[str(hexCoordPair)]) 
                            for city in getattr(self, "player"+str(number)+"CityList"): # for each city of each player                                
                                if hexCoordPair in self.SettlementItemToHexCoordDict[city]: # if city on that hex, city has same item # as settle                                                              
                                    getattr(self, "player"+str(number)+"ResourceCardList").append(self.hexResourceDict[str(hexCoordPair)])                         
                        self.changePlayerCards("player"+self.player)
                    elif self.hexResourceDict[str(hexCoordPair)] == "desert":                        
                        self.changePlayerCards("player"+self.player)
                        self.robberLabel.config(bg="green")    
                        self.robberMove = True                                     
            self.diceButton.config(bg="green")                    
            
    def endTurn(self, event):        
        if not self.beginCity and not self.beginRoad and not self.beginSettlement and not self.robberMove and not self.steal and not self.losingCards \
and self.diceRolled and not self.monopoly and self.takeCards == 0:         
            for card in self.justPickedCards:
                getattr(self,"player"+self.player+"DevCardList").append(card)                  
            if not self.checkForWin(): # after cards are added, and only current player can win
                self.justPickedCards = [] # clears cards so they may be used
                getattr(self, "player"+self.player+"Button").config(fg="black") # before turn changes so it resets          
                self.turn += 1
                self.player = str(self.turn % self.NumofPlayers)            
                if self.player == "0":
                    self.player = str(self.NumofPlayers) # there is no player0. If 3rd turn with 3 players, % returns 0, not 3.
                self.updateTradeOptions(self.player)            
                self.diceRolled = False
                self.diceButton.config(bg=self.defaultBG)
                getattr(self, "player"+self.player+"Button").config(fg="white")
                self.secondTrader = None
                for player in range(1,self.NumofPlayers+2): # all the buttons for bottom trader
                    if player == self.NumofPlayers+1:
                        nameString = "CaravanRadioButton"
                        getattr(self, nameString).deselect()
                    else:
                        nameString = "Player"+str(player)+"RadioButton"
                        if str(player) == self.player:
                            getattr(self, nameString).config(state=tk.DISABLED)
                            getattr(self, nameString).deselect()
                        else:
                            getattr(self, nameString).deselect()
                            getattr(self, nameString).config(state=tk.NORMAL)
            else: 
                self.Win()                
    def changePlayerCards(self, strPlayer):
        if self.steal and getattr(self, strPlayer+"Button").cget("bg") == "green": # gets bg color. .cget("bg") can also just be ["bg"] 
            card = random.choice(getattr(self, strPlayer+"ResourceCardList"))
            getattr(self, strPlayer+"ResourceCardList").remove(card)
            getattr(self, "player"+self.player+"ResourceCardList").append(card) # steals a card
            self.steal = False
            for player in range(1, self.NumofPlayers+1):
                getattr(self, "player"+str(player)+"Button").config(bg=self.playerColorDict[str(player)]) # resets after stealing
            self.changePlayerCards("player"+self.player) # resets for current player           
        elif not self.steal and not self.robberMove:
            for variableName in self.currentcardList:
                getattr(self, variableName).destroy() # removes all cards previously in window
            number = 0
            for card in getattr(self, strPlayer+"DevCardList"):            
                cardName = str(card).replace(" ", "")
                variableName = cardName+str(number)
                number +=1 
                if card not in self.VictoryPointCardList and strPlayer == "player"+self.player: # must be current player to be button        
                    setattr(self, variableName, tk.Button(self.devCardFrame, text=str(card))) #makes card
                    getattr(self, variableName).bind("<Button-1>", event_lambda(getattr(self, "play"+cardName), card, variableName)) #binds playing ability function                                    
                else:
                    setattr(self, variableName, tk.Label(self.devCardFrame, text=str(card))) #makes card but VPs can't be played
                getattr(self, variableName).pack(side=tk.LEFT)
                self.currentcardList.append(variableName)        
            for card in getattr(self, strPlayer+"ResourceCardList"): 
                index = getattr(self, strPlayer+"ResourceCardList").index(card)           
                variableName = card+str(number)
                number += 1 # each card is unique
                setattr(self, variableName, tk.Button(self.resourceCardFrame, text=str(card))) #makes card
                getattr(self, variableName).bind("<Button-1>", event_lambda(self.loseCard, variableName, int(strPlayer[-1:]), card))
                getattr(self, variableName).pack(side=tk.LEFT)
                self.currentcardList.append(variableName)             
            setattr(self, "playerLabel", tk.Label(self.displayFrame, text="Player "+str(strPlayer)[-1:])) #last digit of strPlayer is number                
            getattr(self, "playerLabel").pack(side=tk.TOP)   
            self.currentcardList.append("playerLabel") # allows it to be destroyed
############# Build Functions     
    def hasCards(self, item):    
        hasCards = False
        if item == "settle":          
            if "clay" in getattr(self, "player"+self.player+"ResourceCardList"):                
                if "wool" in getattr(self, "player"+self.player+"ResourceCardList"):
                    if "wood" in getattr(self, "player"+self.player+"ResourceCardList"):
                        if "corn" in getattr(self, "player"+self.player+"ResourceCardList"):
                            hasCards = True
        if item == "road":
            if "clay" in getattr(self, "player"+self.player+"ResourceCardList"):      
                if "wood" in getattr(self, "player"+self.player+"ResourceCardList"):
                    hasCards = True
        if item == "city":
            if getattr(self, "player"+self.player+"ResourceCardList").count("ore") >= 3:
                if getattr(self, "player"+self.player+"ResourceCardList").count("corn") >= 2:
                    hasCards = True
        if item == "DevCard":
            if "ore" in getattr(self, "player"+self.player+"ResourceCardList"):                
                if "wool" in getattr(self, "player"+self.player+"ResourceCardList"):
                    if "corn" in getattr(self, "player"+self.player+"ResourceCardList"):
                        hasCards = True
        return hasCards
    def deleteRoads(self):
        deleteList = []      
        saveList = []    
        for roadItem in self.RoadDictionary.keys():
            lengthX = abs(self.RoadDictionary[roadItem][0]-self.RoadDictionary[roadItem][2]) 
            lengthY = abs(self.RoadDictionary[roadItem][1]-self.RoadDictionary[roadItem][3])
            length = math.sqrt((lengthX**2)+(lengthY**2))
            if length < 1.0: # if road connects to only one settlement, remove it. keeps next for loop from keeping an invalid road
                self.RoadDictionary.pop(roadItem)
                self.map.delete(roadItem)
        for roadItem in self.RoadDictionary.keys():
            foundRoad = False
            averageX = (self.RoadDictionary[roadItem][0]+self.RoadDictionary[roadItem][2])/2.0 
            averageY = (self.RoadDictionary[roadItem][1]+self.RoadDictionary[roadItem][3])/2.0
            for nearby in self.map.find_overlapping(averageX-1, averageY-1, averageX+1, averageY+1):
                if "UnRoad" in self.map.gettags(nearby) and nearby not in deleteList and nearby not in saveList:
                    if not foundRoad:
                        foundRoad = True # finds one road and deletes all others
                        saveList.append(nearby)
                    elif foundRoad:
                        deleteList.append(nearby) 
        for road in deleteList:
            if road not in saveList:
                self.RoadDictionary.pop(road)
                self.map.delete(road)
    def useUpCards(self, number, card, trade=False, givingPlayer=None, receivingPlayer=None):        
        for each in range(number):
            if not trade:
                getattr(self, "player"+self.player+"ResourceCardList").remove(card)
            elif trade: # if giving it to another:
                getattr(self, "player"+givingPlayer+"ResourceCardList").remove(card) # isn't necessarily the current player
                getattr(self, "player"+receivingPlayer+"ResourceCardList").append(card) 
        self.changePlayerCards("player"+self.player)                         
    def buildAll(self, event): # one binding does them all for clicking on canvas
        if self.diceRolled or self.beginGame: # dice must be rolled first
            self.buildSettlement(event)
            self.buildRoad(event)
            self.buildCity(event)
            if self.diceRoll == 7 or self.knight == True:
                self.moveRobber(event)
    def BeginBuildSettlement(self, event): # allows next click to build a settlement  
        if not self.beginGame and self.hasCards("settle"): # protects against inadvertent clicks at beginning  
            if self.beginSettlement: # resets on second click
                self.beginSettlement = False
                self.buildSettlementButton.config(bg=self.defaultBG)
            elif not self.beginRoad and not self.beginCity and not self.robberMove and not self.monopoly and self.takeCards == 0:
                self.beginSettlement = True
                self.buildSettlementButton.config(bg="green")
    def buildSettlement(self, event):  
        ListUnderMouse=self.map.find_overlapping(event.x,event.y,event.x+1,event.y+1) 
        self.settlementBuilt = False        
        for itemUnderMouse in ListUnderMouse:                    
            if self.beginSettlement: # allows first settlement
                if str(itemUnderMouse) in self.SettlementItemToCoordDict.keys() and "UnSettle" in self.map.gettags(itemUnderMouse) and \
(self.beginGame or self.hasCards("settle")) and self.adjacentSettleCheck(itemUnderMouse):                                                          
                    self.settlementBuilt = False   
                    self.map.itemconfig(itemUnderMouse, fill=self.playerColorDict[self.player]) #player is number, gives fill color
                    self.map.addtag_withtag("Settle", itemUnderMouse)                  
                    self.map.dtag(itemUnderMouse, "UnSettle")
                    getattr(self, "player"+self.player+"SettleList").append(itemUnderMouse)
                    self.beginSettlement = False # allows click to continue if missed. 
                    self.settlementBuilt = True                   
                    self.buildSettlementButton.config(bg=self.defaultBG)
                    if self.beginGame:
                        self.beginRoad = True # allows road after settlement is built
                        self.currentSettlement = itemUnderMouse
                        if self.reverseOrder == -1: # gives resources on second settlement
                            for hexCoords in self.SettlementItemToHexCoordDict[itemUnderMouse]:                                
                                if self.hexResourceDict[str(hexCoords)] != "desert":
                                    getattr(self, "player"+self.player+"ResourceCardList").append(self.hexResourceDict[str(hexCoords)])
                    else: # removes cards if not at beginning of game
                        self.useUpCards(1, "wool") 
                        self.useUpCards(1, "corn")
                        self.useUpCards(1, "clay")
                        self.useUpCards(1, "wood")
                    deleteList = []
                    for nearbySettle in self.SettlementItemToCoordDict.keys():   
                        if math.fabs(self.SettlementItemToCoordDict[str(itemUnderMouse)][0]-self.SettlementItemToCoordDict[nearbySettle][0]) <= \
self.sideLength+1 and math.fabs(self.SettlementItemToCoordDict[str(itemUnderMouse)][1]-self.SettlementItemToCoordDict[nearbySettle][1]) <= \
(math.sqrt(3.0)*self.sideLength/2.0)+1 and str(itemUnderMouse) != nearbySettle: # if adjacent, removes the possibilities of settling
                            deleteList.append(nearbySettle)
                    for deleted in deleteList:
                        self.map.delete(deleted)
                        self.SettlementItemToCoordDict.pop(deleted)
            if "UnSettle" in self.map.gettags(itemUnderMouse) and self.settlementBuilt: # other settlements in same place
                self.map.delete(itemUnderMouse) #removes settlement copies                                    
                self.SettlementItemToCoordDict.pop(str(itemUnderMouse))
                self.SettlementItemToHexCoordDict.pop(itemUnderMouse)
    def adjacentSettleCheck(self, settleItem):
        returnValue = False
        if self.beginGame:
            returnValue = True # must be adjacent to current settlement
        else:
            for road in getattr(self, "player"+self.player+"RoadList"):                
                if (self.SettlementItemToCoordDict[str(settleItem)] == (self.RoadDictionary[road][0], self.RoadDictionary[road][1])) or \
                (self.SettlementItemToCoordDict[str(settleItem)] == (self.RoadDictionary[road][2], self.RoadDictionary[road][3])):
                    returnValue = True         
        return returnValue                                          
    def BeginBuildRoad(self, event): # allows next click to build a settlement
        if not self.beginGame and self.hasCards("road") and self.roadCard >= 2: # protects against inadvertent clicks at beginning and dev card 
            if self.beginRoad: # resets on second click
                self.beginRoad = False
                self.buildRoadButton.config(bg=self.defaultBG) 
            elif not self.beginCity and not self.beginSettlement and not self.robberMove and not self.monopoly and self.takeCards == 0:
                self.beginRoad = True # continues
                self.buildRoadButton.config(bg="green")          
    def buildRoad(self, event):                
        inSettle = False
        self.roadBuilt = False              
        ListUnderMouse=self.map.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1) 
        for item in ListUnderMouse: # makes sure not clicking in a settlement
            if item in self.map.find_withtag("Settle") or item in self.map.find_withtag("UnSettle"):
                inSettle = True # sees if click is within a settlement, still possible because road goes to center of settlement              
        for itemUnderMouse in ListUnderMouse:
            if self.beginRoad and not self.roadBuilt:                                   
                if itemUnderMouse in self.RoadDictionary.keys() and not inSettle and "UnRoad" in self.map.gettags(itemUnderMouse) and \
(self.beginGame or self.hasCards("road") or self.roadCard < 2) and self.adjacentRoadCheck(itemUnderMouse):                                                           
                    self.map.itemconfig(itemUnderMouse, fill=self.playerColorDict[self.player], width=2, tags="Road")
                    getattr(self, "player"+self.player+"RoadList").append(itemUnderMouse)                                                                       
                    self.beginRoad = False # allows click to continue if missed.
                    self.buildRoadButton.config(bg=self.defaultBG)
                    self.roadBuilt = True
                    if not self.beginGame and self.roadCard >= 2:                   
                        self.useUpCards(1, "clay")
                        self.useUpCards(1, "wood")
                    if self.beginGame:                        
                        self.beginSettlement = True
                        self.player = str(int(self.player)+(1*self.reverseOrder)) # reverse order is either 1 or -1
                        if self.player == str(self.NumofPlayers+1):
                            self.reverseOrder = -1
                            self.player = str(self.NumofPlayers) 
                        if self.player == "0":
                            self.player = "1"
                            self.beginGame = False    
                            self.beginSettlement = False                                            
                    if self.roadCard < 2:
                        self.roadCard += 1
                        if self.roadCard < 2:
                            self.beginRoad = True
                            self.buildRoadButton.config(bg="green")                       
    def adjacentRoadCheck(self, roadItem): # checks for being next to own road or settlement, and not being cut
        returnValue = False
        roadsAvailableOnSide = False
        OneCoord = (self.RoadDictionary[roadItem][0],self.RoadDictionary[roadItem][1])        
        OtherCoord = (self.RoadDictionary[roadItem][2],self.RoadDictionary[roadItem][3])
        averageX = (self.RoadDictionary[roadItem][0]+self.RoadDictionary[roadItem][2])/2.0
        averageY = (self.RoadDictionary[roadItem][1]+self.RoadDictionary[roadItem][3])/2.0
        if self.beginGame:            
            for nearby in self.map.find_overlapping(averageX-self.sideLength/2.0, averageY-self.sideLength/2.0, averageX+self.sideLength/2.0, \
averageY+self.sideLength/2.0):  # finds only perfectly adjacent settlements, roads, and hexes
                if nearby == self.currentSettlement:
                    returnValue = True # must be adjacent to current settlement
        else:
            for nearby in self.map.find_overlapping(averageX-self.sideLength/2.0, averageY-self.sideLength/2.0, averageX+self.sideLength/2.0, \
averageY+self.sideLength/2.0):
                if nearby in getattr(self, "player"+self.player+"SettleList") or nearby in getattr(self, "player"+self.player+"CityList"):
                    returnValue = True # a city or settle of that player exists immediately adjacent
                elif nearby in getattr(self, "player"+self.player+"RoadList"): # player has adjacent road. Is it blocked? only checks if no settle or city nearby, which means if there is another settlement, it's not the player                  
                    for nearby in self.map.find_overlapping(OneCoord[0]-1,OneCoord[1]-1,OneCoord[0]+1,OneCoord[1]+1):
                        if nearby in getattr(self, "player"+self.player+"RoadList"):
                            roadsAvailableOnSide = True 
                        if "Settle" in self.map.gettags(nearby) or "City" in self.map.gettags(nearby): # another players because of previous if statement
                            roadsAvailableOnSide = False # no roads on this side possible
                            break # prevents other roads from changing their variable back, won't miss any if no settle exists
                    if not roadsAvailableOnSide: # means no settle or city and roads available, auto pass road can be built
                        for nearby in self.map.find_overlapping(OtherCoord[0]-1,OtherCoord[1]-1,OtherCoord[0]+1,OtherCoord[1]+1):
                            if nearby in getattr(self, "player"+self.player+"RoadList"):
                                roadsAvailableOnSide = True 
                            if "Settle" in self.map.gettags(nearby) or "City" in self.map.gettags(nearby): # another players because of previous if statement
                                roadsAvailableOnSide = False # no roads on this side possible
                                break # prevents other roads from changing their variable back, won't miss any if no settle exists
                    if roadsAvailableOnSide:
                        returnValue = True
        return returnValue             
    def BeginBuildCity(self, event): # allows next click to build a settlement
        if not self.beginGame and self.hasCards("city"): # protects against inadvertent clicks at beginning
            if self.beginCity: # resets on second click
                self.beginCity = False
                self.buildCityButton.config(bg=self.defaultBG)
            elif not self.beginRoad and not self.beginSettlement and not self.robberMove and not self.monopoly and self.takeCards == 0:
                self.beginCity = True        
                self.buildCityButton.config(bg="green")
    def buildCity(self, event):
        if self.beginCity:     
            ListUnderMouse=self.map.find_overlapping(event.x,event.y,event.x+1,event.y+1) 
            for itemUnderMouse in ListUnderMouse:
                if itemUnderMouse in getattr(self, "player"+self.player+"SettleList") and \
itemUnderMouse not in getattr(self, "player"+self.player+"CityList"): # checks it's a settlement and owned by current player
                    self.map.create_text(self.SettlementItemToCoordDict[str(itemUnderMouse)], text="C") 
                    getattr(self, "player"+self.player+"CityList").append(itemUnderMouse)         
                    self.beginCity = False # allows click to continue if missed.
                    self.buildCityButton.config(bg=self.defaultBG)
                    self.map.addtag_withtag("City", itemUnderMouse) # no longer a Settlement but a city
                    self.map.dtag(itemUnderMouse, "Settle")                    
                    self.useUpCards(3, "ore") 
                    self.useUpCards(2, "corn")
    def pickCard(self, event):        
        if self.diceRolled and len(self.DevCardUnusedList) > 0 and self.hasCards("DevCard") and not self.beginGame and not self.beginRoad and not \
self.beginSettlement and not self.robberMove and not self.steal and not self.losingCards and not self.monopoly and self.takeCards == 0:
            randomCard = random.choice(self.DevCardUnusedList)
            self.justPickedCards.append(randomCard) # cards are added at end of turn            
            self.DevCardUnusedList.remove(randomCard) 
            self.useUpCards(1, "ore") 
            self.useUpCards(1, "corn")
            self.useUpCards(1, "wool")                                        
################ Card Functions, only playable by current player
    def playKnight(self, card, variableName):
        self.knight = True          
        self.robberMove = True               
        self.robberLabel.config(bg="green")
        getattr(self, "player"+self.player+"DevCardList").remove(card)        
        getattr(self, variableName).destroy()
        setattr(self, "player"+self.player+"UsedKnightNumber", (getattr(self, "player"+self.player+"UsedKnightNumber")+1)) # for largest army
        if getattr(self, "player"+self.player+"UsedKnightNumber") > self.largestArmy[1]: # there will only ever be one value
            self.largestArmy = [self.player, getattr(self, "player"+self.player+"UsedKnightNumber")]
        if self.largestArmy[1] >= 3 and self.largestArmy[0] == self.player:
            self.largestArmyLabel.config(bg=self.playerColorDict[self.player])            
    def playMonopoly(self, card, variableName): # optional for anythig requiring two variables
        tkm.showinfo("Monopoly", "Click any resource in the top resource trading bar to take all players' cards of that resource.")
        self.monopoly = True            
        getattr(self, "player"+self.player+"DevCardList").remove(card)        
        getattr(self, variableName).destroy()
    def stealMonopoly(self, resource):
        if self.monopoly:
            for player in range(1, self.NumofPlayers+1):
                number = getattr(self, "player"+str(player)+"ResourceCardList").count(resource)
                self.useUpCards(number, resource, True, str(player), self.player)
            self.monopoly = False
    def playRoadBuilding(self, card, variableName):
        self.roadCard = 0
        self.beginRoad = True
        self.buildRoadButton.config(bg="green")
        getattr(self, "player"+self.player+"DevCardList").remove(card)
        getattr(self, variableName).destroy()
        self.changePlayerCards("player"+self.player)        
    def playDiscovery(self, card, variableName):
        tkm.showinfo("Discovery", "Click any two resources in the bottom resource trading bar to take a free card of that resource.\n"+\
                     "The resources may be both the same or different.")
        self.takeCards = 2 
        getattr(self, "player"+self.player+"DevCardList").remove(card)        
        getattr(self, variableName).destroy()
    def DiscoverResource(self, resource):
        if self.takeCards > 0:
            getattr(self, "player"+self.player+"ResourceCardList").append(resource)
            self.takeCards -= 1
            self.changePlayerCards("player"+self.player)
################ Game Functions
    def nearbyRoadList(self, road):
        returnList = []
        averageX = (self.RoadDictionary[road][0]+self.RoadDictionary[road][2])/2.0 
        averageY = (self.RoadDictionary[road][1]+self.RoadDictionary[road][3])/2.0
        for nearby in self.map.find_overlapping(averageX-self.sideLength/2.0, averageY-self.sideLength/2.0, averageX+self.sideLength/2.0, \
averageY+self.sideLength/2.0): # finds only perfectly adjacent settlements, roads, and hexes            
            if nearby in getattr(self, "player"+self.player+"RoadList"): # found adjacent road.
                if nearby != road:
                    returnList.append(nearby)
        return returnList
    def moveRobber(self, event):          
        self.playerList = []
        ListUnderMouse=self.map.find_overlapping(event.x-1,event.y-1,event.x+1,event.y+1)
        if self.robberMove:
            for itemUnderMouse in ListUnderMouse:
                if itemUnderMouse in self.hexCoordDict.keys() and self.hexCoordDict[itemUnderMouse] != self.robberCoords:
                    self.map.itemconfig(self.textFromCoordDict[(self.robberCoords[0], self.robberCoords[1])][0], text=self.robberPreviousText)                     
                    self.robberCoords = self.hexCoordDict[itemUnderMouse]                                        
                    self.robberPreviousText = self.textFromCoordDict[(self.robberCoords[0], self.robberCoords[1])][1]                    
                    self.map.itemconfig(self.textFromCoordDict[(self.robberCoords[0], self.robberCoords[1])][0], text="R")  
                    self.robberMove = False                           
                    self.robberLabel.config(bg=self.defaultBG)
                    for number in range(1,self.NumofPlayers+1): #List of each player's settlements                        
                        for settlement in getattr(self, "player"+str(number)+"SettleList"): # for each settlement of each player                                
                            if self.robberCoords in self.SettlementItemToHexCoordDict[settlement] and number not in self.playerList: # if settlement on that hex                                                              
                                self.playerList.append(number) # finds players on the hex
                        for city in getattr(self, "player"+str(number)+"CityList"): # for each city of each player                                
                            if self.robberCoords in self.SettlementItemToHexCoordDict[city] and number not in self.playerList: # if city on that hex, city has same item # as settle                                                              
                                self.playerList.append(number)  
                    self.halfCards() # robber steals half if over 7                     
    def halfCards(self):
        self.playersToLoseCards = {}
        if not self.knight: # knights don't get rid of cards 
            for player in range(1, self.NumofPlayers+1):
                if len(getattr(self, "player"+str(player)+"ResourceCardList")) > 7:
                    self.playersToLoseCards[player] = len(getattr(self, "player"+str(player)+"ResourceCardList"))                
        if len(self.playersToLoseCards.keys()) == 0: # in case no one needs to lose any cards, will always happen on knight.
            self.stealCard(self.playerList)
        else:
            tkm.showinfo("robber", "Player "+str(self.playersToLoseCards.keys()[0])+" needs to discard "+str(int(self.playersToLoseCards[self.playersToLoseCards.keys()[0]]//2))+" cards.")
            self.changePlayerCards("player"+str(self.playersToLoseCards.keys()[0])) # brings up first player with too many cards                
            self.losingCards = True
    def loseCard(self, variableName, player, card):
        if player in self.playersToLoseCards.keys():
            getattr(self, variableName).destroy() 
            getattr(self, "player"+str(player)+"ResourceCardList").remove(card)
            if len(getattr(self, "player"+str(player)+"ResourceCardList")) <= math.ceil(self.playersToLoseCards[player]/2.0): # rounds up
                self.playersToLoseCards.pop(player)
                if len(self.playersToLoseCards.keys()) > 0:
                    tkm.showinfo("robber", "Player "+str(self.playersToLoseCards.keys()[0])+" needs to discard "+str(int(self.playersToLoseCards[self.playersToLoseCards.keys()[0]]//2))+" cards.")
                    self.changePlayerCards("player"+str(self.playersToLoseCards.keys()[0])) # brings up first player with too many cards
                else:
                    self.stealCard(self.playerList)
    def stealCard(self, playerList):  
        self.losingCards = False
        self.knight = False
        for player in playerList:
            if str(player) != self.player and len(getattr(self, "player"+str(player)+"ResourceCardList")) > 0 : # no self-stealing or from players with none
                getattr(self, "player"+str(player)+"Button").config(bg="green")
                self.steal = True                            
        if self.steal:
            tkm.showinfo("robber", "Click any green player button to steal a card from them.")
    def calculateVP(self):
        for player in range(1, self.NumofPlayers+1):
            number = 0
            number += len(getattr(self, "player"+str(player)+"SettleList"))
            number += len(getattr(self, "player"+str(player)+"CityList"))
            for card in (getattr(self, "player"+str(player)+"DevCardList")):
                if card in self.VictoryPointCardList:
                    number += 1
            if self.largestArmy[0] == str(player) and self.largestArmy[1] >= 3:
                number += 2
            if self.longestRoad[0] == str(player) and self.longestRoad[1] >= 5:
                number += 2    
            setattr(self, "player"+str(player)+"VP", number)
            getattr(self, "player"+str(player)+"Button").config(text="Player "+str(player)+" VP: "+str(number))
    def checkForWin(self):
        self.calculateVP()
        if getattr(self, "player"+self.player+"VP") >= 10:# only current player can win
            tkm.showinfo("Game Ended", "Player "+self.player+" has won!") # pauses game with win message
            root.quit() # only quits after win is acknowledged 
        else: 
            return False
if __name__ == "__main__": # allows import without running
###### below is commented out for testing. Will allow flexible rules in board and players
    while True:
        players = raw_input("How many players: ")
        rings = raw_input("How many rings to the board: ")        
        try: 
            players = int(players)
            rings = int(rings)
        except:
            print "please input a valid number"
        if players < 2 or players > rings*3 or rings < 0 or rings > 10:
            print "Valid player values are between 2 and three times the number of rings. Valid ring numbers are between 1 and 10"
            continue
        break
        
    root = tk.Tk()
    GUI = CataanGUI(root, players, rings)
#     GUI = CataanGUI(root, 2, 2) # 2s are place holders
    root.title("Settlers of Cataan")
    root.mainloop()
