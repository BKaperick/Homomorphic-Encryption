#include <stdlib.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>

#define LAMBDA 5
#define GAMMA 5
#define NU 5
#define RHO 5
#define TAU 5


int main() {
	uint64_t params[5] = {5,5,5,5,5};
	uint64_t secParam = LAMBDA; 
	//uint64_t lenPK    = GAMMA; 
	uint64_t lenSK    = NU;
	uint64_t lenNoise = RHO;
	uint64_t intsPK   = TAU;	
	}
uint64_t randOfSize(uint64_t *size) {
	time_t t;
	srand((unsigned) time(&t));
	return rand(2** (*size));
}

uint64_t *keyGen(uint64_t *secParam, uint64_t *lenPK, uint64_t *lenSK, uint64_t *lenNoise, uint64_T intsPK) {	
	sk = randOfSize(lenSK);
	uint64_t pk[GAMMA];
	pk[0] = 2;
	


