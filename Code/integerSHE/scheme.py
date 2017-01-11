import random as rand
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
    
    def encrypt_int(self, message): 
        size = byte_length(message) 
        bytes_message = message.to_bytes(size, 'little') 
        return self.encrypt_bytes(bytes_message)
    
    def encrypt_bytes(self, message):
        message_enc = []
        for byte in message:
            val = 0
            for i in range(8):
                m = (byte & (1 << i)) >> i
                c = self.encrypt(m)
                message_enc.append(c)
        return message_enc

    # Input: multi-bit integer or an ascii string
    # Output: list of integers
    def encrypt_string(self, message):
        message_bytes = message.encode()
        message_enc = self.encrypt_bytes(message_bytes)
        return message_enc
    
    # Input: encrypted_bits: a list of encrypted bits 
    #        func: a function of integer addition/multiplication which performs 
    #             analogous binary addition/multiplication on unencrypted bits
    # Output: list of evaluated encrypted bits
    def evaluate(self, encrypted_bits, func):
        return func(encrypted_bits)

    def decrypt(self, c):
        return rmod(self.sk, c) % 2

    # Input list of integers, each element corresponding to an encrypted bit
    # Output bytearray of decrypted message
    def decrypt_bytes(self, message_enc):
        message = 0
        out = bytearray()
        for i,c in enumerate(message_enc):
            m = self.decrypt(c)
            message += m << (i % 8)
            if i % 8 == 7:
                out.append(message)
                message = 0
        
        # str.encode() and int.to_bytes() automatically fill out bits with zeros to be a multiple of 8,
        # but data from scheme.evaluate() will not necessarily.
        if len(message_enc) % 8 != 0:
            out.append(message)
        
        return out
    
    # Input list of integers, each element corresponding to an encrypted bit
    # Output string of decrypted message
    def decrypt_string(self, message_enc):
        message = self.decrypt_bytes(message_enc)
        return message.decode()
    
    # Random int
    def _dist_special(self):
        q = rand_of_size(self.lenPK) // self.sk
        r = rand_of_size(self.lenNoise, signed=True)
        return self.sk*q + r

