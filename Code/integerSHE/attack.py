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
        plaintext_guess = 0
        return plaintext_guess
   
    # Output: best guess for q(scheme.sk,z)
    def learn_LSB(self, z):
        scheme = self.scheme
        
        Bs = []
        max_iter = rand.randint(1,10)*scheme.secParam**rand.randint(0,5) // self.eps
        for j in range(max_iter):
            r = rand_of_size(scheme.lenNoise_secondary, signed=True)
            m = rand.getrandbit()
            S_size = rand.randrange(1, scheme.intsPK+1)
            S = rand_subset1(scheme.intsPK, size = S_size)
            r = rand_of_size(scheme.lenNoise_secondary, signed=True)
            val = z + m + 2*r + 2*sum([self.pk[i] for i in S])
            c = rmod(self.pk[0], val)
            a = self.predict(self.pk, c)
            b = a ^ (z%2) ^ m
            Bs.append(b)
        return int(Bs.count(1) >= Bs.count(0))

    def approx_GCD(self):
        pass

