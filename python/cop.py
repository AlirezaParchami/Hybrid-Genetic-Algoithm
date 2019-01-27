import math
import numpy as np
import random
import copy
import datetime

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


def available_time(course, prof, room, day, ans):
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
                if ans.room_times[room][day][j] == 1 or ans.prof_times[prof][day][j] == 1:
                    x = False
            if x == True:
                break
        if x == False:
            day = (day + 1) % 5
    for k in range(i, i+hours):
        ans.room_times[room][day][k] = 1
        ans.prof_times[prof][day][k] = 1
    return i, day


def optimum_day_for_prof(prof, ans):
    # Optimization Condition 1
    days = []
    for i in range(0, Days):
        tmp = 0
        for j in range(0, Span[1]-Span[0]):
            if ans.prof_times[prof][i][j] == 1:
                tmp +=1
        days.append(tmp)
    for i in range(0, len(days)):
        if i > 0 and i < Span[1]-Span[0]:
            return i
    # Optimization Condition 2
    total_hours_in_day = Total_time_a_day(ans)
    max_index = total_hours_in_day.index(max(total_hours_in_day))
    if total_hours_in_day[max_index] != 0:
        return total_hours_in_day.index(min(total_hours_in_day))
    # Return random index
    return random.randint(0, len(days)-1)


# Optimization Condition 3
def optimum_room_for_professor(prof, rooms, ans):
    howmany_times_professor_room = copy.copy(ans.prof_room)
    for i in range(0, len(howmany_times_professor_room)):
        max_index = howmany_times_professor_room[prof].argmax()
        if max_index in rooms:
            return max_index
        howmany_times_professor_room[prof][max_index] = 0
    return rooms[random.randint( 0, len(rooms)-1 )]


def generate_persons(ans):
    persons = []
    for course in range(0, len(Courses)):
#        print("========================================== ", course)
        prof = available_profs(Courses[course])
        # Select random professor because we don't have any optimization condition
        prof = prof[random.randint(0, len(prof)-1)]
        room = available_room(Courses[course])
        room = optimum_room_for_professor(prof, room, ans)  # room[random.randint(0, len(room)-1)]
        day = optimum_day_for_prof(prof, ans)
        time, day = available_time(Courses[course], prof, room, day, ans)
 #       print("course: ", Courses[course])
 #       print("prof: ", Profs[prof])
 #       print("room: ", Rooms[room])
 #       print("day: ", day)
 #       print("time: ", time)
        ans.prof_room[prof][room] += 1
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


def num_days(ans):
    days = 0
    for i in ans.prof_times:
        for j in i:
            if 1 in j:
                days += 1
    return days


def num_rooms(ans):
    rooms = 0
    for i in ans.prof_room:
        for j in i:
            if j == 1:
                rooms += 1
    return rooms


def Total_time_a_day(ans):
    hours = []
    for i in range(0,Days):
        hours.append(0)
    for i in range(0, len(Profs)):
        for j in range(0, Days):
            for k in range(0, Span[1]-Span[0]):
                hours[j] += ans.prof_times[i][j][k]
    return hours


def sdt(hours):
    return np.var(hours)


def dist(ans):
    distance = 0
    #for sep in Separates:
    #        tmp = []
    #        for person in ans.persons:
    #            if Courses[person.course][0] in sep and Courses[person.course][0] not in tmp:
    #                tmp.append(Courses[person.course][0])
    return distance


def fitness(ans):
    global count
    count += 1
    days = num_days(ans)
    rooms = num_rooms(ans)
    hours = Total_time_a_day(ans)
    variance = sdt(hours)
    distance = dist(ans)
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


def check_condition(person, ans):
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
        if ans.prof_times[person.professor][person.day][i] == 1:
            check = False
            return check
    # The room should be free in that day and time
    for i in range(person.time, person.time + t ):
        if ans.room_times[person.room][person.day][i] == 1:
            check = False
    return check


