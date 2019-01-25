import numpy as np

filename = ""
data = []

class Node:
    def __init__(self, string, actual_cost, estimated_cost, weight):
        self.string = string
        self.actual_cost = actual_cost
        self.estimated_cost = estimated_cost
        self.weight = weight
    next = []

def read_file():
    d = open(filename, "r")
    first_line = d.readline().split(" ")
    tmp = (int(first_line[0]), int(first_line[1]))
    data.append(tmp)
    for line in d:
        splited_data = line.split(" ")
        tmp = (int(splited_data[0]), int(splited_data[1]))
        data.append(tmp)


def knapsnack(x):
    # Read first line and detect the number and MaxWeight
    numbers = data[0][0]
    max_weight = data[0][1]
    values = []
    weights = []
    # Read each line and calculate the weight and value for x
    for line in range(1, len(data)):
        values.append(data[line][0])
        weights.append(data[line][1])
    sum_weight = 0
    sum_value = 0
    for i in range(0, len(x)):
        if x[i] == '1':
            sum_weight += weights[i]
            sum_value += values[i]
    #print("SUM Weight: ", sum_weight)
    #print("SUM Value: ", sum_value)
    if sum_weight > max_weight:
        sum_value = 0
    return sum_value, sum_weight


def heuristic(cand):
    cand.sort(key=lambda x: x.actual_cost + x.estimated_cost)
    cand.reverse()
#    for i in cand:
#        print("string: ", i.string)
#        print("actual cost: ", i.actual_cost)
#        print("estimated cost: ", i.estimated_cost)
#        print("weight: ", i.weight)
    return cand



def switch_char(index, child):
    if child[index] == "1":
        child = child[:index] + "0" + child[index+1:]
    elif child[index] == "0":
        child = child[:index] + "1" + child[index+1:]
    else:
        print("Something is Wrong. The ", index, " in string ", child, " is ", child[index])
    return child


def estimate():
    current_value = 0
    for i in path:
        current_value += i.actual_cost
    value = abs(current_value - optimum_value)
    value = value / maxWeight
    return value


def goal_t():
    global path
    sum_value = 0
    sum_weight = 0
    for i in path:
        sum_value += i.actual_cost
        sum_weight += i.weight
    if sum_value == optimum_value and sum_weight <= maxWeight:
        return 1
    elif sum_weight > maxWeight:
        return 2
    elif sum_value < optimum_value or sum_value > optimum_value:
        return 0
    else:
        print("Something is Wrong in Goal Test")
        return 3


def finds():
    neighbours = []
    candidates = []
    for i in path:
        for j in range(0, len(i.string)):
            tmp = switch_char(j, i.string)
            neighbours.append(tmp)
    # We should not add elements that are in path
    for i in path:
        if i.string in neighbours:
            neighbours.remove(i.string)
    # We should not add elements that we removed in previous searches
    for i in neighbours:
        if i in removed:
            neighbours.remove(i)
    for element in neighbours:
        cost, weight = knapsnack(element)
        candidates.append(Node(element, cost, estimate(), weight))
    print("PATH: ")
    for i in path:
        print(i.string)
    print("==========")

    print("CANDIDATES: ")
    for i in candidates:
        print(i.string)
    print("==============")
    return candidates



optimum_value = 0
filename = input("Enter the name of your file: ")
if filename == "ks_20_878":
    optimum_value = 1024
elif filename == "ks_100_997":
    optimum_value = 2397
elif filename == "ks_200_1008":
    optimum_value = 1634
else:
    print("Something is wrong in filename")
filename = "..//Dataset//" + filename + ".txt"
indivSize = int(input("Enter the length of Individual: "))
read_file()
persons = []
removed = []
maxWeight = data[0][1]
path = []  # A list of tuples that contain string, value and weight
init = ""
for i in range(0, indivSize):
    init += "0"
path.append(Node(init, 0, estimate(), 0))
print(path[0].estimated_cost)
while True:
    ans_t = goal_t()
    if ans_t == 1:  # Find answer
        break
    elif ans_t == 0:
        candidate = finds()
        candidate = heuristic(candidate)
        path.append(candidate[0])
    elif ans_t == 2:
        removed.append(path.pop(-1))
    else:
        print("Something is wrong in WHILE LOOP")
print("ANSWER: ", path)