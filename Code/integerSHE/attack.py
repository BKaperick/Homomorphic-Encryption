from scheme import *
from helper_functions import *

import random as rand

class Attack():
    def __init__(self, scheme, advantage):
        self.scheme = scheme
        self.eps = advantage
    
    def key_gen(self):
        self.pk = [2]
        while self.pk[0] % 2 == 0:
            self.pk = []
            for i in range(self.scheme.intsPK+1):
                x = self.scheme._dist_special()
                #x[0] must be maximum
                if len(self.pk) == 0 or x <= self.pk[0]:
                    self.pk.append(x)
                else:
                    self.pk.insert(0,x)

    def predict(self, pk, c):
        pk_preserved    = self.scheme.pk
        self.scheme.pk  = self.pk
        plaintext_guess = self.scheme.decrypt(c)
        self.scheme.pk  = pk_preserved
        return plaintext_guess
   
    # Output: best guess for q(scheme.sk,z)
    def learn_LSB(self, z):
        scheme = self.scheme
        print(z) 
        Bs = []
        #max_iter = int(rand.randint(40,50)*scheme.secPar**rand.randint(0,5) // self.eps)
        max_iter = 50
        for j in range(max_iter):
            r = rand_of_size(scheme.lenNoise_secondary, signed=True)
            m = rand.getrandbits(1)
            S_size = rand.randrange(1, scheme.intsPK+1)
            S = rand_subset1(scheme.intsPK, size = S_size)
            r = rand_of_size(scheme.lenNoise_secondary, signed=True)
            val = z + m + 2*r + 2*sum([self.pk[i] for i in S])
            c = rmod(self.pk[0], val)
            a = self.predict(self.pk, c)
            b = a ^ (z%2) ^ m
            Bs.append(b)
        return int(Bs.count(1) >= Bs.count(0))

    def binary_GCD(self, a, b):
        if a == 0:
            return a
        elif a < b:
            a,b = b,a
        elif a % 2 == b % 2 == 0:
            return 2*self.binary_GCD(a/2, b/2)
        elif a % 2 == b % 2 == 1:
            new_a = (a - b) / 2
            return self.binary_GCD(new_a, b)
        elif a % 2 == 1:
            return self.binary_GCD(a, b/2)
        elif b % 2 == 1: # else
            return self.binary_GCD(a/2, b)
         
