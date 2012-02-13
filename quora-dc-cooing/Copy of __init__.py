import datetime 

'''
populates a 2d array to return the room at x,y
'''
def getStartingRoomAndMap(width, height, values):
    map = {}
    startingRoom = (-1, -1)
    count = 0
    height = 0
    for value in values :
        x = count % width
        y = height
        map["%i-%i" % (x, y)] = value
        if value == 2 :
            startingRoom = (x,y)
        count += 1
        if count % width == 0 :
            height +=1 
       
    return (startingRoom, map)

def dcCooling(width, height, values) :
    numPaths = [0]
    usageCount = 0
    startingRoom, roomMap = getStartingRoomAndMap(width, height, values)
    sx,sy = startingRoom
    roomMap = (roomMap)
    if sx < 0 or sy < 0 :
        raise Error("Could not find a starting room!")
    
    usageMap = {}
    numRooms = len(values) - ( reduce(lambda x,y : x+y, values) - 3 )
    
    def getAdjacentRooms(x,y):
        adjacentRooms = []
        if x > 0 :
            adjacentRooms.append((x-1, y))
        if x < width-1 :
            adjacentRooms.append((x+1, y))
        if y > 0 :
            adjacentRooms.append((x, y-1))
        if y < height-1 :
            adjacentRooms.append((x, y+1))
#        print "%s~%s" % ((x,y), adjacentRooms)
        return adjacentRooms
                
    runningStack = []
    def processAdjacentRooms(x,y):
        nextRooms = []
        adjacentRooms = getAdjacentRooms(x,y)
        done = False
        if len(usageMap) == numRooms :
            for x,y in adjacentRooms :
                if roomMap.get("%i-%i" % (x,y)) == 3 :
                    done = True
        else :
            for x,y in adjacentRooms :
                key = "%i-%i" % (x,y)
                if roomMap.get("%i-%i" % (x,y)) == 0 and not usageMap.get(key) :
                    nextRooms.append((x,y))
                    
        if done :
            numPaths[0] += 1
            print str(runningStack)
        elif nextRooms :
            for x,y in nextRooms :
                runningStack.append((x,y))
                usageMap["%i-%i" % (x,y)] = 1
                processAdjacentRooms(x,y)
                del usageMap["%i-%i" % (x,y)]
                runningStack.pop()
                
                
    processAdjacentRooms(sx, sy)
    return numPaths[0]


if __name__ == "__main__" :
    
    #expected 0
    print dcCooling(2,2, (2, 0, 
                          0, 3))
    
    #expected 1
    print dcCooling(2, 3, (2, 0, 
                           0, 0, 
                           0, 3))

    #expected 2 
    print dcCooling(4, 3, (2, 0, 0, 0, 
                           0, 0, 0, 0, 
                           0, 0, 3, 1))
 
    print dcCooling(7, 4, (2, 0, 0, 0, 0, 0, 0, 
                           0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0,
                           3, 0, 0, 0, 0, 1, 1))
 
#    print dcCooling(7, 8, (2, 0, 0, 0, 0, 0, 0, 
#                           0, 0, 0, 0, 0, 0, 0, 
#                           0, 0, 0, 0, 0, 0, 0, 
#                           0, 0, 0, 0, 0, 0, 0, 
#                           0, 0, 0, 0, 0, 0, 0, 
#                           0, 0, 0, 0, 0, 0, 0, 
#                           0, 0, 0, 0, 0, 0, 0, 
#                           3, 0, 0, 0, 0, 1, 1))
    