def mutation(person, ans):
    # Professor Mutation
    for i in range(0, len(person.professor_bit)):
        if random.uniform(0, 1) < mutationProb:
            tmp = int(switch_char(i, person.professor_bit), 2)
            tmp_bit = ("{0:0" + str(Profs_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.professor = tmp
            p.professor_bit = tmp_bit
            if check_condition(p, ans) == True:
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
            if check_condition(p, ans) == True:
                person.course_bit = tmp_bit
                person.course = tmp
    for i in range(0, len(person.room_bit)):
        if random.uniform(0, 1) < mutationProb:
            tmp = int(switch_char(i, person.room_bit), 2)
            tmp_bit = ("{0:0" + str(Rooms_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.room = tmp
            p.room_bit = tmp_bit
            if check_condition(p, ans) == True:
                person.room = tmp
                person.room_bit = tmp_bit
    for i in range(0, len(person.day_bit)):
        if random.uniform(0,1) < mutationProb:
            tmp = int(switch_char(i, person.day_bit), 2)
            tmp_bit = ("{0:0" + str(Day_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.day_bit = tmp_bit
            p.day = tmp
            if check_condition(p, ans) == True:
                person.day = tmp
                person.day_bit = tmp_bit
    for i in range(0, len(person.time_bit)):
        if random.uniform(0, 1) < mutationProb:
            tmp = int(switch_char(i, person.time_bit), 2)
            tmp_bit = ("{0:0" + str(Time_bit_num) + "b}").format(tmp)
            p = copy.copy(person)
            p.time_bit = tmp_bit
            p.time = tmp
            if check_condition(p, ans) == True:
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
#    persons = []


class Population:
    def __init__(self, Profs_size, Days_size, Span_size, Rooms_size):
        self.prof_times = np.random.randint(1, size=(Profs_size, Days_size, Span_size))
        self.room_times = np.random.randint(1, size=(Rooms_size, Days_size, Span_size))
        self.prof_room = np.random.randint(1, size=(Profs_size, Rooms_size))
        self.persons = []
        self.fitness = 0

    def update_prof_times(self):
        for i in range(0, len(Profs)):
            for j in range(0, Days):
                for k in range(0, Span[1]-Span[0]):
                    self.prof_times[i][j][k] = 0

        for i in self.persons:
            self.prof_times[i.professor][i.day][i.time] += 1

    def update_room_times(self):
        for i in range(0, len(Rooms)):
            for j in range(0, Days):
                for k in range(0, Span[1]-Span[0]):
                    self.room_times[i][j][k] = 0
        for i in self.persons:
            self.room_times[i.room][i.day][i.time] += 1

    def update_prof_room(self):
        for i in range(0, len(Profs)):
            for j in range(0, len(Rooms)):
                self.prof_times[i][j] = 0
        for i in self.persons:
            self.prof_room[i.professor][i.room] += 1

    def update(self):
        self.update_prof_times()
        self.update_room_times()
        self.update_prof_room()



def parent_selection_cop(pops):
    fitness_percent = []
    fitness_sum = 0
    for x in pops:
        fitness_sum += x.fitness
    tmp = 0
    for x in pops:
        tmp += (x.fitness/fitness_sum)
        fitness_percent.append(tmp)

    candidate_parents = []
    for i in range(0, int(math.floor(parentPercent*len(pops)))):
        prob = random.uniform(0, 1)
        for j in range(0, len(fitness_percent)):
            if prob < fitness_percent[j]:
                candidate_parents.append(pops[j])
                break

    selected_parents = []
    for i in range(0, int(math.floor(offspringPercent*len(pops)/2))):
        index1 = random.randint(0, len(candidate_parents)-1 )
        index2 = random.randint(0, len(candidate_parents)-1 )
        pair = []
        pair.append(candidate_parents[index1])
        pair.append(candidate_parents[index2])
        selected_parents.append(pair)
    return selected_parents


def crossover_cop(first_pop, second_pop):
    if random.uniform(0, 1) > crossoverPercent:
        return first_pop, second_pop
    rands = random.sample(range( 1, min(len(first_pop.persons),len(second_pop.persons))-1 ), 2)
    rands.sort()
    tmp = first_pop.persons[rands[0]:rands[1]]
    first_pop_tmp = copy.copy(first_pop)
    second_pop_tmp = copy.copy(second_pop)
    first_pop.persons[rands[0]:rands[1]] = second_pop.persons[rands[0]:rands[1]]
    second_pop.persons[rands[0]:rands[1]] = tmp
    first_pop.update()
    second_pop.update()
    consistency = True
    for i in first_pop.persons:
        if check_condition(i, first_pop) == False:
            consistency = False
    for i in second_pop.persons:
        if check_condition(i, second_pop) == False:
            consistency = False
    if consistency == True:
        return first_pop, second_pop
    return first_pop_tmp, second_pop_tmp


def reproduction_cop(pops):
    children = []
    SP = parent_selection_cop(pops)  # A list of tuples of population
    for pair in SP:
        pair[0], pair[1] = crossover_cop(pair[0], pair[1])
        pair[0].update()
        pair[1].update()
        for item in range( 0, len(pair[0].persons) ):
            pair[0].persons[item] = mutation(pair[0].persons[item], pair[0])
        pair[0].update()
        for item in range(0, len(pair[1].persons)):
            pair[1].persons[item] = mutation(pair[1].persons[item], pair[1])
        pair[1].update()
        children.append(pair[0])
        children.append(pair[1])
    return children


filename = input("Enter File name: ")
read_file()
fill_Times()
print("Enter factors")
a1 = float(input("a1: "))
a2 = float(input("a2: "))
a3 = float(input("a3: "))
a4 = float(input("a4: "))
parentPercent = float(input("Enter parent Percent: "))
offspringPercent = float(input("Enter offspring Percent: "))
crossoverPercent = float(input("Enter crossover Percent"))
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
print("Courses: ", Courses)

maxGen = int(input("Enter The maximum Generation: "))
popSize = int(input("Enter Population Size: (Recommend to lower than maxGen)"))
run_times = 5
results = []

output_file_name = "COP_log" + str(datetime.datetime.now()).split(" ")[1].replace(":", "_") + ".txt"
output = open(output_file_name, "x")


for rt in range(0, run_times):
    count = 0
    populationS = []
    for g in range(0, maxGen):
        population = Population(len(Profs), Days, Span[1]-Span[0], len(Rooms))
        population.persons = generate_persons(population)
        population.fitness = fitness(population)
        populationS.append(population)
    children = reproduction_cop(populationS)
    populationS = populationS + children
    for j in populationS:
        j.fitness = fitness(j)
    populationS.sort(key=lambda o:o.fitness)
    populationS.reverse()
    populationS = populationS[:popSize]
    output.write("\n" + "================================================= RUN: " + str(rt) + "\n")
    output.write("Best Population Fitness:" +  str(populationS[0].fitness) + "\n")
    ave_fitness = 0
    for i in populationS:
        ave_fitness += i.fitness
    ave_fitness /= popSize
    output.write("Fitness Average:" + str(ave_fitness) + "\n")

    output.write("Best Schedule:" + "\n")
    for j in populationS[0].persons:
        output.write("Professor: " + str(Profs[j.professor]) + "\n")
        output.write("Course: " + str(Courses[j.course]) + "\n")
        output.write("Room: " + str(Rooms[j.room]) + "\n")
        output.write("Day: " + str(j.day) + "\n")
        output.write("Time: " + str(j.time + Span[0]) + "\n" + "\n")
    result = [populationS[0], ave_fitness, count]
    results.append(result)
output.write("\n" + "*****************************************************Finally:" + "\n")
results.sort(key=lambda o:o[0].fitness)
results.reverse()
ave_ave_fitness = 0
ave_count = 0
for i in results:
    ave_ave_fitness += i[1]
    ave_count += i[2]
ave_ave_fitness /= len(results)
ave_count /= len(results)
output.write("Average of Average of fitness:" + str(ave_ave_fitness) + "\n")
output.write("Best Person:" + "\n")
for j in results[0][0].persons:
    output.write("Professor: " + str(Profs[j.professor]) + "\n")
    output.write("Course: " + str(Courses[j.course]) + "\n")
    output.write("Room: " + str(Rooms[j.room]) + "\n")
    output.write("Day: " + str(j.day) + "\n")
    output.write("Time: " + str(j.time + Span[0]) + "\n")


