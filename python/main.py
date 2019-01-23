import string
import random
import math
from random import randint

filename = ""


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


def reproduction(indiv_size, cross_prob, mut_prob, persons, person_fitness, parentPercent, offspringPercent):
    # Select parents, crossover, mutation
    children = []
    SP = parent_selection(persons, person_fitness, parentPercent, offspringPercent)  # Selected Parents
    print("SP: ", SP)
    for x in SP:
        x[0], x[1] = crossover(cross_prob, indiv_size, x[0], x[1])
        x[0] = mutation(mut_prob, indivSize, x[0])
        x[1] = mutation(mut_prob, indivSize, x[1])
        children.append(x[0])
        children.append(x[1])
    return children


def crossover(cross_prob, length, first, second):
    if random.uniform(0, 1) < cross_prob:
        crossover_points = random.sample(range(1, length), 2)
        crossover_points.sort()
        tmp = second
        second = second[:crossover_points[0]] + first[crossover_points[0]:crossover_points[1]] + second[crossover_points[1]:]
        first = first[:crossover_points[0]] + tmp[crossover_points[0]:crossover_points[1]] + first[crossover_points[1]:]
    return first, second


def mutation(mut_prob, length, string):
    print("-------------- Mutation of ", string)
    for i in range(0, len(string)):
        if random.uniform(0, 1) < mut_prob:
            if string[i] == "0":
                string = string[:i] + "1" + string[i+1:]
            elif string[i] == "1":
                string = string[:i] + "0" + string[i + 1:]
            else:
                print("Something is Wrong. The ", i, " in string ", string, " is ", string[i])
            print("Mutation Done")
    print("-----------String after: ", string, "\n")
    return string


def knapsnack(x):  # fn: file name
    # Open file
    data = open(filename, "r")
    # Read first line and detect the number and MaxWeight
    first_line = data.readline().split(" ")
    numbers = int(first_line[0])
    max_weight = int(first_line[1])
    values = []
    weights = []
    # Read each line and calculate the weight and value for x
    for line in data:
        splited_data = line.split(" ")
        values.append(int(splited_data[0]))
        weights.append(int(splited_data[1]))
    sum_weight = 0
    sum_value = 0
    for i in range(0, len(x)):
        if x[i] == '1':
            sum_weight += weights[i]
            sum_value += values[i]
    if sum_weight > max_weight:
        sum_value = 0
    data.close()
    return sum_value


def parent_selection(persons, person_fitness, parentPercent, offspringPercent):
    # List of Fitness percents
    fitness_percent = []
    fitness_sum = 0
    for x in person_fitness:
        fitness_sum += x
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
indivSize = int(input("Enter the length of Individual: "))
popSize = int(input("Enter the number of population: "))
persons = population_generation(popSize, indivSize)
print("persons= ", persons)

filename = input("Enter the name of your file: ")
filename = "..//Dataset//" + filename + ".txt"
person_fitness = []
for person in persons:
    person_fitness.append(knapsnack(person))

parentPercent = float(input("Enter parent percent: "))
offspringPercent = float(input("Enter offspring percent: "))
maxGen = int(input("Enter max generation number: "))
crossoverProb = float(input("Enter Crossover Probability: "))
mutaionProb = float(input("Enter Mutation Probability: "))
reproduction(indivSize, crossoverProb, mutaionProb, persons, person_fitness, parentPercent, offspringPercent)
