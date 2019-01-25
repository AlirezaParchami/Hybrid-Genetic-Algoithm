import math
import numpy as np
import random
import copy

Profs = []
Courses = []
Times = []
Rooms = []
Span = []
Separates = []
Days = 5
Profs_bit_num = 0
Courses_bit_num = 0
Rooms_bit_num = 0
Day_bit_num = 3
Time_bit_num = 0
a1 = 0
a2 = 0
a3 = 0
a4 = 0

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
               tmp[1] = math.ceil(tmp[1])
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
    for prof in range(0, len(Profs)):
        if course[0] in Profs[prof]:
            Availables.append(prof)
    return Availables


def available_room(course):
    Availables = []
    for room in range(0, len(Rooms)):
        if course[1] <= Rooms[room][1]:
            Availables.append(room)
    return Availables


def available_time(course, prof, room, day):
    Available = []
    hours = 0
    for i in Times:
        if course[0] == i[0]:
            hours = i[1]
            break
    x = False
    while x == False:
        for i in range(0, (Span[1]-Span[0])-hours):
            x = True
            for j in range(i, i+hours):
                if room_times[room][day][j] == 1 or prof_times[prof][day][j] == 1:
                    x = False
            if x == True:
                break
        if x == False:
            day = (day + 1) % 5
    for k in range(i, i+hours):
        room_times[room][day][k] = 1
        prof_times[prof][day][k] = 1

    return i, day



def generate_persons():
    persons = []
    for course in range(0, len(Courses)):
        print("========================================== ", course)
        prof = available_profs(Courses[course])
        prof = prof[random.randint(0, len(prof)-1)]
        room = available_room(Courses[course])
        room = room[random.randint(0, len(room)-1)]
        day = 0  # day = random.randint(0, 4)
        time, day = available_time(Courses[course], prof, room, day)
        print("course: ", Courses[course])
        print("prof: ", Profs[prof])
        print("room: ", Rooms[room])
        print("day: ", day)
        print("time: ", time)
        prof_room[prof][room] = 1
        person = Person(prof, course, room, day, time)
        person.toBit(Profs_bit_num, Courses_bit_num, Rooms_bit_num, Day_bit_num, Time_bit_num)
        persons.append(person)
    return persons


def fill_Times():
    courses_with_defined_time = []
    for i in Times:
        courses_with_defined_time.append(i[0])
    for course in Courses:
        if course[0] not in courses_with_defined_time:
            tmp = [course[0], 2]
            Times.append(tmp)


def num_days():
    days = 0
    for i in prof_times:
        for j in i:
            if 1 in j:
                days += 1
    return days


def num_rooms():
    rooms = 0
    for i in prof_room:
        for j in i:
            if j == 1:
                rooms += 1
    return rooms


def Total_time_a_day():
    hours = []
    for i in range(0,Days):
        hours.append(0)
    for i in range(0, len(Profs)):
        for j in range(0, Days):
            for k in range(0, Span[1]-Span[0]):
                hours[j] += prof_times[i][j][k]
    return hours


def sdt(hours):
    return np.var(hours)


def dist():
    distance = 0
    classes = []
    #for sep in Separates:
    #    tmp = []
    #    for person in persons:
    #        if Co#urses[person.course][0] in sep and Courses[person.course][0] not in tmp:
    return 0


def fitness(person):
    days = num_days()
    rooms = num_rooms()
    hours = Total_time_a_day()
    variance = sdt(hours)
    distance = dist()
    fit = (a1*days) + (a2*rooms) + (a3*variance) + (a4*distance)
    return fit


def switch_char(index, child):
    if child[index] == "1":
        child = child[:index] + "0" + child[index+1:]
    elif child[index] == "0":
        child = child[:index] + "1" + child[index+1:]
    else:
        print("Something is Wrong. The ", index, " in string ", child, " is ", child[index])
    return child


def check_condition(person):
    check = True
    if person.professor >= len(Profs) or person.course >= len(Courses) or person.room >= len(Rooms) or person.day >= Days or person.time >= Span[1]-Span[0]:
        check = False
        return check
    # The Professor should teach the course
    available_professors = available_profs(Courses[person.course])
    if Profs[person.professor][0] not in available_professors:
        check = False
        return check
    # The class capacity should be equal or greater than course capcity
    if Courses[person.course][1] > Rooms[person.room][1]:
        check = False
        return check
    # Professor should be free in that day and time
    t = 0
    for i in range(0, len(Times)):
        if Times[i][0] == Courses[person.course][0]:
            t = Times[i][1]
            break
    for i in range(person.time, person.time + t ):
        if prof_times[person.professor][person.day][i] == 1:
            check = False
            return check
    # The room should be free in that day and time
    for i in range(person.time, person.time + t ):
        if room_times[person.room][person.day][i] == 1:
            check = False
    return check


