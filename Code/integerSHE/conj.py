# Testing conjecture that for a,b,x,y in Z s.t. b modx mody = 0, then (a+b)modx mody = a modx mody
from helper_functions import *
import random as rand
a = rand.randint(1,100)
x = rand.randint(1,100)
y = rand.randint(1,100)
b = rand.randint(1,10)*x + rand.randint(1,10)*y

def f(a,b,x,y):
    val1 = rmod(y, rmod(x, a+b)) 
    val2 = rmod(y, rmod(x, a))
    return val1 == val2

maxval = 15
with open('out.txt','w') as file_a:
    for a in range(1,maxval):
        for c in range(1,maxval // 5):
            for d in range(1,maxval // 5):
                for x in range(maxval):
                    b = c*x + d*y
                    file_a.write(str(a) + ' ' + str(b) + ' ' + str(x) + ' ' + str(f(a,b,x,2)))
