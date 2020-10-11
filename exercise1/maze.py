#####################################################
# No code change allowed
#####################################################

import math
import random as rnd


class Stop:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def get_id(self):
        return str(self.x) + "-" + str(self.y)


class Road:
    def __init__(self, source: Stop, dest: Stop, weight: int = 1):
        self.source = source
        self.dest = dest
        self.weight = weight

    @property
    def get_source_id(self):
        return self.source.get_id

    @property
    def get_dest_id(self):
        return self.dest.get_id


class Maze:
    def __init__(self, width=5, height=5):
        self.stops = list()
        self.roads = list()
        self.start = None
        self.gold = None
        self.generate(width, height)

    @staticmethod
    def distance_stops(s1: Stop, s2: Stop):
        return math.sqrt(math.pow(s1.x - s2.x, 2) + math.pow(s1.y - s2.y, 2))

    def generate(self, width=5, height=5):

        # Creating stops in __maze
        for j in range(0, height):
            for i in range(0, width):
                stop = Stop(i, j)
                self.stops.append(stop)
        self.start = self.stops[0]
        self.gold = self.stops[rnd.randint(0, len(self.stops) - 1)]

        # generate real __maze
        unvisited_stops = self.stops.copy()

        myStack = []
        current = next((x for x in unvisited_stops if x.get_id == self.start.get_id), None)
        if current is None:
            return self
        
        unvisited_stops.remove(current)
        
        while len(unvisited_stops) > 0:
            # finding unvisited neighbors
            neighbors = [x for x in unvisited_stops if self.distance_stops(x, current) <= 1 ]
            if len(neighbors) == 0:
                if len(myStack) <= 0:
                    return self

                # --- Connecting death end
                neighborRoads = [x for x in self.roads if current.get_id == x.get_source_id]
                neighborRoads.extend([x for x in self.roads if current.get_id == x.get_dest_id])
                lastNeighbors = [x for x in self.stops if abs(self.distance_stops(current, x) - 1) < 0.0001]
                lastNeighbors = [x for x in lastNeighbors if x.get_id not in [s.get_source_id for s in neighborRoads]]
                lastNeighbors = [x for x in lastNeighbors if x.get_id not in [s.get_dest_id for s in neighborRoads]]

                lastCount = len(lastNeighbors)
                if lastCount > 0 and (lastCount > 2 or rnd.randint(1, 100) < 25):
                    randStopIdx = rnd.randint(0, len(lastNeighbors) - 1)
                    nextStop = lastNeighbors[randStopIdx]
                    self.roads.extend([Road(current, nextStop), Road(nextStop, current)])

                # --- end Connecting death end
                current = myStack.pop()
                continue

            randStopIdx = rnd.randint(0, len(neighbors)-1)
            nextStop = neighbors[randStopIdx]
            self.roads.extend([Road(current, nextStop), Road(nextStop, current)])
            myStack.append(current)
            current = nextStop
            unvisited_stops.remove(current)
