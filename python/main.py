import string
import random
import math
from random import randint

filename = ""
data = []

def individual_generation(indiv_size):
    """create stochastic individuals"""
    s = ""
    binary_list = ['0', '1']
    for num in range(indiv_size):
        s += random.choice(binary_list)
    return s


def population_generation(pop_size, indiv_size):
    """Generate Population Set"""
    myList = []
    for num in range(pop_size):
        myList.append(individual_generation(indiv_size))
    return myList


def reproduction(cross_prob, mut_prob, persons, person_fitness, parentPercent, offspringPercent):
    # Select parents, crossover, mutation
    children = []
    SP = parent_selection(persons, person_fitness, parentPercent, offspringPercent)  # Selected Parents
    #print("selected parents: ", SP)
    for x in SP:
        x[0], x[1] = crossover(cross_prob, indivSize, x[0], x[1])
        x[0] = mutation(mut_prob, indivSize, x[0])
        x[1] = mutation(mut_prob, indivSize, x[1])
        children.append(x[0])
        children.append(x[1])
    return children


def crossover(cross_prob, length, first, second):
    if random.uniform(0, 1) < cross_prob:
    #    print("--------Crossover of: ", first, "  ", second)
        crossover_points = random.sample(range(1, length), 2)
        crossover_points.sort()
        tmp = second
        second = second[:crossover_points[0]] + first[crossover_points[0]:crossover_points[1]] + second[crossover_points[1]:]
        first = first[:crossover_points[0]] + tmp[crossover_points[0]:crossover_points[1]] + first[crossover_points[1]:]
    #    print("%%%Crossover Done: ", first, "  ", second)
    return first, second


def mutation(mut_prob, length, string):
    for i in range(0, len(string)):
        if random.uniform(0, 1) < mut_prob:
    #        print("------------ Mutation of ", string)
            string = switch_char(i, string)
    #        print("%%%Mutation Done: ", string, "\n")
    return string


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


def parent_selection(persons, person_fitness, parentPercent, offspringPercent):
    # List of Fitness percents
    fitness_percent = []
    fitness_sum = 0
    #print("Person Fitness in parent_selection func: ", person_fitness)
    for x in person_fitness:
        fitness_sum += x
    #print("Fitness SUM: ", fitness_sum)
    tmp = 0
    for x in person_fitness:
        tmp += (x/fitness_sum)
        fitness_percent.append(tmp)
    # Select Candidate parents
    candidate_parents = []
    for i in range(0, int(math.floor(parentPercent*len(persons)))):
        prob = random.uniform(0, 1)
        for j in range(0, len(fitness_percent)):
            if prob < fitness_percent[j]:
                candidate_parents.append(persons[j])
                break
    # Select Pairs
    selected_parents = []
    for i in range(0, int(math.floor(offspringPercent*len(persons)/2))):
        index1 = randint(0, len(candidate_parents)-1)
        index2 = randint(0, len(candidate_parents)-1)
        pair = []
        pair.append(candidate_parents[index1])
        pair.append(candidate_parents[index2])
        selected_parents.append(pair)
    return selected_parents


def switch_char(index, child):
    if child[index] == "1":
        child = child[:index] + "0" + child[index+1:]
    elif child[index] == "0":
        child = child[:index] + "1" + child[index+1:]
    else:
        print("Something is Wrong. The ", index, " in string ", child, " is ", child[index])
    return child


def neighbor_values(mychild):
    values = {}  # A dictionary that its key is children and its value is fitness
    for i in range(0, len(mychild)):
        tmp = switch_char(i, mychild)
        values[tmp] = knapsnack(tmp)
    sorted_values = sorted(values.items(), key=lambda kv: kv[1])
    sorted_values.reverse()
    return sorted_values


def hill_climbing(mychild, improve, sideway, tabu):

    #print("------------Local search: ", mychild)
    if improve > MaxImprove:
        return mychild
    child_value = knapsnack(mychild)
    sorted_values = neighbor_values(mychild)
    improved_child = ""
    if sorted_values[0][1] > child_value:
    #    print("improve")
        improve += 1
        improved_child = hill_climbing(sorted_values[0][0], improve, sideway, tabu)
    elif sorted_values[0][1] < child_value:
    #    print("return")
        improved_child = mychild
    else:
    #    print("sideway")
        if sideway > MaxSideWay:
            improved_child = mychild
        else:
            for x in sorted_values:
                if x[0] not in tabu and x[1] == child_value:
                    tabu.append(child)
                    sideway += 1
                    improved_child = hill_climbing(x[0], improve, sideway, tabu)
    #print("%%% Hill climbing Done: ", improved_child)
    return improved_child


def replacement(persons_list):
    tmp = []
    for person in persons_list:
        x = (person, knapsnack(person))
        tmp.append(x)
    tmp.sort(key= lambda tup: tup[1])
    tmp.reverse()
    selected = []
    for i in range(0, popSize):
        selected.append(tmp[i][0])
    ave = 0
    for i in range(0, popSize):
        ave += tmp[i][1]
    ave = ave / popSize
    return selected, ave

def read_file():
    d = open(filename, "r")
    first_line = d.readline().split(" ")
    tmp = (int(first_line[0]), int(first_line[1]))
    data.append(tmp)
    for line in d:
        splited_data = line.split(" ")
        tmp = (int(splited_data[0]), int(splited_data[1]))
        data.append(tmp)




"""
for i in range(0, 3):
    print(i)
# 0 1 2    
a = "0123456789"
print(a[:0])
# 
print(a[:1])
# 0
print(a[:4])
# 0 1 2 3
print(a[1:4])
# 1 2 3
print(a[1:])
# 1 2 3 4 5 6 7 8 9

"""
mode = int(input("Enter Mode: 1-Genetic 2-A* : "))
if mode == 1:
    finfuncstart = 0
    indivSize = int(input("Enter the length of Individual: "))
    popSize = int(input("Enter the number of population: "))
    persons = population_generation(popSize, indivSize)
    print("persons= ", persons)

    filename = input("Enter the name of your file: ")
    filename = "..//Dataset//" + filename + ".txt"
    parentPercent = float(input("Enter parent percent: "))
    offspringPercent = float(input("Enter offspring percent: "))
    maxGen = int(input("Enter max generation number: "))
    crossoverProb = float(input("Enter Crossover Probability: "))
    mutaionProb = float(input("Enter Mutation Probability: "))
    TabuSize = int(input("Enter Tabu Size: "))
    MaxSideWay = int(input("Enter Max Sizeway: "))
    MaxImprove = int(input("Enter Max Improve: "))
    read_file()
    #print("DATA: ", data)
    while maxGen > 0:
        #print("=========================================== maxGen: ", maxGen)
        person_fitness = []
        #print("Persons: ", persons)
        for person in persons:
            person_fitness.append(knapsnack(person))
        #print("Person Fitness: ", person_fitness)
        children = reproduction(crossoverProb, mutaionProb, persons, person_fitness, parentPercent, offspringPercent)
        #print("Children: ", children)
        improved_children = []
        for child in children:
            tabu = []
            improved_children.append(hill_climbing(child, 0, 0, tabu))
        persons = persons + improved_children
        persons, average = replacement(persons)
        maxGen -= 1

    print("BEST Person: ", persons[0])
    print("Best Person Fitness: ", knapsnack(persons[0]))
    print("Fitness average: ", average)

elif mode ==2 :
    filename = input("Enter the name of your file: ")
    filename = "..//Dataset//" + filename + ".txt"
    read_file()
    persons=[]
