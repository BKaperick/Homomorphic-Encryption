import random as rand
from math import ceil, log

#Returns a sample uniformly chosen from the set space
def uniform_sample(space):
    return rand.choice(space)    

#Takes an upper bound and returns a random subset of integers on [1, end] 
def rand_subset1(end, size = None):
    if size == None:
        size = end // 10
    
    out = set()
    while len(out) < size:
        out.add(rand.randrange(1,end+1))

    return out

#Takes an upper bound and returns a random subset of integers on [1, end] 
def rand_subset2(end, size = None):
    if size == None:
        size = end // 10
    
    out = set()
    sample = list(range(1, end+1))
    while len(out) < size:
        val = rand.choice(sample)
        out.add(val)
        sample.remove(val)
    
    return out

#Generates a random number of at most size bits
#The output number satisfies 0 <= |x| < 2^size
def rand_of_size(size, signed=False):
    sgn = 1
    if signed:
        sgn = rand.choice([1,-1])
    return sgn*rand.getrandbits(size)

# Returns value such that  2^(size-1) <= x < 2^size
def rand_of_exact_size(size):
    val = rand_of_size(size)
    mask = 1 << (size - 1)
    return val | mask

def bit_length(num):
    return ceil(log(num+1, 2))

def byte_length(num):
    return ceil(log(num+1,2) / 8)

#the quotient between p and z rounded to the nearest integer
def q(p,z):
    #return round(z/p)
    return (2*z+p) // (2*p)

# For the purposes of this paper, r(p,z) == z mod p
def rmod(p,z):
    return z - q(p,z)*p

