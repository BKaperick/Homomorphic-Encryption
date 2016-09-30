#include <time.h>
#include <stdlib.h>
#include <inttypes.h>
#include <stdbool.h>
#include <stdio.h>
//#include "linkedlist.h"

#define LAMBDA 5
#define GAMMA 5
#define NU 5
#define RHO 5
#define TAU 5


uint64_t randOfSize(uint64_t size) {
	time_t t;
	srand((unsigned) time(&t));
	return rand() % (1 << size);
}

int64_t randOfSizeSigned(uint64_t size) {
	if (1 << size > RAND_MAX)
		printf("%" PRId64 " larger than RAND_MAX (%d)\n", 1 << size, RAND_MAX);
	time_t t;
	srand((unsigned) time(&t));
	bool sign = rand() & 1;
	int64_t randval = rand() % (1 << size);
        if (sign)
		return randval;
	return -1*randval;
}

int64_t distrSpecial(uint64_t lenPK, uint64_t lenNoise, uint64_t sk) {
	uint64_t q = randOfSize(lenPK) / sk;
	int64_t r = randOfSizeSigned(lenNoise);
	return sk*q + r;
}

void insert(int64_t* array, int64_t* elem, int64_t index, int64_t* length) {
	for (int j = *length; j > index; j--) {
		array[j] = array[j-1];
	}
	array[index] = *elem;
	length++;
}

void keyGen(uint64_t secParam, uint64_t lenPK, uint64_t lenSK, uint64_t lenNoise, uint64_t intsPK, uint64_t* sk, int64_t* pk) {	
	*sk = randOfSize(lenSK);
	//int64_t pk[GAMMA];
	pk[0] = 2;
	int64_t currLen = 0;
	while (pk[0] % 2 == 0 || (pk[0] % *sk) % 2 == 1) {
		currLen = 0;	
		for (uint64_t ind = 0; ind < intsPK; ind++) {
			int64_t x = distrSpecial(lenPK, lenNoise, *sk);
			if (currLen == 0 || x <= pk[0]) {
				currLen++;
				pk[currLen] = x;
			}
			else
				insert(pk, &x, 0, &currLen);			
		}
	}
}	

int main() {
	//uint64_t params[5] = {5,5,5,5,5};
	uint64_t secParam = LAMBDA; 
	uint64_t lenPK    = GAMMA; 
	uint64_t lenSK    = NU;
	uint64_t lenNoise = RHO;
	uint64_t intsPK   = TAU;	
	int64_t pk[GAMMA];
	uint64_t* sk = (uint64_t *) malloc(8);
	keyGen(secParam, lenPK, lenSK, lenNoise, intsPK, sk, pk);
	}


