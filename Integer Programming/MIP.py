from ortools.linear_solver import pywraplp


def Time(d):
    days = ["Monday morning", "Monday afternoon", "Tuesday morning", "Tuesday afternoon", "Wednesday morning",
            "Wednesday afternoon", "Thursday morning", "Thursday afternoon", "Friday morning", "Friday afternoon"]
    return days[d]


def solve_timetabling(n, m, t, g, s, rooms):
    solver = pywraplp.Solver(
        'schedule_classes', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    inf = solver.infinity()

    # binary variables indicating if class i is assigned to room r at day d, period p
    x = {}
    for i in range(n):
        for r in range(m):
            for d in range(10):
              for p in range(6):
                x[i, r, d, p] = solver.IntVar(
                    0, 1, 'x[%d,%d,%d,%d]' % (i, r, d, p))

    y = {}
    for i in range(n):
      y[i] = solver.IntVar(0, 1, 'y[%d]' % (i))

    # constraint 1: a teacher can only teach one class at a moment
    teachers = {}
    G = set(g)      # G is a set of teachers

    for i in G:
      teachers[i] = [j for j in range(n) if g[j] == i]

    for teacher in teachers:
      for d in range(10):
        for p in range(6):
            c = solver.Constraint(0, 1)
            for r in range(m):
                for i in teachers[teacher]:
                    c.SetCoefficient(x[i, r, d, p], 1)

    # constraint:
    for r in range(m):
        for d in range(10):
            c = solver.Constraint(0, 6)
            for i in range(n):
                for p in range(6):
                    c.SetCoefficient(x[i, r, d, p], 1)
    #
    for i in range(n):
        for r in range(m):
            for d in range(10):
                c = solver.Constraint(0, t[i])
                for p in range(6):
                    c.SetCoefficient(x[i, r, d, p], 1)

    # constraint: một lớp chỉ được nằm trong một phòng học
    for i in range(n):
                for r in range(m):
                    for ri in range(m):
                        if ri != r:
                            for d in range(10):
                                for di in range(10):
                                    for p in range(6):
                                        for pi in range(6):
                                            c = solver.Constraint(0, 1)
                                            c.SetCoefficient(x[i, r, d, p], 1)
                                            c.SetCoefficient(x[i, ri, di, pi], 1)
                                            
    # constraint: một lớp chỉ được nằm trong một buổi học
    for i in range(n):
        for d in range(10):
            for di in range(10):
                if di != d:
                    for r in range(m):
                        for ri in range(m):
                            for p in range(6):
                                for pi in range(6):
                                    c = solver.Constraint(0, 1)
                                    c.SetCoefficient(x[i, r, d, p], 1)
                                    c.SetCoefficient(x[i, ri, di, pi], 1)

    # constraint 2:The number of students is less than the room's capacity
    for i in range(n):
        for r in range(m):
            if s[i] > rooms[r]:
                for d in range(10):
                    for p in range(6):
                        cstr = solver.Constraint(0, 0)
                        cstr.SetCoefficient(x[i, r, d, p], 1)

    # constraint 3: There can be only one class at one room
    for r in range(m):
        for d in range(10):
            for p in range(6):
                cstr = solver.Constraint(0, 1)
                for i in range(n):
                    cstr.SetCoefficient(x[i, r, d, p], 1)

    # constraint 4: Each class must be assigned to at least one room

    for i in range(n):
        for d in range(10):
            for p in range(6):
                cstr = solver.Constraint(0, 1)
                for r in range(m):
                    cstr.SetCoefficient(x[i, r, d, p], 1)

    # constraint 5: các tiết học của một lớp phải liên tiếp nhau
    # không tồn tại cách xếp kiểu 101 1001 10001 100001
    # 0 1 2 3 4 5
    for i in range(n):
        if (t[i] > 1):
            for r in range(m):
                for d in range(10):
                    for p in range(4):
                        for q in range(p+2,6):
                            c=solver.Constraint(-1, 2)
                            c.SetCoefficient(x[i,r,d,p+1],1)
                            c.SetCoefficient(x[i,r,d,q-1],1)
                            c.SetCoefficient(x[i,r,d,p],-1)
                            c.SetCoefficient(x[i,r,d,q],-1)


    # value for y
    for i in range(n):
        c = solver.Constraint(0, 0)
        for r in range(m):
            for d in range(10):
                for p in range(6):
                    c.SetCoefficient(x[i, r, d, p], 1)
        c.SetCoefficient(y[i], -t[i])

    # objective function
    objective = solver.Objective()
    for i in range(n):
        objective.SetCoefficient(y[i], 1)
    objective.SetMaximization()
    solver.Solve()

    # print solution
    for i in range(n):
        for r in range(m):
            for d in range(10):
                for p in range(6):
                    if x[i, r, d, p].solution_value() > 0:
                        print(
                            f"Class {i} is assigned to room {r} on {Time(d)} at period {p}")
    count = 0
    for i in range(n):
        if y[i].solution_value() > 0:
            count += 1
    print(f"Total number of classes assigned: {count}")
    # print(objective.Value())


if __name__ == '__main__':
    n, m = map(int, input().split())
    classes = [list(map(int, input().split())) for _ in range(n)]
    rooms = list(map(int, input().split()))
    t = [classes[i][0] for i in range(n)]
    g = [classes[i][1] for i in range(n)]
    s = [classes[i][2] for i in range(n)]
    # print(f"Number of classes: {n}, number of rooms: {m}")
    # for i in range(n):
    #     print(
    #         f"Class {i} has teacher {g[i]}, {s[i]} students, and {t[i]} shifts")
    # for i in range(m):
    #     print(f"Room {i} has capacity {rooms[i]}")

    # teachers = {}
    # G = set(g)
    # print(G)

    # for i in G:
    #   teachers[i] = [j for j in range(n) if g[j] == i]
    # for teacher in teachers:
    #     print(f"Teacher {teacher} teaches classes {teachers[teacher]}")

    solve_timetabling(n, m, t, g, s, rooms)

