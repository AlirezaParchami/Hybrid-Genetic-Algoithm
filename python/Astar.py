filename = ""
data = []

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
    global finfuncstart
    finfuncstart += 1
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
    return sum_value


def goal_test():
    sum = 0
    for i in path:
        sum += i[1]
    if sum < optimum_value or sum > optimum_value:
        return False
    elif sum == optimum_value:
        return True

def heuristic():
    heuristic_values = []
    for x in persons:
        tmp = (x, abs(knapsnack(x) - optimum_value) / maxWeight)
        heuristic_values.append(tmp)
    heuristic_values.sort(key=lambda tup: tup[1])



filename = input("Enter the name of your file: ")
filename = "..//Dataset//" + filename + ".txt"
read_file()
persons = []
optimum_value = 0
if filename == "ks_20_878":
    optimum_value = 1024
elif filename == "ks_100_997":
    optimum_value = 2397
elif filename == "ks_200_1008":
    optimum_value = 1634
else:
    print("Something is wrong in filename")
maxWeight = data[0][1]
path = []
while goal_test(path):
    heuristic()
