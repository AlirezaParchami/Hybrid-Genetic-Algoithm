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


#a = "abcdefg"
#print(a[:3], a[3:])
indivSize = int(input("Enter the length of Individual: "))
popSize = int(input("Enter the number of population: "))
b = population_generation(popSize , indivSize)
print("b = " , b)
reproduction(b[0], b[1])