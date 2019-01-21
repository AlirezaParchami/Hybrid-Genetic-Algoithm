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
    data = open(filename , "r")
    #Read first line and detect the number and MaxWeight
    first_line = data.readline().split(" ")
    numbers = int(first_line[0])
    max_weight = int(first_line[1])
    values = []
    weights = []
    for line in data:
        splited_data = line.split(" ")
        values.append(int(splited_data[0]))
        weights.append(int(splited_data[1]))
    for i in range(0, len(x)):
        sum_weight = 0
        sum_value = 0
        if (x[i] == '1'):
            sum_weight += weights[i]
            sum_value += values[i]
    if(sum_weight > max_weight):
        sum_value = 0
    return sum_value

#a = "abcdefg"
#print(a[:3], a[3:])
s = "00101"
for x in range(0, len(s)):
    print(x)
    print(type(s[x]))
    print(s[x])
    print(type(int(s[x],2)))
    print("---------------+")
indivSize = int(input("Enter the length of Individual: "))
popSize = int(input("Enter the number of population: "))
b = population_generation(popSize, indivSize)
print("b= ", b)
#reproduction(b[0], b[1])
fn = input("Enter the name of your file: ")
knapsnack(b[0], fn)
