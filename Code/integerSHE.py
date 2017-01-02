import sys
import random as rand
from math import log

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
    mask = 1 << size
    return val | mask


#the quotient between p and z rounded to the nearest integer
def q(p,z):
    return (z+.5) // p

class Scheme:
    def __init__(self, lam, gam, nu, rho, tau):
        # Security parameter
        self.secPar = lam
        # Length of public encr. key
        self.lenPK = gam
        # Length of secret encr. key
        self.lenSK = nu
        # rho parameter
        self.lenNoise = rho
        self.intsPK = tau 

    def key_gen(self):

        # Secret key is:
        #  * an odd integer
        #  * of lenSK bits
        self.sk = rand_of_exact_size(self.lenSK) 
        if self.sk % 2 == 0:
            self.sk += 1

        self.pk = [2]
        while self.pk[0] % 2 == 0 or (self.pk[0] % self.sk) % 2 == 1:
            self.pk = []
            for i in range(self.intsPK+1):
                x = self._dist_special()
                if len(self.pk) == 0 or x <= self.pk[0]:
                    self.pk.append(x)
                else:
                    self.pk.insert(0,x)

    def encrypt(self, m):
        S = rand_subset1(self.intsPK)
        #r = uniform_sample(range(-2**(2*self.lenNoise)+1, 2**(2*self.lenNoise)))
        r = rand_of_size(self.lenNoise, signed=True)
        c = 0
        for i in S:
            try:
                c += (m + 2*r + 2*self.pk[i]) 
            except IndexError:
                print("Index Error:")
                print(i, len(self.pk))
        c = c % self.pk[0]
        return c

    def evaluate(self, C, Cin):
        return C(Cin)

    def decrypt(self, c):
        return (c % self.sk) % 2
    
    # Random int
    def _dist_special(self):
        q = rand_of_size(self.lenPK) // self.sk
        r = rand_of_size(self.lenNoise, signed=True)
        return self.sk*q + r

def test_scheme(scheme, N = 10):
    score = {'decrypt':0,
             'eval then decrypt':0,
             }
    for n in range(N):
        # Generate public/secret key pair
        scheme.key_gen()

        #encode message
        message = rand.choice([0,1])
        message_enc = scheme.encrypt(message)
        enc_times_2 = scheme.evaluate(lambda x: x*2, message_enc)
        
        dec = scheme.decrypt(message_enc)
        dec_times_2 = scheme.decrypt(enc_times_2)
        score['decrypt'] += int(dec == message)
        score['eval then decrypt'] += int(dec_times_2 == (message*2) % 2)
    score = {k:100*v/N for k,v in score.items()}
    return score

        
#Constants for one particular scheme
c1 = 10
c2 = 10
lam = 2
gam = c2*lam**3 # 80
rho = lam
tau = gam + lam # 82

# >= rho * Theta[lam*log^2(lam)]
order_of_nu = rho*lam*(log(lam,2)**2)
nu  = c1*lam

# Initialize scheme with given parameters
scheme = Scheme(lam, gam, nu, rho, tau)

score = test_scheme(scheme, 1000)

print(score)
