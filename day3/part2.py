class Point:
    # Constructor
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(" + str(self.x) + ", " + str(self.y) + ")"

    # Calculates the distance between two points
    def distanceTo(self, p):
        return abs(self.x - p.x) + abs(self.y - p.y)

    # Generates a point a given distance away from itself
    # given a direction string.
    def pointFrom(self, string):
        direction = string[0]
        distance = int(string[1:])

        if (direction == 'U'):
            return Point(self.x, self.y + distance)
        elif (direction == 'D'):
            return Point(self.x, self.y - distance)
        elif (direction == 'L'):
            return Point(self.x - distance, self.y)
        elif (direction == 'R'):
            return Point(self.x + distance, self.y)

class Vector:
    # Constructor
    def __init__(self, startPt, mag_direc, prev_steps):
        self.startPt = startPt # Start point
        self.endPt = startPt.pointFrom(mag_direc) # End point
        self.isHorizontal = True
        self.mag_direc = mag_direc
        self.steps = prev_steps + int(mag_direc[1:])
        direc = mag_direc[0]
        if (direc == 'U' or direc == 'D'):
            self.isHorizontal = False

    def __str__(self):
        return "Vector(" + str(self.startPt) + ", " + str(self.endPt) + ", " + self.mag_direc + ", " + str(self.isHorizontal) +", " + str(self.steps) + ") "

    # Calculates if perpendicular vectors are intersecting
    # NOTE: Does not account for if vectors are part of same line
    def ifIntersecting(self, other):
        if (self.isHorizontal == other.isHorizontal):
            return False
        else:
            if (self.isHorizontal):
                left_x = min(self.startPt.x, self.endPt.x)
                right_x = max(self.startPt.x, self.endPt.x)
                bottom_y = min(other.startPt.y, other.endPt.y)
                top_y = max(other.startPt.y, other.endPt.y)
                return (left_x <= other.startPt.x and right_x >= other.startPt.x and bottom_y <= self.startPt.y and top_y >= self.startPt.y)
            else:
                left_x = min(other.startPt.x, other.endPt.x)
                right_x = max(other.startPt.x, other.endPt.x)
                bottom_y = min(self.startPt.y, self.endPt.y)
                top_y = max(self.startPt.y, self.endPt.y)
                return (left_x <= self.startPt.x and right_x >= self.startPt.x and bottom_y <= other.startPt.y and top_y >= other.startPt.y)
    
    # Calculates the intersection point of two vectors
    def intersectionPoint(self, other):
        if (self.ifIntersecting(other)):
            print(str(self) + " and " + str(other) + "intersect!")
            if (self.isHorizontal): 
                return Point(other.startPt.x, self.startPt.y)
            else: 
                return Point(self.startPt.x, other.startPt.y)
        else: 
            return None

    # Gets the real cost to an intersection given current steps
    def realDistanceToIntersection(self, intersectionPoint):
        return abs(self.steps - self.endPt.distanceTo(intersectionPoint))

def getVectorArray(wires):
    vector_list = []
    current_steps = 0
    initial_point = Point(0,0)

    # Point directions
    for direction_string in wires.split(','):
        current_vector = Vector(initial_point, direction_string, current_steps)
        print(current_vector)
        vector_list.append(current_vector)
        current_steps = current_vector.steps
        initial_point = current_vector.endPt
    
    return vector_list

# Open and parse the file
f = open("input.txt", 'r')
wires_1 = f.readline()
wires_2 = f.readline()

vector_list_1 = getVectorArray(wires_1)
vector_list_2 = getVectorArray(wires_2)

origin = Point(0,0)
intersection_array = []
least_distance = 999999
least_steps = 999999

for vector1 in vector_list_1:
    for vector2 in vector_list_2:
        intersectionPoint = vector1.intersectionPoint(vector2)
        # Intersection has been found
        if (intersectionPoint != None):
            print("at" + str(intersectionPoint))
            current_distance = origin.distanceTo(intersectionPoint)
            if (current_distance > 0):
                least_distance = min(least_distance, current_distance)
                least_steps = min(least_steps, vector1.realDistanceToIntersection(intersectionPoint) + vector2.realDistanceToIntersection(intersectionPoint))

print("Least distance is " + str(least_distance))
print("Least steps is " + str(least_steps))
