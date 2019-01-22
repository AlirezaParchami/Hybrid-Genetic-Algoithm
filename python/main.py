import string
import random
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
    myList =[]
    for num in range(pop_size):
        myList.append(individual_generation(indiv_size))
    return myList


def reproduction(x, y):
    """Reproduce an individual from x and y"""
    individual_length = len(x)
    crossover_point = randint(0, individual_length)
    individual = x[:crossover_point] + y[crossover_point:]
    print("x=", x, "y=", y, "individual=" ,individual, "CrossoverPoint=",crossover_point)
    return individual


def knapsnack(x, fn):
    # Open file
    filename = "..//Dataset//" + fn + ".txt"
    data = open(filename, "r")
    #Read first line and detect the number and MaxWeight
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
        if (x[i] == '1'):
            sum_weight += weights[i]
            sum_value += values[i]
    if(sum_weight > max_weight):
        sum_value = 0
    return sum_value

#a = "abcdefg"
#print(a[:3], a[3:])
indivSize = int(input("Enter the length of Individual: "))
popSize = int(input("Enter the number of population: "))
b = population_generation(popSize, indivSize)
print("b= ", b)

fn = input("Enter the name of your file: ")
person_fitness = []
for person in b:
    person_fitness.append(knapsnack(person, fn))

#reproduction(b[0], b[1])