def mutation(person):
    # Professor Mutation
    for i in range(0, len(person.professor_bit)):
        if random.uniform(0, 1) < mutationProb:
            tmp = int(switch_char(i, person.professor_bit), 2)
            tmp_bit = ("{0:0" + str(Profs_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.professor = tmp
            p.professor_bit = tmp_bit
            if check_condition(p) == True:
                person.professor_bit = tmp_bit
                person.professor = tmp
    # Course Mutation
    for i in range(0, len(person.course_bit)):
        if random.uniform(0, 1) < mutationProb:
            tmp = int(switch_char(i, person.course_bit), 2)
            tmp_bit = ("{0:0" + str(Courses_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.course = tmp
            p.course_bot = tmp_bit
            if check_condition(p) == True:
                person.course_bit = tmp_bit
                person.course = tmp
    for i in range(0, len(person.room_bit)):
        if random.uniform(0, 1) < mutationProb:
            tmp = int(switch_char(i, person.room_bit), 2)
            tmp_bit = ("{0:0" + str(Rooms_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.room = tmp
            p.room_bit = tmp_bit
            if check_condition(p) == True:
                person.room = tmp
                person.room_bit = tmp_bit
    for i in range(0, len(person.day_bit)):
        if random.uniform(0,1) < mutationProb:
            tmp = int(switch_char(i, person.day_bit), 2)
            tmp_bit = ("{0:0" + str(Day_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.day_bit = tmp_bit
            p.day = tmp
            if check_condition(p) == True:
                person.day = tmp
                person.day_bit = tmp_bit
    for i in range(0, len(person.time_bit)):
        if random.uniform(0, 1) < mutationProb:
            tmp = int(switch_char(i, person.time_bit), 2)
            tmp_bit = ("{0:0" + str(Time_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.time_bit = tmp_bit
            p.time = tmp
            if check_condition(p) == True:
                person.time = tmp
                person.time_bit = tmp_bit
    return person


class Person:
    def __init__(self, professor, course, room, day, time):
        self.professor = professor
        self.course = course
        self.room = room
        self.day = day
        self.time = time

    def toBit(self, prof_bit_num, course_bit_num, room_bit_num, day_bit_num, time_bit_num):
        self.professor_bit = ("{0:0" + str(prof_bit_num) + "b}").format(self.professor)  # prof = bin(prof)[2:]
        self.course_bit = ("{0:0" + str(course_bit_num) + "b}").format(self.course)  # lesson = bin(course)[2:]
        self.room_bit = ("{0:0" + str(room_bit_num) + "b}").format(self.room)  # room = bin(room)[2:]
        self.day_bit = ("{0:0" + str(day_bit_num) + "b}").format(self.day)  # day = bin(day)[2:]
        self.time_bit = ("{0:0" + str(time_bit_num) + "b}").format(self.time)  # time = bin(time)[2:]
        self.person_bit = self.professor + self.course + self.room + self.day + self.time


filename = input("Enter File name: ")
read_file()
fill_Times()
print("Enter factors")
a1 = float(input("a1: "))
a2 = float(input("a2: "))
a3 = float(input("a3: "))
a4 = float(input("a4: "))
mutationProb = float(input("Enter Mutation Prob: "))
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
prof_times = np.random.randint(1, size=(len(Profs), Days, Span[1]-Span[0]) )
room_times = np.random.randint(1, size=(len(Rooms), Days, Span[1]-Span[0]) )
prof_room = np.random.randint(1, size=(len(Profs), len(Rooms)) )
print("Courses: ", Courses)
persons = generate_persons()
print("=================================================")
print("prof bit: ", Profs_bit_num, " Course bit: ", Courses_bit_num, " Room bit: ", Rooms_bit_num,
      " Day: ", Day_bit_num, " Time bit: ", Time_bit_num)
for i in range(0, len(persons)):
    print("========= ", i)
    a = mutation(persons[i])
    print("Mutated professor: ", Profs[a.professor])
    print("Mutated course: ", Courses[a.course])
    print("Mutated room: ", Rooms[a.room])
    print("Mutated day: ", a.day)
    print("Mutated time: ", a.time)
    print("")


#for person in persons:
#    fitness(person)
