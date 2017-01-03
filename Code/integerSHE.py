import sys
import random as rand
from math import log, ceil

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


#the quotient between p and z rounded to the nearest integer
def q(p,z):
    return (2*z+p) // (2*p)

def r(p,z):
    return z - q(p,z)

class Scheme:
    def __init__(self, lam, gam, nu, rho, rho_prime, tau):
        # Security parameter
        self.secPar = lam
        # Length of public encr. key
        self.lenPK = gam
        # Length of secret encr. key
        self.lenSK = nu
        # rho parameter
        self.lenNoise = rho
        self.lenNoise_secondary = rho_prime
        self.intsPK = tau 

    def key_gen(self):

        # Secret key is:
        #  * an odd integer
        #  * of lenSK bits
        self.sk = rand_of_exact_size(self.lenSK) 
        if self.sk % 2 == 0:
            self.sk += 1

        self.pk = [2]
        while self.pk[0] % 2 == 0 or r(self.sk, self.pk[0]) % 2 == 1:
            self.pk = []
            for i in range(self.intsPK+1):
                x = self._dist_special()
                #x[0] must be maximum
                if len(self.pk) == 0 or x <= self.pk[0]:
                    self.pk.append(x)
                else:
                    self.pk.insert(0,x)
    
    def encrypt(self, m):
        S_size = rand.randrange(1, self.intsPK+1)
        S = rand_subset1(self.intsPK, size = S_size)
        r = rand_of_size(self.lenNoise_secondary, signed=True)
        c = (m + 2*r + 2*sum([self.pk[i] for i in S])) % self.pk[0]
        return c
   
    # Input: multi-bit integer or an ascii string
    # Output: list of integers, the encrypted bits
    def encrypt_full(self, message):
        
        # Converts ASCII string to integer
        if type(message) == str:
            mess = 0
            for i,c in enumerate(message[::-1]):
               mess += ord(c) << i*7
            message = mess
        print(bin(message)[2:]) 
        # Each 7-bit chunk in message is a letter.
        
        message.encode()

        # Encrypts message bit by bit
        message_enc = []
        size = ceil(log(message, 2))
        for i in range(0, size):
            m = (message & (1 << i)) >> i
            c = self.encrypt(m)
            message_enc.append(c)
        
        return message_enc

    def evaluate(self, C, Cin):
        return C(Cin)

    def decrypt(self, c):
        return (c % self.sk) % 2

    def decrypt_full(self, message_enc):
        message = 0
        #print(len(message_enc))
        for i,c in enumerate(message_enc):
            m = self.decrypt(c)
            message += (m << i)
        bits = ceil(log(message, 2))
        pad = len(message_enc) - bits
        chars = bits // 7
        message_out = ''
        for i in range(chars):
            # 7-bit mask
            mask = 0x7F << (7*i)
            val = (mask & message) >> (7*i)
            message_out += chr(val)
        print(pad*'0' + bin(message)[2:]) 
        return message_out
    
    # Random int
    def _dist_special(self):
        q = rand_of_size(self.lenPK) // self.sk
        r = rand_of_size(self.lenNoise, signed=True)
        return self.sk*q + r

def test_scheme(scheme, N = 10):
    score = {'validate':0,
             'decrypt':0,
             'eval then decrypt':0,
             'e vs e&d':0,
             }
    
    # Generate public/secret key pair
    scheme.key_gen()
    
    for n in range(N):
            
        # Validate Keys
        check = [
                scheme.pk[0] % 2 == 1,
                r(scheme.sk, scheme.pk[0]) % 2 == 0,
                max(scheme.pk) == scheme.pk[0],
                (1 << (scheme.lenSK - 1)) <= scheme.sk < (1 << scheme.lenSK),
                scheme.sk % 2 == 1,
                ]
        score['validate'] += int(all(check))

        # Encode message
        message = rand.choice([0,1])

        message_enc = scheme.encrypt(message)
        enc_times_2 = scheme.evaluate(lambda x: x*2, message_enc)
        
        dec = scheme.decrypt(message_enc)
        dec_times_2 = scheme.decrypt(enc_times_2)
        score['decrypt'] += int(dec == message)
        #score['eval then decrypt'] += int(dec_times_2 == (message*2) % 2)
        #score['e vs e&d'] += int(dec == dec_times_2)
    score = {k:100*v/N for k,v in score.items()}
    return score

        
#Constants for one particular scheme
c1 = 10
c2 = 10
lam = 8
gam = c2*lam**3 # 80
rho = 1
rho_prime = rho
tau = gam + lam # 82

# >= rho * Theta[lam*log^2(lam)]
order_of_nu = rho*lam*(log(lam,2)**2)
nu  = c1*lam

# Initialize scheme with given parameters
scheme = Scheme(lam, gam, nu, rho, rho_prime, tau)

if __name__ == '__main__':
    if sys.argv[1] == 't':
        order = ['validate', 'decrypt']
        score = test_scheme(scheme, 100)
        [print(k,score[k]) for k in order]
    elif sys.argv[1] == 'm':
        scheme.key_gen()
        m = " ".join(sys.argv[2:])
        m_enc = scheme.encrypt_full(m)
        m_dec = scheme.decrypt_full(m_enc)
        print('"' + m_dec + '"')
