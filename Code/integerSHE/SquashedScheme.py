import random as rand
from helper_functions import *

class SquashedScheme(Scheme):
    def __init__(self, lam, gam, nu, rho, rho_prime, tau, ):
        super().__init__(lam, gam, nu, rho, rho_prime, tau)
        self.Theta = Theta
        self.theta = theta
        self.kappa = kappa
    
    def key_gen(self):
        super().key_gen()
        xp = q(self.sk, 2**self.kappa)
        s = array_of_hamming_weight(self.Theta, self.theta)
        S = [i for i in range(len(s)) if s[i] == 1]
        while (not u) or sum([u[i] for i in S]) != rmod(2**(self.kappa+1), xp):
            u = [rand_of_size(self.kappa+1) for i in range(self.Theta)]

        y = [u[i]/(2**self.kappa) for i in range(self.Theta)]

        self.sk = s
        self.pk = (self.pk, y)

    def encrypt(self, message):
        c = super().encrypt(message)
        y = self.pk[1]
        z = [rmod(2, c*y[i]) for i in range(self.Theta)]
        n = ceil(log(self.theta, 2)) + 3
        #Here truncate all except n most significant non-integer bits of each element of z.
        return (c, z)

    def decrypt(self, c):
        c_star, z = c
        s = self.pk[1]
        interior = c - sum([x[0]*x[1] for x in zip(z,s)])
        return rmod(2, interior)

    

