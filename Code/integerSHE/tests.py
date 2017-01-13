import unittest
from main import *
from helper_functions import *
from attack import *
import random as rand

class Test(unittest.TestCase):
    
    def setUp(self):
        
        #Constants for one particular scheme
        c1 = 10
        c2 = 10
        lam = 2
        gam = 80
        rho = 2 
        rho_prime = 4
        tau = 82
        nu  = 20

        # Initialize scheme with given parameters
        self.scheme = Scheme(lam, gam, nu, rho, rho_prime, tau)
        self.scheme.key_gen()
        
        # Attack has perfect knowledge
        eps = 1
        self.attack = Attack(self.scheme, eps)
        self.attack.key_gen()

    def test_bit_length(self):
        self.assertEqual(bit_length(7), 3)
        self.assertEqual(bit_length(8), 4)
        self.assertEqual(bit_length(250), 8)
        self.assertEqual(bit_length(256), 9)
        self.assertEqual(bit_length(1), 1)
        self.assertEqual(bit_length(0), 0)

    def test_byte_length(self):
        self.assertEqual(byte_length(255), 1)
        self.assertEqual(byte_length(256), 2)
        self.assertEqual(byte_length(1), 1)
        self.assertEqual(byte_length(0), 0)

    def test_quotient(self):
        p = 5
        self.assertEqual(q(p,10), 2)
        self.assertEqual(q(p,11), 2)
        self.assertEqual(q(p,12), 2)
        self.assertEqual(q(p,13), 3)
        self.assertEqual(q(p,14), 3)
        self.assertEqual(q(p,15), 3)
        self.assertEqual(q(p,16), 3)
        self.assertEqual(q(p,17), 3)
        self.assertEqual(q(p,18), 4)
        
        p = 2
        self.assertEqual(q(p,0), 0)
        self.assertEqual(q(p,1), 0)
        self.assertEqual(q(p,2), 1)
        self.assertEqual(q(p,3), 1)
        self.assertEqual(q(p,4), 2)
        
    def test_rmod(self):
        p = 5
        self.assertEqual(rmod(p,10), 0)
        self.assertEqual(rmod(p,11), 1)
        self.assertEqual(rmod(p,12), 2)
        self.assertEqual(rmod(p,13), -2)
        self.assertEqual(rmod(p,14), -1)
        self.assertEqual(rmod(p,15), 0)
        self.assertEqual(rmod(p,16), 1)
        self.assertEqual(rmod(p,17), 2)
        self.assertEqual(rmod(p,18), -2)
        p = 2
        self.assertEqual(rmod(p,0), 0)
        self.assertEqual(rmod(p,1), 1)
        self.assertEqual(rmod(p,2), 0)
        self.assertEqual(rmod(p,3), 1)
        self.assertEqual(rmod(p,4), 0)
   
    def test_rmod2_equiv(self):
        for i in range(-500,500):
            self.assertEqual(rmod(2,i), i % 2)

    # Given this paper's rmod(p,z), we establish the following conjecture:
    # Let a and b be integers.
    #     If a even and b odd, rmod(2,a) - rmod(2,b) == rmod(2,b-a) == 1
    #     Else, rmod(2,a) - rmod(2,b) == rmod(2,a-b)
    def test_mod_conjecture(self):
        a = rand.randint(0,100)
        b = rand.randint(0,100)
        if a % 2 == 0:
            if b % 2 == 0:
                self.assertEqual(rmod(2, a-b), 0)
                self.assertEqual(rmod(2, a) - rmod(2,b), 0)
            elif b % 2 == 1:
                self.assertEqual(rmod(2, a-b), 1)
                self.assertEqual(rmod(2, a) - rmod(2,b), 1)
        else:
            if b % 2 == 0:
                self.assertEqual(rmod(2, a-b), 1)
                self.assertEqual(rmod(2, a) - rmod(2,b), 1)
            elif b % 2 == 1:
                self.assertEqual(rmod(2, a-b), 0)
                self.assertEqual(rmod(2, a) - rmod(2,b), 0)
    
    def test_keygen(self):
        scheme = self.scheme
        self.assertEqual(scheme.pk[0] % 2, 1)
        self.assertEqual(rmod(scheme.sk, scheme.pk[0]) % 2, 0)
        self.assertEqual(max(scheme.pk), scheme.pk[0])
        self.assertTrue((1 << (scheme.lenSK - 1)) <= scheme.sk < (1 << scheme.lenSK))
        self.assertEqual(scheme.sk % 2, 1)
    
    def test_encrypt_decrypt(self):
        scheme = self.scheme
        self.assertEqual(scheme.decrypt(scheme.encrypt(0)), 0)
        self.assertEqual(scheme.decrypt(scheme.encrypt(1)), 1)
        for i in range(50):
            b = rand.getrandbits(1)
            self.assertEqual(scheme.decrypt(scheme.encrypt(b)), b)


    # Encrypt and decrypt a simple test message.  With these parameters, the chance of
    # information corruption is at most negligible.
    def test_encrypt_decrypt_string(self):
        scheme = self.scheme
        #messages = ["test message", "a", "abc", "big test test test message", "\r"]
        messages = ['\r']
        for message in messages:
            mess_enc = scheme.encrypt_string(message)
            message_out = scheme.decrypt_string(mess_enc)
            self.assertEqual(message, message_out)
    
    def test_encrypt_decrypt_int(self):
        scheme = self.scheme
        message = 15
        mess_enc = scheme.encrypt_int(message)
        message_out = scheme.decrypt_bytes(mess_enc)
        self.assertEqual(len(message_out), 1)
        self.assertEqual(message, message_out[0])
        scheme = self.scheme
        
        message = 200 # 0110 1000
        mess_enc = scheme.encrypt_int(message)
        message_out = scheme.decrypt_bytes(mess_enc)
        self.assertEqual(len(message_out), 1)
        self.assertEqual(message, message_out[0])

        message = 3345 # 0000 1101 0000 1111
        mess_enc = scheme.encrypt_int(message)
        message_out = scheme.decrypt_bytes(mess_enc)
        self.assertEqual(len(message_out), 2)
        self.assertEqual(17, message_out[0])
        self.assertEqual(13, message_out[1])

    # F returns 1 for odd number of 1-bits, 0 for even number    
    def test_evaluate_binary_add(self):
        scheme = self.scheme
        F = lambda x: [sum(x)]
        messages = [13,   # 0000 1101
                    12,   # 0000 1100
                    456,  # 1110 1000
                    458,  # 1110 1010
                    970,  # 0001 1110 1010
                    1994, # 0011 1110 1010
                    ]
        
        for message in messages: 
            encrypted_bits = scheme.encrypt_int(message)
            evaluated_bits = scheme.evaluate(encrypted_bits, F)
            decrypted = scheme.decrypt_bytes(evaluated_bits)
            self.assertEqual(decrypted[0], bin(message).count('1') % 2)
    
    # F returns 1 for 2 least sig bits on, else 0
    def test_evaluate_binary_mult(self):
        scheme = self.scheme
        F = lambda x: [x[0]*x[1]]
        messages = [4,5,6,7,8,]
        for message in messages: 
            encrypted_bits = scheme.encrypt_int(message)
            evaluated_bits = scheme.evaluate(encrypted_bits, F)
            decrypted = scheme.decrypt_bytes(evaluated_bits)
            self.assertEqual(decrypted[0], int(message % 2 == (message & 2) >> 1 == 1))

    '''
    def test_lsb(self):
        messages = [0, 15, 16, 458, 1000, 10000,10001]
        for message in messages:
            bit = self.attack.learn_LSB(message)
            qp = q(self.scheme.sk, message) % 2
            self.assertEqual(bit, qp)
    '''
if __name__ == '__main__':
    unittest.main()
