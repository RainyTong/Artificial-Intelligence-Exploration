import numpy as np
import sys
import random
import time

# parameters passed:
network_file_path = ""
seedset_file_path = ""
model_type = ""
time_budget = 0

# after processing:
network_file_list = []
seedset_file_list = []
n = 0  ### nodes number
m = 0  ### edges number
graph = []
nbr_dict = {}

# a list of size n+1 to record if the node has been activated. 1 ==> activated, 0 ==>not yet
check_a_list = []


def init():
    global network_file_path
    global seedset_file_path
    global model_type
    global time_budget

    global network_file_list
    global seedset_file_list
    global n
    global m
    global graph
    global nbr_dict

    global check_a_list

    network_file_path = sys.argv[2]
    seedset_file_path = sys.argv[4]
    model_type = sys.argv[6]
    time_budget = sys.argv[8]

    network_file_list = open(network_file_path).readlines()
    seedset_file_list = open(seedset_file_path).readlines()

    n = int(network_file_list[0].split()[0])
    m = int(network_file_list[0].split()[1])

    graph = np.zeros((n + 1, n + 1), dtype=np.float)

    for i in range(1, m + 1):
        v1 = int(network_file_list[i].split()[0])
        v2 = int(network_file_list[i].split()[1])
        graph[v1][v2] = float(network_file_list[i].split()[2])

        if v1 not in nbr_dict:
            nbr_dict[v1] = [v2]
        else:
            nbr_dict[v1].append(v2)


    ## seedset_file_list (seedset):
    for i in range(len(seedset_file_list)):
        seedset_file_list[i] = int(seedset_file_list[i])

    ## check_a_list:
    check_a_list = np.zeros(n + 1, dtype=np.int)
    for seed in seedset_file_list:
        check_a_list[seed] = 1

def ISE(N, model_type):
    sum = 0.0

    if model_type == "IC":
        for i in range(N):

            oneSample = one_IC_Sample()
            sum += oneSample

    elif model_type == "LT":
        for i in range(N):
            oneSample = one_LT_Sample()
            sum += oneSample
    return sum / N



def one_IC_Sample():

    ActivitySet = []
    check_a_list_copy = []
    for c in check_a_list:
        check_a_list_copy.append(c)

    ### initialize ActivitySet <== SeedSet
    for seed in seedset_file_list:
        ActivitySet.append(seed)

    count = len(ActivitySet)


    while (len(ActivitySet) != 0):

        newActivitySet = []

        for seed in ActivitySet:

            if seed not in nbr_dict:
                continue
            for neighbor in nbr_dict[seed]:
                if check_a_list_copy[neighbor] != 1:
                    probability = graph[seed][neighbor]
                    state = random_pick([1, 0], [probability, 1 - probability])
                    if state == 1:
                        check_a_list_copy[neighbor] = 1
                        newActivitySet.append(neighbor)

        count += len(newActivitySet)

        ActivitySet = []
        for new in newActivitySet:
            ActivitySet.append(new)

    return count

def one_LT_Sample():

    ActivitySet = []
    threshold_list = np.zeros(n + 1, dtype=np.float)

    check_a_list_copy = []
    for c in check_a_list:
        check_a_list_copy.append(c)

    ### initialize ActivitySet <== SeedSet
    for seed in seedset_file_list:
        ActivitySet.append(seed)

    ### initialize threshold_list:
    for i in range(1, len(threshold_list)):
        threshold_list[i] = random.random()
        if threshold_list[i] == 0:
            ActivitySet.append(i)

    count = len(ActivitySet)

    while (len(ActivitySet) != 0):
        newActivitySet = []
        for seed in ActivitySet:
            if seed not in nbr_dict:
                continue
            for neighbor in nbr_dict[seed]:
                if check_a_list_copy[neighbor] != 1:
                    w_total = 0
                    for father_node in range(1, n + 1):
                        if graph[father_node][neighbor] != 0 and check_a_list_copy[father_node] == 1:
                            w_total += graph[father_node][neighbor]
                    if w_total >= threshold_list[neighbor]:
                        check_a_list_copy[neighbor] = 1
                        newActivitySet.append(neighbor)
        count += len(newActivitySet)
        ActivitySet = []
        for new in newActivitySet:
            ActivitySet.append(new)
    return count

def random_pick(some_list, probabilities):
    x = random.uniform(0, 1)

    cumulative_probability = 0.0
    for item, item_probability in zip(some_list, probabilities):
        cumulative_probability += item_probability
        if x < cumulative_probability: break
    return item




def main():
    start_time = time.time()

    init()

    ISE_res = ISE(10000, model_type)

    print(round(ISE_res,2))

    # print("runtime:", time.time() - start_time)



if __name__ == '__main__':
    main()
