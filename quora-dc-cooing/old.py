import datetime
import sys

'''
Optimizations - detect all cycles.
- for each cycle, all paths within the cycles that don't contain all rooms can be ignored immediately.
'''

def getStartingAndMap(width, height, values):
    count = 0
    map = get2dArray(width, height)
    
    startingPoint = (-1, -1)
    for x in xrange(len(values)) :
        column = x % width
        row = count
        map[column][row] = values[x]
        
        if values[x] == 2 :
            startingPoint = (column, row)
        
        if (x + 1) % width == 0 :
            count += 1
            
    return (startingPoint, map)
        
def get2dArray(width, height):
    array = []
    for x in xrange(width) :
        array.append([])
        for y in xrange(height) :
            array[x].append(0)
    return array


'''
An optimization.  If we found a cycle in the piping and
there exists rooms within the cycle and rooms outside the
cycle ... we can stop and save further processing
'''
def isBadPiping(numRooms, adjacentRooms, visitedRooms, visitedRoomsStack, roomMap):
    for aRoom in adjacentRooms :
        roomsInsideCycle = 0
#        visitedRoomsSinceMap = get2dArray(len(visitedRooms), len(visitedRooms[0]))
        
        if visitedRooms[aRoom[0]][aRoom[1]] :
            #cycle found
            
            #return all rooms that are contained in the cycle found
            pos = 0
            for room in visitedRoomsStack :
                if aRoom[0] == room[0] and aRoom[1]  == room[1] :
                    break
                pos += 1
    
            #now we have the visited rooms that created the cycle
            #see if there's are room inside the cycle and a room outside the cycle
            minX = minY = sys.maxint
            maxX = maxY = -1
            for x in xrange(pos, len(visitedRoomsStack)) :
                room = visitedRoomsStack[x]
#                visitedRoomsSinceMap[room[0]][room[1]] = 1
                if room[0] < minX :
                    minX = room[0]
                if room[0] > maxX :
                    maxX = room[0]
                if room[1] < minY :
                    minY = room[1]
                if room[1] > maxY :
                    maxY = room[1]
                    
            if maxX - minX > 1 and maxY - minY > 1 :
                for x in range(minX, maxX) :
                    for y in range(minY, maxY) :
                        if not visitedRooms[x][y] and roomMap[x][y] in (0,3):
                            found1 = found2 = False
                            for xn1 in range(minX, x) :
                                if visitedRooms[xn1][y] :
                                    for xn2 in range(x+1, maxX) :
                                        if visitedRooms[xn2][y] :
                                            found1 = True
                                            break
                                if found1 :
                                    break
                                
                            for yn1 in range(minY, y) :
                                if visitedRooms[x][yn1] :
                                    for yn2 in range(y+1, maxY) :
                                        if visitedRooms[x][yn2] :
                                            found2 = True
                                            break
                                if found2 :
                                    break
                            if found1 and found2 :
                                roomsInsideCycle += 1
                        
                        
        if roomsInsideCycle :
            return roomsInsideCycle > 0 and len(visitedRoomsStack) + roomsInsideCycle < numRooms

    return False


    



def dcCooling(width, height, values):
    
    startingPoint, roomMap = getStartingAndMap(width, height, values)
    numRoomsToVisit = len(values) - (reduce(lambda x,y: x+y, values) - 5)
    
    if startingPoint[0] < 0 or startingPoint[1] < 0 :
        raise Exception("Non starting point")
    
    def getAdjacentPoints(x,y):
        adjacents = []
        if x - 1 >= 0 :
            adjacents.append((x-1, y))
        if x + 1 < width :
            adjacents.append((x+1, y))
        if y - 1 >= 0 :
            adjacents.append((x, y-1))
        if y + 1 < height :
            adjacents.append((x, y+1))
        return adjacents
    
    memoizedCache = get2dArray(width, height)
    visitedRooms = get2dArray(width, height)
    visitedRoomsStack = []
    
    def getMemoizedCache(x, y):
        hash = "".join(visitedRoomCodes)
        value = None
        if memoizedCache[x][y] :
            value = memoizedCache[x][y].get(hash) 
            
        return value
#
    def putMemoizedCache(x, y, value):
        hash = "".join(visitedRoomCodes)
        if not memoizedCache[x][y] :
            memoizedCache[x][y] = {}
        memoizedCache[x][y][hash] = value
        
    
    def getNumVisitedRooms():
        count = 0
        for x in xrange(len(visitedRooms)) :
            for y in xrange(len(visitedRooms[x])) :
                if visitedRooms[x][y] == 1 :
                    count += 1
        return count
 
    def getNumPaths(x,y):
        numPaths = 0
        visitedRooms[x][y] = 1
        visitedRoomsStack.append((x,y))
        roomValue = roomMap[x][y]
        
        if roomValue == 3 and getNumVisitedRooms() == numRoomsToVisit :
            #by definition, a path exists only if we hit 3 and visited all rooms
            numPaths = 1
#            print visitedRoomsStack
        elif roomValue in (0, 2) :
            #we only want to further traverse if were at the start or in a room
            adjacents = getAdjacentPoints(x,y)
            
            if not isBadPiping(numRoomsToVisit, adjacents, visitedRooms, visitedRoomsStack, roomMap) :

                for adjacent in adjacents :
                    if not visitedRooms[adjacent[0]][adjacent[1]] :
                        #can't cross the same room twice
                        
                        paths = getNumPaths(adjacent[0], adjacent[1])
                        numPaths += paths
   
                    
        visitedRooms[x][y] = 0
        visitedRoomsStack.pop()
        return numPaths
    
    return getNumPaths(*startingPoint)


if __name__ == "__main__" :
    
    #expected 0
    print dcCooling(1,1,(2,))

    #expected 1 
    print dcCooling(2,1, (2,3))
    
    #expected 1
    print dcCooling(2,2, (2,3,
                          0,0))
    
    #expected 2 
    print dcCooling(3,3, (2,0,0,
                          0,0,0,
                          3,0,0))

    #expected 399
    start = datetime.datetime.now()
    
    print dcCooling(7, 5, (2, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0,
                           3, 0, 0, 0, 0, 1, 1))

    end = datetime.datetime.now()
    print (end-start).seconds