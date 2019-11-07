import numpy as np
import random
import functools
import copy
import operator
from functools import reduce
import sys
import time
totaltime = 0
time_start = 0
vertices = 0
depot = 0
requiredEdge = 0
nRequiredEdge = 0
vehicles = 0
totalCost = 0
costs = None
minCost = None
IFINITY = 100000
allDemands = []
alldemandedge = set()
lamda = 0


class solution:
	routes = []
	costs = 0

	def __init__(self, routes, costs):
		self.routes = routes
		self.costs = costs

def check(sol,t):
	demands = copy.deepcopy(allDemands)
	for i in sol:
		for (a,b) in i:
			if demands[a][b]!=0:
				demands[a][b] = 0
			else:
				print(t)
			if demands[b][a]!=0:
				demands[b][a] = 0
			else:
				print(t)


def c(n, k):
	return reduce(operator.mul, range(n - k + 1, n + 1)) / reduce(operator.mul, range(1, k + 1))


def ReadFile(file_name):
	i = 1;
	for lines in open(file_name):
		if (lines == 'END'):
			break
		if (i > 9):
			lines = lines.split(' ')
			a = int(lines[0])
			b = int(lines[3])
			cost = int(lines[6])
			demand = int(lines[-1][:-1])
			costs[a][b] = cost
			costs[b][a] = cost
			minCost[a][b] = cost
			minCost[b][a] = cost
			if demand>0:
				allDemands[a][b] = demand
				allDemands[b][a] = demand
				alldemandedge.add((a,b))
				alldemandedge.add((b,a))
		i += 1


def floyd(A):
	for a in range(len(A)):
		for b in range(len(A)):
			for c in range(len(A)):
				if (A[b][a] + A[a][c] < A[b][c]):
					A[b][c] = A[b][a] + A[a][c]
	return A


def pathScaning(method, alldemandedge):
	finalresult = []
	tempt = set()
	for i in alldemandedge:
		tempt.add(i)
	while len(tempt)!=0:
		routes = []
		leftCap = capacity
		start = depot
		while leftCap>0:
			closest = set()
			mincost = IFINITY+1
			# print(tempt)
			for key in tempt:
				a,b = key
				if (minCost[start][a] == mincost):
					closest.add(key)
				elif (minCost[start][a] < mincost):
					closest = set()
					closest.add(key)
					mincost = minCost[start][a]


			closest2 = set()
			for i in closest:
				closest2.add(i)
			for p,q in closest2:
				if allDemands[p][q]>leftCap:
					closest.remove((p,q))

			result = None
			if (len(closest) == 0):
				break;
			if (len(closest) == 1):
				for i in closest:
					result = i
			else:
				if method == 1:  ###maxmize the dis from the head to the depot
					maxdis = 0
					result = None
					for (a, b) in closest:
						if (minCost[b][depot] >= maxdis):
							result = (a, b)
							maxdis = minCost[b][depot]
				elif method == 2:  ###minimize the dis from the head to the depot
					mindis = IFINITY - 1
					result = None
					for (a, b) in closest:
						if (minCost[b][depot] < mindis):
							result = (a, b)
							mindis = minCost[b][depot]
				elif method == 3:  ###maximize dem(t)/sc(t)
					demsc = 0
					result = None
					for (a, b) in closest:
						demsc2 = allDemands[a][b]/ costs[a][b]
						if (demsc2 >= demsc):
							result = (a, b)
							demsc = demsc2
				elif method == 4:  ###minimize dem(t)/sc(t)
					demsc = IFINITY
					result = None
					for (a, b) in closest:
						demsc2 = allDemands[a][b] / costs[a][b]
						if (demsc2 < demsc):
							result = (a, b)
							demsc = demsc2
				elif method == 5:  ###if capacity <=0.5capacity then use method1 otherwise use method 2
					if leftCap >= 0.5 * capacity:
						maxdis = 0
						result = None
						for (a, b) in closest:
							if (minCost[b][depot] >= maxdis):
								result = (a, b)
								maxdis = minCost[b][depot]
					else:
						mindis = IFINITY
						result = None
						for (a, b) in closest:
							if (minCost[b][depot] < mindis):
								result = (a, b)
								mindis = minCost[b][depot]
				elif method == 6:
					result = random.choice(list(closest))

			routes.append(result)
			c,d = result
			start = d
			leftCap -= allDemands[c][d]
			tempt.remove(result)
			tempt.remove((d,c))

		finalresult.append(routes)


	return finalresult


