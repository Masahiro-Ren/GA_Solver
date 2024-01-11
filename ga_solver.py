import numpy as np
import random as rand
from itertools import combinations
# find the proper a, b, c, d of f(x) = (a + 2b + 3c + 4d) - 30

def func(a, b, c, d) :
    return ((a + 2 * b + 3 * c + 4 * d) - 30)

def Evaluation(Chromosomes) :
    Npop, Ngen = Chromosomes.shape
    Fitness = np.zeros(Npop)
    Total = 0
    for k, chromosome in enumerate(Chromosomes) :
        F_obj = abs(func(chromosome[0], chromosome[1], chromosome[2], chromosome[3]))
        f = 1.0 / ( 1 + F_obj )
        # Calculate Fitness and Total for the next step.
        Total += f
        Fitness[k] = f
    
    print("F_obj : ", F_obj)
    print("Fitness : ", Fitness)

    return Fitness, Total

def Selection(Chromosomes, Fitness, Total) :
    Npop, Ngen = Chromosomes.shape
    P = np.zeros(Npop)
    C = np.zeros(Npop)

    NewChromosomes = np.array(Chromosomes)

    for k, f in enumerate(Fitness) :
        P[k] = f / Total
    
    C[0] = P[0]
    for i in range(1, Npop) :
        C[i] = P[i] + C[i - 1]
    
    # print("P : ", P)
    # print("C : ", C)

    for k in  range(0, Npop) :
        kk = 0
        R = rand.random()
        print("R{0} : {1}".format(k, R))
        while kk < Npop  and R >= C[kk] :
            kk += 1
        if(kk == Npop) :
            kk = 0  
        for j in range(0, Ngen) :
            NewChromosomes[k][j] = Chromosomes[kk][j]
    
    # Swap 2 array
    NewChromosomes, Chromosomes = Chromosomes, NewChromosomes

    for k, chro in enumerate(Chromosomes) :
        print("After shuffle Chromosome {0} : {1}".format(k, chro))
    
def Crossover(Chromosomes, rho_c) :
    Npop, Ngen = Chromosomes.shape
    print("Crossover rate : ", rho_c)

    CrossoverCandi = []

    print("Searching candidates ......")
    while len(CrossoverCandi) < 3 :
        CrossoverCandi.clear()
        for k in range(0, Npop) :
            R = rand.random()
            if(R < rho_c) :
                CrossoverCandi.append(k)

    Combs = list(combinations(CrossoverCandi, 2))

    print("Crossover candidates : ", CrossoverCandi)
    print("Combs : ", Combs)

    for k, comb in enumerate(Combs) :
        l = comb[0]
        r = comb[1]
        print("Crossover {0} and {1}".format(l, r))
        rand_c = rand.randint(0, Ngen - 2) # indicate which postion to start crossover 
        for i in range(0, Ngen) :
            if(i > rand_c) : 
                Chromosomes[l][i] = Chromosomes[r][i]

    for k, chro in enumerate(Chromosomes) :
        print("After crossover Chromosome {0} : {1}".format(k, chro))

def Mutation(Chromosomes, rho_m, Nmute) :
    Npop, Ngen = Chromosomes.shape
    print("Mutation rate : {0}; Mutation Number : {1}".format(rho_m, Nmute))
    for i in range(0, Nmute) :
        rand_pop = rand.randint(0, Npop - 1)
        rand_gen = rand.randint(0, Ngen - 1)
        new_gen_val = rand.randint(0, 30)
        print("Chromosome{0} Gen{1} has been mutated as : {2}".format(rand_pop, rand_gen, new_gen_val))
        Chromosomes[rand_pop][rand_gen] = new_gen_val

    print("After mutation : ", Chromosomes)

def Verify(Chromosomes) :
    innerFLAG = False
    print("Verifying ......") 
    for k, chro in enumerate(Chromosomes) :
        if(func(chro[0], chro[1], chro[2], chro[3]) == 0) :
            innerFLAG = True
            print("Found the best chromosome {0} : {1}".format(k, chro))
            break

    return innerFLAG

def GA_Solver(Chromosomes) :
    Npop, Ngen = Chromosomes.shape
    rho_c = 0.25
    rho_m = 0.1

    Nmute = int(round(Npop * Ngen * rho_m))

    epoch = 1
    flag = False

    while not flag :
        print("================================ Epoch {0} ==================================".format(epoch))
        epoch += 1

        print("---- Step 1. Evaluation ---- ")
        Fitness, Total = Evaluation(Chromosomes)

        print("---- Step 2. Selection ---- ")
        Selection(Chromosomes, Fitness, Total)

        print("---- Step 3. Crossover ---- ")
        Crossover(Chromosomes, rho_c)

        print("---- Step 4. Mutation ---- ")
        Mutation(Chromosomes, rho_m, Nmute)

        print("---- Step 5. Verify ---- ")
        flag = Verify(Chromosomes)

if __name__ == "__main__" :
    Chromosomes = np.array([
        [12, 5, 23, 8],
        [2, 21, 18, 3],
        [10, 4, 13, 14],
        [20, 1, 10, 6], 
        [1, 4, 13, 19], 
        [20, 5, 17, 1]])

    GA_Solver(Chromosomes)

