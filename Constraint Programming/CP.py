from ortools.sat.python import cp_model
import time
import numpy as np

def read_local_input(filename):
    t = []
    g = []
    s = []
    with open(filename) as f:
        [N, M] = [int(x) for x in f.readline().split()]
        for _ in range(N):
            l = [int(x) for x in f.readline().split()]
            t.append(l[0])
            g.append(l[1])
            s.append(l[2])
        c = [int(x) for x in f.readline().split()]
    return N, M, t, g, s, c

def read_erp_input():
    t = []
    g = []
    s = []

    N, M = map(int, input().split())
    items = [tuple(map(int, input().split())) for i in range(N)]
    c = list(map(int, input().split()))
    for item in items:
        t.append(item[0])
        g.append(item[1])
        s.append(item[2])    
    return N, M, t, g, s, c

class ConstraintProgrammingSolver:
    def __init__(self, N, M, t, g, s, c, trial=False):
        """
        Args:
            N: number of classes
            M: number of rooms
            t: list containing the number of periods of the classes
            g: list containing teachers of the classes
            s: list containing the number of students of the classes
            c: list containing the capacity of the rooms
            trial: run for estimate time execute
        """
        self.N = N
        self.M = M
        self.t = t
        self.g = g 
        self.s = s
        self.c = c
        self.trial = trial

        G0 = set(g)
        self.G = {}
        for i in G0:
            self.G[i] = [j for j in range(N) if g[j] == i]

    def set_model(self):
        self.model = cp_model.CpModel()

        self.x = {}
        self.y = None

        for i in range(self.N):
            for d in range(10):
                for k in range(6):
                    for r in range(self.M):
                        self.x[i, d, k, r] = self.model.NewIntVar(0, 1, f'x[{i}, {d}, {k}, {r}]',)
        self.y = [self.model.NewIntVar(0, 1, f'y[{i}]') for i in range(self.N)]

        
    def set_constraint(self):

        # Number of students in each class <= room capacity
        for i in range(self.N):
            for d in range(10):
                for k in range(6):
                    for r in range(self.M):
                        self.model.Add(self.x[i, d, k, r] * self.s[i] <= self.c[r])

        # Two classes having the same teacher have to be scheduled separately
        for p in self.G: 
            for d in range(10):
                for k in range(6):
                    self.model.Add(sum(self.x[i, d, k, r] for i in self.G[p] for r in range(self.M)) <= 1)

        # Only one class in one room at a time
        for d in range(10):
            for k in range(6):
                for r in range(self.M):
                    self.model.Add(sum(self.x[i, d, k, r] for i in range(self.N)) <= 1)

        # A room is assigned to only one class at a time
        for d in range(10):
            for k in range(6):
                for i in range(self.N):
                    self.model.Add(sum(self.x[i, d, k, r] for r in range(self.M)) <= 1)

        # Lessons must be completed in one session
        for i in range(self.N):
            for r in range(self.M):
                for d in range(10):
                    c = self.model.NewBoolVar('c')
                    self.model.Add(sum(self.x[i, d, k, r] for k in range(6)) == t[i]).OnlyEnforceIf(c)
                    self.model.Add(sum(self.x[i, d, k, r] for k in range(6)) == 0).OnlyEnforceIf(c.Not())

        # Lessons of each class must be continuous
        for i in range(self.N):
            for r in range(self.M):
                for d in range(10):
                    for b in range(6 - t[i]):
                        self.model.Add(sum(self.x[i, d, k, r] for k in range(b, b + t[i])) == self.x[i, d, b, r] * t[i]).OnlyEnforceIf(self.x[i, d, b, r])

        # Constraint for y
        for i in range(self.N):  
            c = self.model.NewBoolVar('')
            self.model.Add(self.y[i] == 1).OnlyEnforceIf(c)
            self.model.Add(self.y[i] == 0).OnlyEnforceIf(c.Not())
            self.model.Add(sum(self.x[i, d, k, r] for d in range(10) for k in range(6) for r in range(self.M)) == t[i]).OnlyEnforceIf(c)
            self.model.Add(sum(self.x[i, d, k, r] for d in range(10) for k in range(6) for r in range(self.M)) < t[i]).OnlyEnforceIf(c.Not())
    
    def set_objective(self):
        self.model.Maximize(sum(self.y[i] for i in range(self.N)))
    
    def solve(self):
        self.set_model()
        self.set_constraint()
        self.set_objective()

        self.solver = cp_model.CpSolver()  
        self.status = self.solver.Solve(self.model)

    def print_solution(self):
        self.solve() 
        if not self.trial:
            print(int(self.solver.ObjectiveValue()))
            results = []
            if self.status == cp_model.OPTIMAL:
                for i in range(self.N):
                    for d in range(10):
                        for k in range(6):
                            for r in range(self.M):
                                if self.solver.Value(self.x[i, d, k, r]):
                                    # print(f'Class {i + 1} has session: {d + 1} - lesson: {k + 1} - room: {r + 1} - teacher: {self.g[i]}')
                                    results.append([i + 1, d * 6 + (k + 1), r + 1])
            else:
                print(-1)

            classes = set()
            for result in results:
                class_ = result[0]
                if class_ not in classes:
                    classes.add(class_)
                    print(result[0], result[1], result[2])

        # print(f'The maximum number of scheduled classes is: {int(self.solver.ObjectiveValue())}')

if __name__ == '__main__':
    filename = "data.txt"

    # # run in local
    # N, M, t, g, s, c = read_local_input(filename)
    # t1 = time.time()
    # solver = ConstraintProgrammingSolver(N, M, t, g, s, c)
    # solver.print_solution()
    # t2 = time.time()
    # t = t2 - t1
    # print('Total run time: ', t)

    # # run in erp  
    # # N, M, t, g, s, c = read_erp_input()
    # t1 = time.time()
    # solver = ConstraintProgrammingSolver(N, M, t, g, s, c)
    # solver.print_solution()
    # t2 = time.time()
    # t = t2 - t1
    # print('Total run time: ', t)
    
    # run for experiment
    time_list = []
    trial = 0
    while trial < 10:
        N, M, t, g, s, c = read_local_input(filename)
        t1 = time.time()
        solver = ConstraintProgrammingSolver(N, M, t, g, s, c, trial=True)
        solver.print_solution()
        t2 = time.time()
        t = t2 - t1
        time_list.append(t)
        trial += 1
    print(f'Time executed: {np.mean(time_list):.4f} +- {np.std(time_list):.4f}')