def calculate2(routes):
	load = 0
	Cost = 0
	start = depot
	for (a, b) in routes:
		Cost += minCost[start][a]
		Cost += costs[a][b]
		start = b
	Cost += minCost[start][depot]
	return Cost


def getCrossOver(task, routes):
	minGrade = IFINITY
	finalresult = []
	for i in range(len(routes)):
		list.insert(routes, i, task)
		temptGrade = calculate2(routes)
		if temptGrade < minGrade:
			finalresult = copy.deepcopy(routes)
		routes.remove(task)

	return finalresult


def calculateLoad(routes):
	load = 0

	for (a, b) in routes:
		load += allDemands[a][b]
	return load


def crossOver(S1, S2):
	# time_start = time.time()
	times = 100
	while times>0:
		times-=1

		r1 = random.randint(0, len(S1) - 1)
		r2 = random.randint(0, len(S2) - 1)
		R1 = (S1[r1])
		R2 = (S2[r2])
		r1 = random.randint(0, len(R1) - 1)
		R11 = R1[:r1]
		R12 = R1[r1:]

		r2 = random.randint(0, len(R2) - 1)
		R22 = R2[r2:]
		R1loss = []  ###the tasks that R1new don't have
		###find out the lost one
		for (a, b) in R12:
			if ((a, b) not in R22) or ((b, a) not in R22):
				R1loss.append((a, b))
		# print("R22", R22)
		###handle duplicate
		for (a, b) in R22:
			for q in S1:
				if q == R1:
					if ((a, b) in R11) or ((b, a) in R11):
						R22.remove((a, b))
						break
				if ((a, b) in q) or ((b, a) in q):
					R22.remove((a, b))
					break
		R1new = []
		if R11 != []:
			R1new = (R11)
		if R22 != []:
			if R1new == []:
				R1new = (R22)
			else:
				R1new = R1new + (R22)
		# print("R1new",R1new)
		# print("R1loss:",R1loss)
		for i in R1loss:
			R1new = getCrossOver(i, R1new)

		if (R1new != []):
			while ([] in R1new):
				R1new.remove([])

			if calculateLoad(R1new) > capacity:
				continue
			else:
				if(calculate2(R1new)<calculate2(R1)):
					S1.remove(R1)
					S1.append(R1new)
					break
				else:
					continue
	# time_end = time.time()
	# print("CrossOverTime", time_end - time_start)
	return S1


def singleInsertion(S):
	# print(S)
	S1 = copy.deepcopy(S)
	allCost = calculate(S)
	currentCost = allCost
	currentSol = copy.deepcopy(S1)
	for i in range(len(S1)):
		for j in range(len(S1[i])):
			for i2 in range(len(S1)):
				for j2 in range(len(S1[i2]) + 1):
					if i2 == i and j2 == j:
						continue
					value = S1[i][j]

					list.insert(S1[i2], j2, value)
					if(calculateLoad(S1[i2])>capacity):
						S1[i2].remove(value)
						continue
					S1[i].remove(value)
					currentCost = calculate(S1)
					if (currentCost < allCost):
						allCost = currentCost
						currentSol = copy.deepcopy(S1)

					S1[i2].remove(value)
					list.insert(S1[i], j, value)
	while ([] in currentSol):
		currentSol.remove([])
	return currentSol


def doubleInsertion(S):
	allCost = calculate(S)
	S1 = copy.deepcopy(S)
	currentCost = allCost
	currentSol = copy.deepcopy(S1)
	for i in range(len(S1)):
		for j in range(len(S1[i])-1):
			for i2 in range(len(S1)):
				for j2 in range(len(S1[i2]) + 1):
					if i2 == i and j2 == j:
						continue
					value1 = S1[i][j]
					value2 = S1[i][j + 1]


					list.insert(S1[i2], j2, value2)
					list.insert(S1[i2], j2, value1)
					if (calculateLoad(S1[i2]) > capacity):
						S1[i2].remove(value1)
						S1[i2].remove(value2)
						continue
					S1[i].remove(value1)
					S1[i].remove(value2)

					currentCost = calculate(S1)

					if (currentCost < allCost):
						allCost = currentCost
						currentSol = copy.deepcopy(S1)
					# print(currentCost)
					# print(S)
					S1[i2].remove(value1)
					S1[i2].remove(value2)
					list.insert(S1[i], j, value2)
					list.insert(S1[i], j, value1)


	while ([] in currentSol):
		currentSol.remove([])
	return currentSol


