import math
import numpy as np
import random

Profs = []
Courses = []
Times = []
Rooms = []
Span = []
Separates = []
Profs_bit_num = 0
Courses_bit_num = 0
Rooms_bit_num = 0
Day_bit_num = 3
Time_bit_num = 0

def read_file():
    global filename
    filename = "..//Dataset//" + filename + ".txt"
    fn = open(filename, 'r')
    for line in fn:
        first, second = line.split(" ")
        second = int(second)
        if first == "#Course":
            for i in range(0, second):
                tmp = fn.readline().split(" ")
                tmp[1] = int(tmp[1])
                if tmp[1] == -1:
                    tmp[1] = 30
                Courses.append(tmp)
        elif first == "#Prof":
           for i in range(0, second):
               tmp = fn.readline().splitlines()[0].split(" ")
               Profs.append(tmp)
        elif first == "#Time":
           for i in range(0, second):
               tmp = fn.readline().split(" ")
               tmp[1] = float(tmp[1])
               if tmp[1] == -1:
                   tmp[1] = 2
               Times.append(tmp)
        elif first == "#Room":
            for i in range(0, second):
                tmp = fn.readline().split(" ")
                tmp[1] = int(tmp[1])
                if tmp[1] == -1:
                    tmp[1] = 35
                Rooms.append(tmp)
        elif first == "#Span":
            for i in range(0, second):
                tmp = fn.readline().split(" ")
                tmp[0] = int(tmp[0])
                tmp[1] = int(tmp[1])
                Span.append(tmp[0])
                Span.append(tmp[1])
        elif first == "#Separate":
            for i in range(0, second):
                tmp = fn.readline().splitlines()[0].split()
                Separates.append(tmp)

def find_indivsize():
    global Profs_bit_num, Courses_bit_num, Rooms_bit_num, Time_bit_num, Day_bit_num
    Profs_bit_num += math.ceil( math.log(len(Profs),2) )
    Courses_bit_num += math.ceil( math.log(len(Courses), 2) )
    Rooms_bit_num += math.ceil( math.log(len(Rooms), 2) )
    Time_bit_num += math.ceil( math.log( abs(Span[1]-Span[0]), 2))
    size = Profs_bit_num + Courses_bit_num + Rooms_bit_num + Day_bit_num + Time_bit_num
    return size


def break_class():
    global Courses
    tmp = []
    for i in range(0, len(Rooms)):
        tmp.append(Rooms[i][1])
    tmp.sort()
    tmp.reverse()
    cond_bool = True
    while cond_bool:
        cond_bool = False
        for i in Courses:
            if i[1] > tmp[0]:
                cond_bool = True
                new_course = [i[0], tmp[0]]
                i[1] -= tmp[0]
                Courses.append(new_course)

def available_profs(course):
    Availables = []
    for prof in range(0,len(Profs)):
        if course[0] in Profs[prof]:
            Availables.append(prof)
    return Availables

def available_room(course):
    Availables = []
    for room in range(0,len(Rooms)):
        if course[1] == Rooms[room][1]:
            Availables.append(room)
    return Availables


def generate_persons():
    persons = []
    for course in range(0, len(Courses)):
        person = ""
        prof = available_profs(Courses[course])
        prof = prof[random.randint(0, len(prof)-1)]
        prof = bin(prof)[2:]
        lesson = bin(course)[2:]
        room = available_room(Courses[course])
        room = room[random.randint(0, len(room)-1)]
        room = bin(room)[2:]



filename = input("Enter File name: ")
read_file()
print("Profs: ", Profs)
print("Courses: ", Courses)
print("Rooms: ", Rooms)
# Day
print("Times: ", Times)
# During
print("Span: ", Span)
print("Separates: ", Separates)
break_class()
size = find_indivsize()
arr = np.random.randint(1, size=(Profs_bit_num + 1, Rooms_bit_num + 1, Day_bit_num + 1, Time_bit_num + 1))

print("Courses: ", Courses)