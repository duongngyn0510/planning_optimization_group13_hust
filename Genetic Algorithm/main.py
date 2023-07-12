from GA import genetic_algorithm
from util import final_schedule, fitness

def read_input(filename):
	t, g, s, c = [], [], [], []

	with open(filename) as f:
		[N, M] = [int(x) for x in f.readline().split()]
		for _ in range(N):
			l = [int(x) for x in f.readline().split()]
			t.append(l[0])
			g.append(l[1])
			s.append(l[2])
		c = [int(x) for x in f.readline().split()]
	return N, M, t, g, s, c

if __name__=='__main__':
	population_size = 8
	generations = 6000
	data = 'data.txt'
	N,M,t,g,s,c=read_input(data)

	best_individual = genetic_algorithm(N, M, generations, population_size, t, g, s, c)
	schedule, cl = final_schedule(best_individual, t, g, s, c)

	f_c = []
	for i in range(len(cl)):
		u = schedule[i][0]*12 + schedule[i][1]*6 +  schedule[i][2]
		f_c.append([cl[i]+1, u, schedule[i][3]])
		
	print(len(f_c))
	for i in range(len(f_c)):
		print(f_c[i][0], end = " ")
		print(f_c[i][1], end = " ")
		print(f_c[i][2])