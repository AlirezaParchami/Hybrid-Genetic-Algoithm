import string
import random

def individual_generation (n):
    "create schotastic individuals"
    s = ""
    binary_list = ['0' , '1']
    for num in range(n):
        s += random.choice(binary_list);
    return s

def population_generation (n):
    "Generate Population Set"
    myList =[]
    for num in range(n):
        myList.append(individual_generation(10))
    return myList


a = individual_generation(5)
b = population_generation(5)
print("a = " , a)
print("b= " , b)