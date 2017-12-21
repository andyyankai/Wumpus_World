from Agent import Agent
import queue

class MyAI ( Agent ):

    def __init__ ( self ):

        self.wumpusKill = False
        self.wumpusLoc = None
        self.haveArrow = True
        self.curr = (1,1)
        self.face = 'R'
        self.dx = -1
        self.dy = -1
        self.action = list()
        self.oldaction = list()
        self.firstMove = 0

        #some maps
        self.breezeMap = [['Nah' for x in range(10)] for y in range(10)]
        self.pitMap = [['Nah' for x in range(10)] for y in range(10)]
        self.stenchMap = [[False for x in range(10)] for y in range(10)]
        self.safeMap = [[False for j in range(10)] for i in range(10)]
        self.stenchLoc = []
        self.safeLoc = []
        self.oldLoc = None
        self.boundary = []
        self.exploredSquares = [(1,1)]
        self.pitsFound = []
        self.shoot = False

    def getAction( self, stench, breeze, glitter, bump, scream ):

        (curX, curY) = self.curr 
        self.safeMap[curX][curY] = True
        if glitter:
            self.gogo((1,1))
            self.action.append(Agent.Action.CLIMB)
            return Agent.Action.GRAB

        if len(self.action) != 0:
            if bump:
                self.action.clear()
                self.nextMove()
            return self.action.pop(0)

        if stench and not breeze and self.curr == (1,1) and self.haveArrow and self.firstMove == 0:
            self.firstMove = 1
            self.stenchLoc.append((1,1))
            self.haveArrow = False
            self.shoot = True
            return Agent.Action.SHOOT


        if self.shoot == True:
            
            self.shoot = False
            if scream:
                self.wumpusKill = True
            elif self.firstMove == 1:
                self.firstMove = 2
                self.wumpusLoc = (1,2)
            else:
                if self.face == 'U':
                    self.safeMap[curX][curY+1] = True
                if self.face == 'D':
                    self.safeMap[curX][curY-1] = True
                if self.face == 'L':
                    self.safeMap[curX-1][curY] = True
                if self.face == 'R':
                    self.safeMap[curX+1][curY] = True
                self.extendBound()
                self.nextMove()
                
            self.extendBound()
            self.nextMove()
            return self.action.pop(0)
        if bump:
            self.curr = self.oldLoc
            if self.face == 'R':
                self.dx = self.curr[0]
                for i in range(len(self.safeMap)):
                    self.safeMap[self.dx+1][i] = False
                i = 0
                while i != len(self.boundary):
                    x, _ = self.boundary[i]
                    if x > self.dx:
                        self.boundary.pop(i)
                    else:
                        i = i + 1
            elif self.face == 'U':
                self.atTopEdge = True
                self.dy = self.curr[1]

                for j in range(len(self.safeMap[0])):
                    self.safeMap[j][self.dy+1] = False
                i = 0
                while i != len(self.boundary):
                    _, y = self.boundary[i]
                    if y > self.dy:
                        self.boundary.pop(i)
                    else:
                        i = i + 1
            self.nextMove()
            return self.action.pop(0)
        else:
            dangers = []
            if stench and not self.wumpusKill:
                self.stenchMap[curX-1][curY-1] = True
                if self.curr not in self.stenchLoc:
                    self.stenchLoc.append(self.curr)
                dangers.append('stench')
            if breeze:
                dangers.append('breeze')
                self.breezeMap[curX][curY] = True
            else:
                self.breezeMap[curX][curY] = False
            if len(dangers) != 0:
                self.dangerMove(dangers)
                return self.action.pop(0)
            self.oldaction.append(self.curr)
            self.extendBound()
            self.nextMove()
            return self.action.pop(0)
        return Agent.Action.CLIMB

    #==========helper functions==============

    def dangerMove(self, dangers):
        curX, curY = self.curr
        noDanger = []
        if 'breeze' in dangers and 'stench' in dangers:
            noWumpusNear = self.getWumpusFree(self.curr)
            if len(noWumpusNear) != 0:
                noPitNeighbors = self.getPitFree(self.curr)
                if len(noPitNeighbors) != 0:
                    noDanger.extend(list(set(noPitNeighbors).intersection(set(noWumpusNear))))

        elif 'breeze' in dangers:
            noPitNeighbors = self.getPitFree(self.curr)
            noDanger.extend(noPitNeighbors)

        elif 'stench' in dangers and not self.wumpusKill:
            noWumpusNear = self.getWumpusFree(self.curr)
            noDanger.extend(noWumpusNear)
        self.extendBound(tabolist = list(set(self.getNear(self.curr, tabolist = noDanger))))
        self.nextMove()

    def getWumpusFree(self, s):
        if self.wumpusLoc == None:
            self.wumpusLoc = self.findWumpus()
        rs = []
        if self.wumpusLoc != None:
            allNear = self.getNear(s)
            for n in allNear:
                if n != self.wumpusLoc:
                    rs.append(n)
        return rs

    def getPitFree(self, s):
        self.updatePitInformation(s)
        ret = []
        allNear = self.getNear(s)
        for n in allNear:
            x, y = n
            if self.pitMap[x][y] == False:
                ret.append(n)
        return ret

    def updatePitInformation(self, s):
        allNear = self.getNear(s)
        safeNear = self.safeNear(s)
        unsafeNear = list(set(allNear) - set(safeNear))
        for neighbor in unsafeNear:
            x, y = neighbor
            if self.isPit(neighbor):
                self.pitMap[x][y] = True
                self.safeMap[x][y] = False
                self.pitsFound.append(neighbor)
            elif self.isPit(neighbor) == False:
                self.pitMap[x][y] = False
                self.safeMap[x][y] = True

    def getNoBreezeNeighbors(self, s):
        allNear = self.getNear(s)
        ret = []

        for n in allNear:
            if self.breezeMap[n[0]][n[1]] == False:
                ret.append(n)
        return ret
 

    def isPit(self, s):
        x, y = s
        allNear = self.getNear(s)
        for (x,y) in allNear:
            if self.breezeMap[x][y] == False:
                return False
        return True

    def nextMove(self):
        nextstep = self.popFrontier()
        if not nextstep:
            self.gogo((1,1))
            self.action.append(Agent.Action.CLIMB)
        else:
            self.gogo(nextstep)

    def gogo(self, dest):
        if self.curr == dest:
            return
        (curX, curY) = self.curr
        (destX, destY) = dest
        if (abs(destX - curX) + abs(destY - curY)) == 1:
            if dest != self.curr:
                x, y = self.curr
                self.faceSquare(dest)
                self.action.append(Agent.Action.FORWARD)
                self.oldLoc = self.curr
                self.curr = dest
        else:
            path = self.goTo(dest)
            for p in path[1:]:
                if p != self.curr:
                    x, y = self.curr
                    self.faceSquare(p)
                    self.action.append(Agent.Action.FORWARD)
                    self.oldLoc = self.curr
                    self.curr = p

    def goTo(self, dest):
        Q = [self.curr]
        parents = {self.curr : None}
        u = None
        pathFound = False
        while len(Q) != 0 and not pathFound:
            u = Q.pop(0)
            ne = self.safeNear(u)
            for v in ne:
                if v not in parents:
                    parents[v] = u
                    Q.append(v)
                if v == dest:
                    pathFound = True
                    break
        if not pathFound:
            return None
        else:
            w = dest
            path = []
            while w != self.curr:
                path.insert(0, w)
                w = parents[w]
            path.insert(0, self.curr)
            return path

    def extendBound(self, tabolist = []):
        (x, y) = self.curr
        up = (x, y + 1)
        down = (x, y - 1)
        left = (x - 1, y)
        right = (x + 1, y)
        if self.wumpusLoc in self.boundary:
            tp = self.boundary.index(self.wumpusLoc)
            del self.boundary[tp]
        if x != self.dx:
            if right not in tabolist:
                if right not in self.exploredSquares and right not in self.boundary:
                    self.boundary.append(right)
                self.safeMap[x+1][y] = True
        if x > 1:
            if left not in tabolist:
                if left not in self.exploredSquares and left not in self.boundary:
                    self.boundary.append(left)
                self.safeMap[x-1][y] = True
        if y != self.dy:
            if up not in tabolist:
                if up not in self.exploredSquares and up not in self.boundary:
                    self.boundary.append(up)
                self.safeMap[x][y+1] = True
        if y > 1: 
            if down not in tabolist:
                if down not in self.exploredSquares and down not in self.boundary:
                    self.boundary.append(down)
                self.safeMap[x][y-1] = True

    def safeNear(self, s):
        if self.wumpusLoc:
            (wx,wy) = self.wumpusLoc
        else:
            wx = -1
            wy = -1
        x, y = s
        S = []
        up = (x, y + 1)
        down = (x, y - 1)
        left = (x - 1, y)
        right = (x + 1, y)
        if self.safeMap[x][y+1] and (x == wx and y+1 == wy) == False:
            S.append(up)
        if self.safeMap[x][y-1] and (x == wx and y-1 == wy) == False:
            S.append(down)
        if self.safeMap[x-1][y] and (x-1 == wx and y == wy) == False:
            S.append(left)
        if self.safeMap[x+1][y] and (x+1 == wx and y == wy) == False:
            S.append(right)
        return S

    def getNear(self, s, tabolist = []):
        x, y = s
        return list(set([(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]) - set(tabolist))

    def killWumpus(self):
        self.faceSquare(self.wumpusLoc)
        self.action.append(Agent.Action.SHOOT)
        self.haveArrow = False
    
    def faceSquare(self, dest):
        (curX, curY) = self.curr
        (destX, destY) = dest

        (dx, dy) = (destX - curX, destY - curY)      
        if dx != 0:
            if dx < 0 and self.face != 'L':
                if self.face == 'R':
                    self.action.append(Agent.Action.TURN_RIGHT)
                    self.action.append(Agent.Action.TURN_RIGHT)
                elif self.face == 'U':
                    self.action.append(Agent.Action.TURN_LEFT)
                elif self.face == 'D':
                    self.action.append(Agent.Action.TURN_RIGHT)
                self.face = 'L'
            elif dx > 0 and self.face != 'R':
                if self.face == 'L':
                    self.action.append(Agent.Action.TURN_RIGHT)
                    self.action.append(Agent.Action.TURN_RIGHT)
                elif self.face == 'U':
                    self.action.append(Agent.Action.TURN_RIGHT)
                elif self.face =='D':
                    self.action.append(Agent.Action.TURN_LEFT)
                self.face = 'R'
        elif dy != 0:
            if dy > 0 and self.face != 'U':
                if self.face == 'D':
                    self.action.append(Agent.Action.TURN_RIGHT)
                    self.action.append(Agent.Action.TURN_RIGHT)
                elif self.face == 'L':
                    self.action.append(Agent.Action.TURN_RIGHT)
                elif self.face == 'R':
                    self.action.append(Agent.Action.TURN_LEFT)
                self.face = 'U'
            if dy < 0 and self.face != 'D':
                if self.face == 'U':
                    self.action.append(Agent.Action.TURN_RIGHT)
                    self.action.append(Agent.Action.TURN_RIGHT)
                elif self.face == 'L':
                    self.action.append(Agent.Action.TURN_LEFT)
                elif self.face =='R':
                    self.action.append(Agent.Action.TURN_RIGHT)
                self.face = 'D'

    def findWumpus(self):
        x, y = self.curr
        loc = None
        upRight = (x + 1, y + 1)
        downRight = (x + 1, y - 1)
        upLeft = (x - 1, y + 1)
        downLeft = (x - 1, y - 1)
        up = (x, y + 1)
        down = (x, y - 1)
        left = (x - 1, y)
        right = (x + 1, y)
        if (x + 2, y) in self.stenchLoc:
            loc = right
        elif (x - 2, y) in self.stenchLoc:
            loc = left
        elif (x, y + 2) in self.stenchLoc:
            loc = up
        elif (x, y - 2) in self.stenchLoc:
            loc = down
        else:
            if upRight in self.stenchLoc:
                if up in self.exploredSquares:
                    loc = right
                elif right in self.exploredSquares:
                    loc = up
            elif downRight in self.stenchLoc:
                if down in self.exploredSquares:
                    loc = right
                elif right in self.exploredSquares:
                    loc = down
            elif upLeft in self.stenchLoc:
                if up in self.exploredSquares:
                    loc = left
                elif left in self.exploredSquares:
                    loc = up
            elif downLeft in self.stenchLoc:
                if down in self.stenchLoc:
                    loc = left
                elif left in self.stenchLoc:
                    loc = down
        return loc

    def popFrontier(self):
        if len(self.boundary) == 0:
            return None
        nextSq = self.minNode()
        if nextSq not in self.exploredSquares:
            self.exploredSquares.append(nextSq)
        return nextSq

    def minNode(self):
        minCost = self.cost(self.boundary[0])
        minNode = 0
        i = 1
        while i < len(self.boundary):
            t = self.cost(self.boundary[i])
            if t < minCost:
                minCost = t
                minNode = i
            i = i + 1
        return self.boundary.pop(minNode)

    def cost(self, s):
        dx, dy = (s[0] - self.curr[0], s[1] - self.curr[1])
        rs = 0
        if dx < 0:
            if self.face == 'R':
                rs += 2
            elif self.face == 'U' or self.face == 'D':
                rs += 1
        if dx > 0:
            if self.face == 'L':
                rs += 2
            elif self.face == 'U' or self.face == 'D':
                rs += 1 
        if dy < 0:
            if self.face == 'U':
                rs += 2
            elif self.face == 'L' or self.face == 'R':
                rs += 1
        if dy > 0:
            if self.face == 'D':
                rs += 2
            elif self.face == 'L' or self.face == 'R':
                rs += 1
        rs += abs(self.curr[1] - s[1]) + abs(self.curr[0] - s[0])
        return rs

