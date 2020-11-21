# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 19:18:23 2019

@author: ANKIT
"""

import random
import matplotlib.pyplot as plt
def generate_state():
    pos = [0]
    
    for i in range(n):
        pos.append(random.randint(1,n))
        
    return pos

def calc_fitness(pos):
    #check in same row
    fit = 0 
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            if pos[i] == pos[j]:
                fit = fit + 1
        
    # now check for diagonal
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            if abs(i-j) == abs(pos[i]-pos[j]):
                fit = fit + 1

    return fit        

def sort_fitness():
    for i in range(len(fitness)):
        
        min_index = i
        for j in range(i+1,len(fitness)):
            if fitness[min_index] > fitness[j]:
                min_index = j
        fitness_order.append(min_index)
        fitness[i], fitness[min_index] = fitness[min_index], fitness[i]


def do_crossover():
    p1 = random.randint(0,80)
    p2 = random.randint(0,80)
    cp = random.randint(1,7)
    parent1_index = fitness_order[p1]
    parent2_index = fitness_order[p2]
    
    for j in range(1,cp+1):
        c1.append(parents[parent1_index][j])
        
    for k in range(cp+1,n+1):
        c1.append(parents[parent2_index][k])
        
    for j in range(1,cp+1):
        c2.append(parents[parent2_index][j])
        
    for k in range(cp+1,n+1):
        c2.append(parents[parent1_index][k])

def do_mutation():
    i = random.randint(0,1)
    if i == 1:
        j = random.randint(1,n)
        k = random.randint(1,n)
        c1[j] = k
    
    i = random.randint(0,1)
    if i == 1:
        j = random.randint(1,n)
        k = random.randint(1,n)
        c2[j] = k

print("Enter the value of n") 
n = input()   
n = int(n,10)   
count = 0  
parents = [] 
fitness = []
fitness_order = []    
x_cor = [] 
y_cor = []
children_fitness= []
#generating the initial positions of queens in each column
for x in range(100):
    pos = generate_state()
    parents.append(pos)

#calculating the fitness value of each of the chromosome    
for i in range(100):
    fitness.append(calc_fitness(parents[i]))

sort_fitness()    
while 1 == 1:
    
    children = []
    children_fitness = []
    count = count + 1
    x_cor.append(count)
     
    for i in range(50):
        flag = 0
        c1 = [0]
        c2 = [0]
        do_crossover()
        c1_fit = calc_fitness(c1)
        if c1_fit == 0 or count == 10000:
            child = 1
            flag = 1
            break
        
        c2_fit = calc_fitness(c2)
        if c2_fit == 0 or count == 10000:
            child = 2
            flag = 1
            break
        
        do_mutation()
                  
        c1_fit = calc_fitness(c1)
        if c1_fit == 0 or count == 10000:
            child = 1
            flag = 1
            break
                
        c2_fit = calc_fitness(c2)
        if c2_fit == 0 or count == 10000:
            child = 2
            flag = 1
            break
        children_fitness.append(c1_fit)
        children_fitness.append(c2_fit)   
        children.append(c1)
        children.append(c2)
    
    if flag == 1:
        break
    y_cor.append(min(children_fitness))

    fitness = []
    fitness_order = [] 
    parents = []
    parents.extend(children)
    for i in parents:
        fitness.append(calc_fitness(i))
    
    sort_fitness()  

if count == 10000:
    print("solution not found")

elif child == 1:
    children_fitness.append(c1_fit)
    for i in range(1,n+1):
        print(f"{c1[i]} ", end =" ")
    print()
    print(f"Generation = {count}")
    y_cor.append(min(children_fitness))
    plt.plot(x_cor, y_cor) 
    plt.xlabel('Generation no.')
    plt.ylabel('fitness value') 
    plt.show()

else:
    children_fitness.append(c2_fit)
    for i in range(1,n+1):
        print(f"{c2[i]} ", end =" ")
    print()
    print(f"Generation = {count}")
    y_cor.append(min(children_fitness))
    plt.plot(x_cor, y_cor) 
    plt.xlabel('Generation no.')
    plt.ylabel('fitness value') 
    plt.show()
    