def swap(S):
	allCost = calculate(S)
	S1 = copy.deepcopy(S)
	currentCost = allCost
	currentSol = copy.deepcopy(S1)
	for i in range(len(S1)):
		for j in range(len(S1[i])):
			for i2 in range(len(S1)):
				for j2 in range(len(S1[i2])):
					if i2 == i and j2 == j:
						continue
					value1 = S1[i][j]
					value2 = S1[i2][j2]
					S1[i].remove(value1)
					S1[i2].remove(value2)
					list.insert(S1[i2], j2, value1)
					list.insert(S1[i], j, value2)
					if (calculateLoad(S1[i2]) > capacity )or( calculateLoad(S1[i]) > capacity):
						S1[i2].remove(value1)
						S1[i].remove(value2)
						list.insert(S1[i], j, value1)
						list.insert(S1[i2], j2, value2)
						continue
					currentCost = calculate(S1)

					if (currentCost < allCost):
						allCost = currentCost
						currentSol = copy.deepcopy(S1)

					S1[i2].remove(value1)
					S1[i].remove(value2)
					list.insert(S1[i], j, value1)
					list.insert(S1[i2], j2, value2)

	while ([] in currentSol):
		currentSol.remove([])
	return currentSol


def MS(S):
	# print(S)
	p = 2
	havechosen = []
	newbetter = None
	newbetterscore = 0
	total = c(len(S), p)
	removed1 = []
	removed2 = []
	if total > 100:
		total = 100
	while (total > 0):
		while True:
			a = random.randint(0, len(S) - 1)
			while True:
				b = random.randint(0, len(S) - 1)
				if b != a:
					break
			if (a,b) not in havechosen and (b,a) not in havechosen:
				break
		havechosen.append((a,b))
		havechosen.append((b,a))

		route1 = S[a]
		route2 = S[b]
		newtask = set(route1 + route2)
		newtasks = set()
		rowscore = calculate2(route1)+calculate2(route2)
		for (a,b) in newtask:
			if(allDemands[a][b]>0):
				newtasks.add((a,b))
			if (allDemands[b][a]>0):
				newtasks.add((b,a))

		results = []
		for i in range(5):
			results.append(pathScaning(i + 1, newtasks))

		results = sorted(results, key=functools.cmp_to_key(compare))
		route0 = results[0]
		route0grade = calculate(route0)
		if route0grade<rowscore:
			if newbetter is None:
				newbetter = results[0]
				newbetterscore = rowscore-route0grade
				removed1 = copy.deepcopy(route1)
				removed2 = copy.deepcopy(route2)
			else:
				score = rowscore-route0grade
				if newbetterscore < score:
					newbetter = route0
					newbetterscore = score
					removed1 = copy.deepcopy(route1)
					removed2 = copy.deepcopy(route2)
		total -= 1
	if newbetter is not None:

		S.remove(removed1)
		S.remove(removed2)
		S = S + newbetter

	return S


def localSearch(Sx):
	# time_start = time.time()
	Sls = None
	new1 = singleInsertion(Sx)
	# for i in new1 :
	# 	if calculateLoad(i)>capacity:
			# print("new1")
	grade1 = calculate(new1)
	new2 = doubleInsertion(Sx)
	# for i in new2 :
	# 	if calculateLoad(i)>capacity:
	# 		print("new2")
	grade2 = calculate(new2)
	new3 = swap(Sx)
	grade3 = calculate(new3)
	# for i in new3 :
	# 	if calculateLoad(i)>capacity:
	# 		print("new3")

	if (grade1 <= grade2 and grade1 <= grade3):
		Sls = new1
	elif (grade2 <= grade1 and grade2 <= grade3):
		Sls = new2
	else:
		Sls = new3
	Sls = MS(Sls)
	# for i in Sls :
	# 	if calculateLoad(i)>capacity:
	# 		print("SLS")
	# time_end = time.time()

	return Sls


def calculate(item1):
	Cost = 0
	for routes in item1:
		load = 0
		start = depot
		for (a, b) in routes:
			load += allDemands[a][b]
			Cost += minCost[start][a]
			Cost += costs[a][b]
			start = b
		Cost += minCost[start][depot]
	return Cost


