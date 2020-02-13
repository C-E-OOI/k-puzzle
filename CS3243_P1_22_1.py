import os
import sys

from copy import copy, deepcopy


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful

        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.parent = None
        self.children = []

    def __eq__(self, other):
        return self.init_state == other.init_state

    def __hash__(self):
        hashable = tuple(map(tuple, self.init_state))
        return hash(hashable)

    def setParent(self, puzzle):
        self.parent = puzzle

    def addChildren(self, puzzle):
        self.children.append(puzzle)

    def isGoal(self):
        return self.init_state == self.goal_state

    def findBlank(self):
        for row in range(0, len(self.init_state)):
            for col in range(0, len(self.init_state)):
                if (self.init_state[row][col] == 0):
                    return (row, col)

    def swapPositions(self, row, col, action):

        temp = self.init_state[row][col]
        new_arr = deepcopy(self.init_state)

        # Defines the possible movements and returns an array representing the movement
        if (action == "RIGHT"):
            new_arr[row][col] = new_arr[row][col + 1]
            new_arr[row][col + 1] = temp

        elif (action == "LEFT"):
            new_arr[row][col] = new_arr[row][col - 1]
            new_arr[row][col - 1] = temp

        elif (action == "UP"):
            new_arr[row][col] = new_arr[row - 1][col]
            new_arr[row - 1][col] = temp

        elif (action == "DOWN"):
            new_arr[row][col] = new_arr[row + 1][col]
            new_arr[row + 1][col] = temp

        return new_arr

    def moveRight(self):

        arr = self.findBlank()
        n = len(self.init_state)
        row = arr[0]
        col = arr[1]

        if (col < n - 1):
            new_array = self.swapPositions(row, col, "RIGHT")
            newPuzzle = Puzzle(new_array, self.goal_state)

            newPuzzle.setParent(self)
            self.actions.append("RIGHT")
            self.addChildren(newPuzzle)

            return newPuzzle

    def moveLeft(self):

        arr = self.findBlank()
        row = arr[0]
        col = arr[1]
        if (col > 0):

            new_array = self.swapPositions(row, col, "LEFT")
            newPuzzle = Puzzle(new_array, self.goal_state)

            newPuzzle.setParent(self)
            self.actions.append("LEFT")
            self.addChildren(newPuzzle)

            return newPuzzle

    def moveUp(self):

        arr = self.findBlank()
        row = arr[0]
        col = arr[1]
        if (row > 0):

            new_array = self.swapPositions(row, col, "UP")
            newPuzzle = Puzzle(new_array, self.goal_state)

            newPuzzle.setParent(self)
            self.actions.append("UP")
            self.addChildren(newPuzzle)

            return newPuzzle

    def moveDown(self):

        arr = self.findBlank()
        n = len(self.init_state)
        row = arr[0]
        col = arr[1]
        if (row < n - 1):

            new_array = self.swapPositions(row, col, "DOWN")
            newPuzzle = Puzzle(new_array, self.goal_state)

            newPuzzle.setParent(self)
            self.actions.append("DOWN")
            self.addChildren(newPuzzle)

            return newPuzzle

    def expandNodes(self):

        expandedNodes = []
        expandedNodes.append(self.moveUp())
        expandedNodes.append(self.moveDown())
        expandedNodes.append(self.moveLeft())
        expandedNodes.append(self.moveRight())

        expandedNodes = list(filter(None, expandedNodes))
        return expandedNodes

    def solve(self):
        # TODO
        # implement your search algorithm here

        action_list = []

        # Check if solvable
        if (self.isSolvable()):

            frontier = []
            visited = []

            frontier.append(self)

            # BFS search
            while(len(frontier) > 0):

                currentPuzzle = frontier.pop(0)

                if (currentPuzzle.isGoal()):
                    action_list = currentPuzzle.backtrack()
                    print(action_list)
                    break
                else:
                    if currentPuzzle not in visited:
                        visited.add(currentPuzzle)
                        frontier.extend(currentPuzzle.expandNodes())
        else:
            action_list.append("UNSOLVABLE")
            print(action_list)

    # you may add more functions if you think is useful
    # Backtrack algorithm to trace path from goal node to root node
    def backtrack(self):

        action_list = []

        while (self.parent is not None):
            actionIndex = self.parent.children.index(self)
            action = self.parent.actions[actionIndex]

            if (action == "UP"):
                action_list.append("DOWN")
            elif (action == "DOWN"):
                action_list.append("UP")
            elif (action == "LEFT"):
                action_list.append("RIGHT")
            elif (action == "RIGHT"):
                action_list.append("LEFT")
            self = self.parent

        action_list.reverse()
        return action_list

    # Helper method to calculate the permutation inversions in initial state
    def calculateInversions(self):

        # Flatten array for easier computation
        flat_arr = []
        for i in range(0, len(self.init_state)):
            for j in range(0, len(self.init_state)):
                flat_arr.append(self.init_state[i][j])

        inversion_count = 0

        # Loop through flat array and compare numbers in pairs
        for i in range(0, len(flat_arr)):
            for j in range(i + 1, len(flat_arr)):
                if (flat_arr[i] == 0 or flat_arr[j] == 0):
                    continue
                elif (flat_arr[i] > flat_arr[j]):
                    inversion_count += 1

        return inversion_count

    def findZeroPos(self):

        for row in range(0, len(self.init_state)):
            for col in range(0, len(self.init_state)):
                if (self.init_state[row][col] == 0):
                    return len(self.init_state) - row

    def isSolvable(self):

        n = len(self.init_state)
        inversion_number = self.calculateInversions()

        if (n % 2 != 0 & inversion_number == 0):
            return True
        else:
            zeroPos = self.findZeroPos()
            if (zeroPos % 2 == 0 and inversion_number % 2 != 0):
                return True
            elif (zeroPos % 2 != 0 and inversion_number % 2 == 0):
                return True
            else:
                return False


if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()

    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]

    i, j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number, base=10)
            if 0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1) % n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
