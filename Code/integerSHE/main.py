import sys
import random as rand
from math import log, ceil

from helper_functions import *
from scheme import Scheme

def send_message_ecc(scheme, message, n = 3):
    candidates = []
    size = len(message) * 7
    for i in range(n):
        scheme.key_gen()
        if i == 0:
            m, m_int = scheme.encrypt_full(message)
            print(bin(m_int)[2:])
        else:
            m, m_int = scheme.encrypt_full(m_int)

        decrypted, bits_dec = scheme.decrypt_full(m)
        pad = size - ceil(log(bits_dec,2))
        #print(pad*'0' + bin(bits_dec)[2:].replace('1',' '))
        candidates.append(bits_dec) 
    message_majority = 0
    for i in range(size):
        vote = sum([(c & (1 << i)) >> i for c in candidates]) / n
        if vote >= .5:
            message_majority += 1 << i
    prop_preserved = bin(m_int ^ (~message_majority & ((1 << size) - 1))).count('1') / size
    return message_majority, prop_preserved



#Constants for one particular scheme
c1 = 10
c2 = 10
lam = 2
gam = c2*lam**3
rho = lam 
rho_prime = 2*rho
tau = gam + lam

# >= rho * Theta[lam*log^2(lam)]
order_of_nu = rho*lam*(log(lam,2)**2)
nu  = c1*lam

# Initialize scheme with given parameters
scheme = Scheme(lam, gam, nu, rho, rho_prime, tau)

if __name__ == '__main__':
    if sys.argv[1] == 'm':
        m = " ".join(sys.argv[2:])
        ans, preserved = send_message_ecc(scheme, m, n = 1)
        print(bin(ans)[2:], preserved)
