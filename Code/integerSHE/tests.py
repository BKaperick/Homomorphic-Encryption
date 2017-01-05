import unittest
from main import *
from helper_functions import *

class TestScheme(unittest.TestCase):
    
    def setUp(self):
        
        #Constants for one particular scheme
        lam = 1
        gam = 1
        rho = 1
        rho_prime = 1
        tau = 1 
        nu  = 1

        # Initialize scheme with given parameters
        self.scheme = Scheme(lam, gam, nu, rho, rho_prime, tau)
        self.scheme.key_gen()

    def test_mod(self):
        p = 5
        qs = [2,2,2,3,3,3,3,3,4]
        rs = [0,1,2,-2,-1,0,1,2,-2]
        
        for i,z in enumerate(range(10,19)):
            self.assertEqual(q(p,z), qs[i])
            self.assertEqual(rmod(p,z), rs[i])
        
        p = 2
        qs = [0,1,1,2,2]
        rs = [0,-1,0,-1,0]
        for i,z in enumerate(range(0,5)):
            self.assertEqual(q(p,z), qs[i])
            self.assertEqual(rmod(p,z), rs[i])
        

    def test_keygen(self):
        scheme = self.scheme
        self.assertEqual(scheme.pk[0] % 2, 1)
        self.assertEqual(rmod(scheme.sk, scheme.pk[0]) % 2, 0)
        self.assertEqual(max(scheme.pk), scheme.pk[0])
        self.assertTrue((1 << (scheme.lenSK - 1)) <= scheme.sk < (1 << scheme.lenSK))
        self.assertEqual(scheme.sk % 2, 1)

if __name__ == '__main__':
    unittest.main()
