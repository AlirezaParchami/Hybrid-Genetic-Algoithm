filename = ""
data = []
maxWeight = 0
optimum_value = 0

class Node:
    def __init__(self, string):
        self.string = string
        self.parent = None
        self.H = 0
        self.G = 0
        self.weight = 0


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
    return cand


def switch_char(index, child):
    if child[index] == "0":
        child = child[:index] + "1" + child[index+1:]
#    else:
#        print("Something is Wrong. The ", index, " in string ", child, " is ", child[index])
    return child


def children(parent):
    links = []
    for i in range(0, len(parent.string)):
        links.append(switch_char(i, parent.string))
    return links

def goal_t(current_node):
    sum_value = current_node.G
    sum_weight = current_node.weight
    if sum_value >= optimum_value and sum_weight <= maxWeight:
        return True
#    elif sum_weight > maxWeight:
#        return 2
#    elif sum_value < optimum_value or sum_value > optimum_value:
#        return 0
#    else:
#        print("Something is Wrong in Goal Test")
#        return 3
    return False


def estimate(node):
    current_value = 0
    while node.parent:
        current_value += node.G
        node = node.parent
    value = abs(current_value - optimum_value)
    value = value / maxWeight
    return value


def Astar(start):
    openset = set()
    closeset = set()

    current = start
    openset.add(current)

    while openset:
        current = max(openset, key=lambda o:o.G + o.H)

        if goal_t(current):
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]

        openset.remove(current)
        closeset.add(current)

        for child in children(current):
            closeset_string = []
            for i in closeset:
                closeset_string.append(i.string)
            if child in closeset_string:
                continue

            openset_string = []
            for i in openset:
                openset_string.append(i.string)
            if child not in openset_string:
                node = Node(child)
                node.G, node.weight = knapsnack(node.string)
                if node.weight <= maxWeight:
                    node.parent = current
                    node.H = estimate(current)
                    openset.add(node)
                else:
                    closeset.add(node)

    raise ValueError('No Path Found')


filename = input("Enter the name of your file: ")
if filename == "ks_20_878":
    #optimum_value = 136
    optimum_value = 1024
elif filename == "ks_100_997":
    optimum_value = 2397
elif filename == "ks_200_1008":
    optimum_value = 1634
else:
    print("Something is wrong in filename")
filename = "..//Dataset//" + filename + ".txt"
#indivSize = int(input("Enter the length of Individual: "))
read_file()
indivSize = data[0][0]

maxWeight = data[0][1]
init = "0" * indivSize
print("maxWeight: ", maxWeight)
print("init: ", init)
start_node = Node(init)
path = Astar(start_node)
print("Path: ")
for i in path:
    print("\nstring: ", i.string)
    print("G: ", i.G)
    print("weight: ", i.weight)