'''
V1
In this version, after the robots reach their destinations,
they destroy themselves, clearing the path.
Also, if no path is found for a robot, it is not deployed.
There are two types of robot: urgent and non-urgent. Urgent gets
priority. If there are conflicts between the same kind, conflicts
are managed on the first come first serve basis.
'''


import matplotlib.pyplot as plt


class Queue:

    def __init__(self, cap):
        self.queue = []
        self.capacity = cap

    def push(self, val):
        if len(self.queue) == self.capacity:
            raise OverflowError("Queue overflowed")
        self.queue.append(val)

    def pop(self):
        if not len(self.queue):
            raise ValueError("Queue is empty")
        return self.queue.pop(0)

    def peek(self):
        if not len(self.queue):
            raise ValueError("Queue is empty")
        return self.queue[0]

    def isEmpty(self):
        if not len(self.queue):
            return True
        return False


class Robot:

    def __init__(self, name):
        self.r0 = None
        self.r_end = None
        self.isUrgent = 0
        self.path = None
        self.foundPath = False
        self.path_length = None

    def assign(self, start, end, urgent):
        self.r_0 = start
        self.r_end = end
        self.isUrgent = urgent
        self.path = None
        self.foundPath = False
        self.path_length = None


class Warehouse:

    def __init__(self, length, breadth):
        self.m = length
        self.n = breadth
        self.robots = []
        self.robo_count = 0
        self.serial_nos = None
        self.states = []

        # m and n are the number of cells
        self.hori_walls = [[0 for j in range(self.n+1)] for i in range(self.m)]
        self.vert_walls = [[0 for j in range(self.n)] for i in range(self.m+1)]

        # putting boundary walls
        for i in [0, self.m]:
            for j in range(self.n-1):
                self.hori_walls[i][j] = 1
        for i in range(self.m-1):
            for j in [0, self.n]:
                self.vert_walls[i][j] = 1

    def add_hori_walls(self, y, start, end):
        if not (0<=y<=self.m and 0<=start<=self.n-1 and 0<=end<=self.n-1):
            raise ValueError("parameter is out of bounds")

        for j in range(start, end+1):
            self.hori_walls[y][j] = 1

    def add_hori_walls(self, x, start, end):
        if not (0<=x<=self.n and 0<=start<=self.m-1 and 0<=end<=self.m-1):
            raise ValueError("parameter is out of bounds")

        for i in range(start, end+1):
            self.hori_walls[i][x] = 1

    def add_robot(self, rob):
        for robo in self.robots:
            if robo.r0 == rob.r0 or robo.r_end == rob.r_end:
                raise ValueError("start or end coordinates conflict with existing robot")
        if not (0<=rob.r0[0]<self.n and 0<=rob.r0[1]<self.m):
                raise ValueError("start or end coordinates out of bounds")

        self.robo_count += 1
        if rob.isUrgent:
            self.robots.insert(0, rob)
        else:
            self.robots.append(rob)

    def del_robot(self, rob):
        find_ind = None
        for i in range(self.robo_count):
            if self.robots[i] == rob:
                find_index = i

        if find_index is None:
            raise ValueError("robot not in warehouse")

        self.robo_count -= 1
        self.robots.pop(find_index)

    def find_path(self, rob):
        self.serial_nos = [i for i in range(self.robo_count)]

        for robo in self.robots:
            que = Queue(self.m*self.n)
            i, j = robo.r0
            que.push((i, j))
            discovered = []
            parent = {(i, j): None}

            while(que):
                i, j = que.pop()
                discovered.append((i, j))
                if (i, j) == robo.r_end:
                    robo.foundPath = True
                    break

                if not (i-1, j) in discovered and not self.hori_walls[i][j]:
                    parent[(i-1, j)] = (i, j)
                    que.append((i-1, j))
                if not (i+1, j) in discovered and not self.hori_walls[i+1][j]:
                    parent[(i+1, j)] = (i, j)
                    que.append((i+1, j))
                if not (i, j-1) in discovered and not self.vert_walls[i][j]:
                    parent[(i, j-1)] = (i, j)
                    que.append((i, j-1))
                if not (i, j+1) in discovered and not self.vert_walls[i][j+1]:
                    parent[(i, j+1)] = (i, j)
                    que.append((i, j+1))

            if not robo.foundPath:
                return

            robo.path = []
            node = robo.r_end
            while node:
                robo.path.append(node)
                node = parent[node]
            robo.path = robo.path[::-1]
            robo.path_length = len(robo.path)

    def adjust_paths(self):
        t = 0
        while True:
            self.states.append([[0 for j in range(self.n)] for i in range(self.m)])
            while