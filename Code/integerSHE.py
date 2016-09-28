import random as rand


#Returns a sample uniformly chosen from the set space
def uniformSample(space):
	return rand.choice(space)	

#Takes an upper bound and returns a random subset of integers on [1, end] 
def randSubset(end, size = None):
	if size == None:
		size = end / 10
	out = set()
	while len(out) < size:
		out.add(rand.randrange(1,end+1))
	return out

#Generates a random number of at least minsize bits and at most maxsize bits
#The output number is then 2**minsize <= |x| <= -1 + 2**maxsize 
def randOfSize(size, signed=False):
	sgn = 1
	if signed:
		sgn = rand.choice([1,-1])
	return sgn*rand.getrandbits(size)

#the quotient between p and z rounded to the nearest integer
def q(p,z):
	return int( (z+.5)/p)

class Scheme:
	def __init__(self, lam, gam, nu, rho, tau):
		self.secPar = lam
		self.lenPK = gam
		self.lenSK = nu
		self.lenNoise = rho
		self.intsPK = tau

	def keyGen(self):
		#Odd integer, lenSK bits
		self.sk = randOfSize(self.lenSK) 
		self.pk = [2]
		while self.pk[0] % 2 == 0 or (self.pk[0] % self.sk) % 2 == 1:
			self.pk = []
			for i in range(self.intsPK):
				x = self._distSpecial()
				if len(self.pk) == 0 or x <= self.pk[0]:
					self.pk.append(x)
				else:
					self.pk.insert(0,x)
	
	def encrypt(self, m):
		S = randSubset(self.intsPK)
		r = uniformSample(xrange(-2**(2*self.lenNoise)+1, 2**(2*self.lenNoise)))
		c = 0
		for i in S:
			c += (m + 2*r + 2*self.pk[i])
		c = c % self.pk[0]
		return c

	def evaluate(self, C, Cin):
		return C(Cin)

	def decrypt(self, c):
		return (c % self.sk) % 2

	def _distSpecial(self):
		q = randOfSize(self.lenPK) / self.sk
		r = uniformSample(xrange(-2**self.lenNoise, 2**self.lenNoise))
		return self.sk*q + r

		
#Constants for one particular scheme
c1 = 10
c2 = 10
lam = 2
gam = c2*lam**3
nu  = c1*lam
rho = lam
tau = gam + lam

scheme = Scheme(lam, gam, nu, rho, tau)
scheme.keyGen()
m = 1
c = scheme.encrypt(m)
print c