def compare(item1, item2):
	grade1 = calculate(item1)
	grade2 = calculate(item2)
	if grade1 < grade2:
		return -1
	elif grade1 > grade2:
		return 1
	else:
		return 0


def MEANS(psize, opsize, ubtrial, Pls):
	###Initialization
	pop = []
	# time_start = time.time()

	while (len(pop) < psize):
		ntrial = 0
		Sini = []
		time_start = time.time()
		while (ntrial < ubtrial):
			ntrial += 1

			Sini = pathScaning(6, alldemandedge)

			if Sini not in pop:
				break
		if Sini in pop:
			break
		pop.append(Sini)
	# time_end = time.time()
	# print("pathScaning:",(time_end-time_start))
	pop = sorted(pop, key=functools.cmp_to_key(compare))

	return pop[0]
	psize = len(pop)
	# print(psize)
	if (psize == 1):
		return pop[0]
	###MainLoot
	circles = 30
	counter = 0
	time_end = time.time()
	while (totaltime-time_end>6):
		counter+=1
		# print(circles)
		popt = copy.deepcopy(pop)
		lamda = 0
		for i in range(opsize):

			# while True:
			# 	b = random.randint(0, len(popt) - 1)
			# 	if b != 0:
			# 		break
			# # 随即交配产生后代
			# S1 = copy.deepcopy(popt[0])
			# S2 = copy.deepcopy(popt[b])
			# Sx = crossOver(S1, S2)
			# Sx2 = copy.deepcopy(popt[0])
			# r = random.random()
			# if r < Pls:
			# 	Sls = localSearch(Sx)
			# 	Sls2 = localSearch(Sx2)
			# 	# print("Sls", Sls)
			# 	if Sls not in popt:
			# 		popt.append(Sls)
			# 		# print(1, calculate(Sls))
			# 	if Sls2 not in popt:
			# 		popt.append(Sls2)
			# 		# print(1, calculate(Sls2))
			# 	elif Sx not in popt:
			# 		popt.append(Sx)
			# 		# print(2, calculate(Sx))
			# elif Sx not in popt:
			# 	popt.append(Sx)
			# 	# print(3, calculate(Sx))
			# popt = sorted(popt, key=functools.cmp_to_key(compare))
			# # print("min", calculate(popt[0]))


			# a = random.randint(0, len(popt) - 1)
			# while True:
			# 	b = random.randint(0, len(popt) - 1)
			# 	if b != a:
			# 		break
			# # 随即交配产生后代
			# S1 = copy.deepcopy(popt[a])
			# S2 = copy.deepcopy(popt[b])
			# Sx = crossOver(S1, S2)
			# Sx2 = copy.deepcopy(popt[0])
			# r = random.random()
			# if r < Pls:
			# 	Sls = localSearch(Sx)
			# 	Sls2 = localSearch(Sx2)
			# 	# print("Sls", Sls)
			# 	if Sls not in popt:
			# 		popt.append(Sls)
			# 		print(1, calculate(Sls))
			# 	if Sls2 not in popt:
			# 		popt.append(Sls2)
			# 		print(1, calculate(Sls2))
			# 	elif Sx not in popt:
			# 		popt.append(Sx)
			# 		print(2, calculate(Sx))
			# elif Sx not in popt:
			# 	popt.append(Sx)
			# 	print(3, calculate(Sx))
			# popt = sorted(popt, key=functools.cmp_to_key(compare))
			# print("min", calculate(popt[0]))


			# a = random.randint(0, len(popt) - 1)
			# while True:
			# 	b = random.randint(0, len(popt) - 1)
			# 	if b != a:
			# 		break
			# # 随即交配产生后代
			# S1 = copy.deepcopy(popt[a])
			# S2 = copy.deepcopy(popt[b])
			# Sx = crossOver(S1, S2)
			# r = random.random()
			# if r < Pls:
			# 	Sls = localSearch(Sx)
			# 	# print("Sls", Sls)
			# 	if Sls not in popt:
			# 		popt.append(Sls)
			# 		print(1,calculate(Sls))
			# 	elif Sx not in popt:
			# 		popt.append(Sx)
			# 		print(2,calculate(Sx))
			# elif Sx not in popt:
			# 	popt.append(Sx)
			# 	print(3,calculate(Sx))
			# popt = sorted(popt, key=functools.cmp_to_key(compare))
			# print("min",calculate(popt[0]))


			if counter//2 == 0:
				a = random.randint(0, len(popt) - 1)
				while True:
					b = random.randint(0, len(popt) - 1)
					if b != a:
						break
				# 随即交配产生后代
				S1 = copy.deepcopy(popt[a])
				S2 = copy.deepcopy(popt[b])
			else:
				S1 = copy.deepcopy(popt[0])
				S2 = copy.deepcopy(popt[1])

			Sx = crossOver(S1, S2)
			check(Sx,"corssover")
			Sx2 = copy.deepcopy(popt[0])

			r = random.random()
			if r < Pls:
				Sls = localSearch(Sx)
				Sls2 = localSearch(Sx2)

				# print("Sls", Sls)
				if Sls not in popt:
					popt.append(Sls)
					# print(1,calculate(Sls))
				if Sls2 not in popt:
					popt.append(Sls2)
					# print(1, calculate(Sls2))
				elif Sx not in popt:
					popt.append(Sx)
					# print(2, calculate(Sx))
			elif Sx not in popt:
				popt.append(Sx)
				# print(3,calculate(Sx))
			popt = sorted(popt, key=functools.cmp_to_key(compare))
			# print("min",calculate(popt[0]))


			#选取最优局部搜索 不产生后代
			# Sx2 = copy.deepcopy(popt[0])
			# Sls2 = localSearch(Sx2)
			# if Sls2 not in popt:
			# 	popt.append(Sls2)
			# 	print(4, calculate(Sls2))
			# popt = sorted(popt, key=functools.cmp_to_key(compare))
			# print("min",calculate(popt[0]))
		circles -= 1
		popt = sorted(popt, key=functools.cmp_to_key(compare))
		pop = popt[:psize]
		time_end = time.time()
	# print("pop:", pop)
	pop = sorted(pop, key=functools.cmp_to_key(compare))

	return pop[0]



