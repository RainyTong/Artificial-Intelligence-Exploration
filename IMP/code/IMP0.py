import numpy as np
import sys
import random
import math
from functools import reduce
import operator
import time

### ------------global------------ ###
# parameters passed:
network_file_path = ''
k = 0
model_type = ''
time_budget = 0

# after processing:
network_file_list = []
n = 0  ### nodes number
m = 0  ### edges number

graph = []
nbr_dict = {}
reverse_nbr_dict = {}


### ------------global------------ ###


def init():
    global network_file_path
    global k
    global model_type
    global time_budget

    global network_file_list
    global n
    global m
    global graph
    global nbr_dict
    global reverse_nbr_dict

    global sample_time

    network_file_path = sys.argv[2]
    k = int(sys.argv[4])
    model_type = sys.argv[6]
    time_budget = sys.argv[8]

    network_file_list = open(network_file_path).readlines()

    n = int(network_file_list[0].split()[0])
    m = int(network_file_list[0].split()[1])

    ### build the graph:
    graph = np.zeros((n + 1, n + 1), dtype=np.float)

    ### build the neighbor dict
    for i in range(1, m + 1):
        v1 = int(network_file_list[i].split()[0])
        v2 = int(network_file_list[i].split()[1])
        graph[v1][v2] = float(network_file_list[i].split()[2])

        if v1 not in nbr_dict:
            nbr_dict[v1] = [v2]
        else:
            nbr_dict[v1].append(v2)

        if v2 not in reverse_nbr_dict:
            reverse_nbr_dict[v2] = [v1]
        else:
            reverse_nbr_dict[v2].append(v1)


def comb(n, k):
    return reduce(operator.mul, range(n - k + 1, n + 1)) / reduce(operator.mul, range(1, k + 1))


def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)

    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item


def F_R(S_i, R):

    count = 0.0

    if S_i is None:
        return count
    for i in range(len(R)):
        ### condider R[i]

        for seed in S_i:

            if seed in R[i]:

                count += 1
                break
    # return a fraction number: |RR| / |R|

    return (count / len(R))


def generateRR_IC(v):
    RR = []

    ActivitySet = [v]

    while (len(ActivitySet) != 0):
        newActivitySet = []
        for seed in ActivitySet:
            if seed not in reverse_nbr_dict:
                continue
            for neighbor in reverse_nbr_dict[seed]:
                if neighbor not in RR:
                    probability = graph[neighbor][seed]
                    state = random_pick([1, 0], [probability, 1 - probability])
                    if state == 1:
                        RR.append(neighbor)
                        newActivitySet.append(neighbor)
        ActivitySet = newActivitySet

    return RR


def generateRR_LT(v):
    RR = []

    ActivitySet = [v]

    while (len(ActivitySet) != 0):
        newActivitySet = []
        for seed in ActivitySet:
            other_probability = 1
            pick_list = []
            probability_list = []

            if seed not in reverse_nbr_dict:
                continue
            for neighbor in reverse_nbr_dict[seed]:
                if neighbor not in RR:
                    pick_list.append(neighbor)
                    probability_list.append(graph[neighbor][seed])
                    other_probability -= graph[neighbor][seed]
            pick_list.append(-1)
            probability_list.append(other_probability)
            select_neighbor = random_pick(pick_list, probability_list)

            if select_neighbor != -1:
                RR.append(select_neighbor)
                newActivitySet.append(select_neighbor)
            else:
                return RR
        ActivitySet = newActivitySet

    return RR


def Sampling(e0, l):

    R = []
    LB = 1

    e = e0 * (2 ** 0.5)


    for i in range(1, int(math.log(n, 2))):
        x = n / pow(2, i)

        lmd1 = ((2 + (2.0 / 3.0) * e) * (math.log(comb(n, k)) + l * math.log(n) + math.log(math.log(n, 2))) * n) / pow(e, 2)
        sita_i = lmd1 / x

        while (len(R) <= sita_i):
            v = random.randint(1, n)
            RR = []
            if model_type == 'IC':
                RR = generateRR_IC(v)
            elif model_type == 'LT':
                RR = generateRR_LT(v)
            if len(RR) != 0:
                R.append(RR)

        start = time.time()

        S_i = NodeSelection(R, k)
        print("nodeselection:", time.time()-start,"len R:",len(R))

        _F_R = F_R(S_i, R)

        if (n * _F_R) >= ((1 + e) * x):
            LB = n * _F_R / (1 + e)
            break

    a = (l * math.log(n) + math.log(2)) ** 0.5
    b = ((1 - math.exp(-1)) * (math.log(comb(n, k)) + l * math.log(n) + math.log(2))) ** 0.5
    lmd2 = 200 * n * np.square((1 - math.exp(-1)) * a + b)
    sita = lmd2 / LB



    while (len(R) <= sita):
        v = random.randint(1, n)
        if model_type == 'IC':
            RR = generateRR_IC(v)
        elif model_type == 'LT':
            RR = generateRR_LT(v)
        R.append(RR)

    return R


def NodeSelection(R, k):
    S_k = []
    v_set = set()

    for i in R:
        for j in i:
            v_set.add(j)

    for i in range(k):
        max = -1
        max_v = 0

        for v in v_set:
            S1 = []
            for s in S_k:
                S1.append(s)
            S1.append(v)
            S2 = S_k
            marginal_gain = F_R(S1, R) - F_R(S2, R)
            if marginal_gain > max:
                max = marginal_gain
                max_v = v

        S_k.append(max_v)

        v_set.remove(max_v)

    return S_k


def main():

    init()

    l = 1 + math.log(2) / math.log(n)  #### l = 1

    start = time.time()
    R = Sampling(0.1, l)  #### ipsilon = 0.1

    print("Sampling:",time.time()-start)

    start = time.time()
    S_k = NodeSelection(R, k)
    print("Node Selecting:", time.time() - start,"len R:",len(R))

    for s in S_k:
        print(s)
   


if __name__ == '__main__':
    main()
