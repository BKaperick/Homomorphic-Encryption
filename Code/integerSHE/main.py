import sys
import random as rand
from math import log, ceil

from helper_functions import *
from scheme import Scheme


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
