import string
import random
import math
from random import randint


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


def reproduction(x, y):
    """Reproduce an individual from x and y"""
    individual_length = len(x)
    # TODO: be careful about the range of crossover_point. maybe randint(0, individual_length)
    crossover_point = randint(0, individual_length)
    individual = x[:crossover_point] + y[crossover_point:]
    print("x=", x, "y=", y, "individual=" ,individual, "CrossoverPoint=",crossover_point)
    return individual


def knapsnack(x, fn):
    # Open file
    filename = "..//Dataset//" + fn + ".txt"
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



indivSize = int(input("Enter the length of Individual: "))
popSize = int(input("Enter the number of population: "))
persons = population_generation(popSize, indivSize)
print("persons= ", persons)

fn = input("Enter the name of your file: ")
person_fitness = []
for person in persons:
    person_fitness.append(knapsnack(person, fn))

parentPercent = float(input("Enter parent percent: "))
offspringPercent = float(input("Enter offspring percent: "))
maxGen = int(input("Enter max generation number: "))
crossoverProb = float(input("Enter Crossover Probability: "))
mutaionProb = float(input("Enter Mutation Probability: "))
SP = parent_selection(persons, person_fitness, parentPercent, offspringPercent)  # Selected Parents
# reproduction(persons[0], persons[1])
