import numpy as np

def crossover(parent1, parent2):
    N = len(parent1)
    rnd = np.random.randint(N)
    child1 = parent1[:rnd] + parent2[rnd:]
    child2 = parent2[:rnd] + parent1[rnd:]
    return child1, child2

def mutation(child, M):
    N = len(child)
    rnd = np.random.randint(N)
    child[rnd] = [np.random.randint(5), np.random.randint(2), np.random.randint(1, 7), np.random.randint(1, M+1)]

    return child

def fitness(individual, t, g, s, c):
    # Initialize the fitness value
    fit = 0
    N = len(individual)

    #check if the number of students in the class is larger than the seat
    for i in range(N):
        room = individual[i][3] - 1
        if s[i] > c[room]:
            fit-=1
    
    #check if the class takes place in 1 session
    for i in range(N):
        start = individual[i][2]
        shift = t[i]

        if start+shift-1 > 6:
            fit-=1
    
    #Check if the instructor has the same teaching schedule
    for i in range(N-1):
        for j in range(i+1, N):
            if g[i]==g[j]:
                si = individual[i][0]*12 + individual[i][1]*6 +  individual[i][2]
                ei = si + t[i] -1
                sj = individual[j][0]*12 + individual[j][1]*6 +  individual[j][2]
                ej = sj + t[j] -1 

                if(si<=sj<=ei or si<=ej<=ei or (sj<=si and ei<=ej)):
                    fit-=1

    #Check to see if the classroom has the same class time
    for i in range(N-1):
        for j in range(i+1, N):
            if individual[i][3]==individual[j][3]:
                si = individual[i][0]*12 + individual[i][1]*6 +  individual[i][2]
                ei = si + t[i] -1
                sj = individual[j][0]*12 + individual[j][1]*6 +  individual[j][2]
                ej = sj + t[j] -1

                if(si<=sj<=ei or si<=ej<=ei or (sj<=si and ei<=ej)):
                    fit-=1

    return fit

def final_schedule(schedule: list, t: list, g: list, s: list, c: list):
    N = len(schedule)
    cancel = [0]*N
    cl = list(range(N))
    #check if the number of students in the class is larger than the seat
    for i in range(N):
        room = schedule[i][3] - 1
        if s[i] > c[room]:
            cancel[i] = 1

    #check if the class takes place in 1 session
    for i in range(N):
        start = schedule[i][2]
        shift = t[i]

        if start+shift-1 > 6:
            cancel[i] = 1

    drop = []
    for i in range(N):
        if cancel[i]==1:
            drop.append(i)
    drop.reverse()
    for d in drop:
        schedule.pop(d)
        t.pop(d)
        g.pop(d)
        s.pop(d)
        cl.pop(d)

    while(fitness(schedule, t, g, s, c)!=0):
        N = len(schedule)
        loss = [0]*N
        #Check if the instructor has the same teaching schedule
        for i in range(N-1):
            for j in range(i+1, N):
                if g[i]==g[j]:
                    si = schedule[i][0]*12 + schedule[i][1]*6 +  schedule[i][2]
                    ei = si + t[i] -1
                    sj = schedule[j][0]*12 + schedule[j][1]*6 +  schedule[j][2]
                    ej = sj + t[j] -1 

                    if(si<=sj<=ei or si<=ej<=ei or (sj<=si and ei<=ej)):
                        loss[i]+=1
                        loss[j]+=1

        #Check to see if the classroom has the same class time
        for i in range(N-1):
            for j in range(i+1, N):
                if schedule[i][3]==schedule[j][3]:
                    si = schedule[i][0]*12 + schedule[i][1]*6 +  schedule[i][2]
                    ei = si + t[i] -1
                    sj = schedule[j][0]*12 + schedule[j][1]*6 +  schedule[j][2]
                    ej = sj + t[j] -1

                    if(si<=sj<=ei or si<=ej<=ei or (sj<=si and ei<=ej)):
                        loss[i]+=1
                        loss[j]+=1

        loss = np.array(loss)
        idx = np.argmax(loss)
        schedule.pop(idx)
        t.pop(idx)
        g.pop(idx)
        s.pop(idx)
        cl.pop(idx)

    return schedule, cl 

    