def resultFormat(s):
	r = ''
	res = []
	for i in s:
		p = str(0)
		for a, b in i:
			p += (',(' + str(a) + ',' + str(b) + ')')
		p += (',' + str(0))
		res.append(p)
	for q in res:
		r += (q + ',')
	return r[:-1]


if __name__ == '__main__':
	for i in range(23):
		# s = i // 3 + 1
		# t = (i + 1) % 3
		# if i <12:
		# 	file_name = 'egl-e'+str(s)+'-'
		# 	if t == 1:
		# 		file_name+='A'
		# 	if t == 2:
		# 		file_name += 'B'
		# 	if t == 0:
		# 		file_name += 'C'
		# else:
		# 	s = s-4
		# 	file_name = 'egl-s' + str(s) + '-'
		# 	if t == 1:
		# 		file_name += 'A'
		# 	if t == 2:
		# 		file_name += 'B'
		# 	if t == 0:
		# 		file_name += 'C'
		file_name='gdb'+str(i+1)+'.dat'


		if len(sys.argv) == 6:
			file_name = sys.argv[1]
			totaltime = time.time()+int(sys.argv[3])
			seed = int(sys.argv[5])
		else:
			seed = 0.1
			totaltime = time.time()+60
		random.seed(seed)

		lines = open(file_name)
		lines.readline()
		vertices = int(lines.readline().split(':')[1][:-1])
		depot = int(lines.readline().split(':')[1][:-1])
		requiredEdge = int(lines.readline().split(':')[1][:-1])
		nRequiredEdge = int(lines.readline().split(':')[1][:-1])
		vehicles = int(lines.readline().split(':')[1][:-1])
		capacity = int(lines.readline().split(':')[1][:-1])
		totalCost = int(lines.readline().split(':')[1][:-1])

		costs = np.full((vertices + 1, vertices + 1), IFINITY, dtype=int).tolist()
		minCost = np.full((vertices + 1, vertices + 1), IFINITY, dtype=int).tolist()
		allDemands = np.full((vertices + 1, vertices + 1), 0, dtype=int).tolist()

		for i in range(1, vertices + 1):
			costs[i][i] = 0
			minCost[i][i] = 0
		ReadFile(file_name)
		minCost = floyd(minCost)

		s = MEANS(2000,3,50, 0.2)



		cost = calculate(s)

		s = resultFormat(s)
		# print("s", s)
		print(file_name)
		print("q", cost)