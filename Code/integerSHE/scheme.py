import random as rand
from math import log, ceil
from helper_functions import *

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
        while self.pk[0] % 2 == 0 or rmod(self.sk, self.pk[0]) % 2 == 1:
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
        val = m + 2*r + 2*sum([self.pk[i] for i in S])
        c = rmod(self.pk[0], val)
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
        #print(bin(message)[2:]) 
        # Each 7-bit chunk in message is a letter.
        
        # Encrypts message bit by bit
        message_enc = []
        size = ceil(log(message, 2))
        for i in range(0, size):
            m = (message & (1 << i)) >> i
            c = self.encrypt(m)
            message_enc.append(c)
        
        return message_enc, message

    def evaluate(self, C, Cin):
        return C(Cin)

    def decrypt(self, c):
        return -1*rmod(2, rmod(self.sk, c))

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
        #print(pad*'0' + bin(message)[2:]) 
        return message_out, message
    
    # Random int
    def _dist_special(self):
        q = rand_of_size(self.lenPK) // self.sk
        r = rand_of_size(self.lenNoise, signed=True)
        return self.sk*q + r

