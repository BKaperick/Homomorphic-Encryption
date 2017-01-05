import java.util.*;
public class integerSHE {
    public static void main() {
    }
    public static class Scheme {
	    private int secParam, lenPK, lenSK, lenNoise, intsPK;
	    int sk, pk;
	    public static void main(int lam, int gam, int nu, int rho, int tau) {
		secParam = lam; 
		lenPK = gam;
		lenSK = nu;
		lenNoise = rho;
		intsPK = tau;
	    }

	    public static void keyGen() {
		sk = randOfSize(lenSK);
		pk = ArrayList<Long>();
		pk.add(2);

	    }
    }
    
    public static long randOfSize(int size) {
        long out = 5;
        return out;	
    }

}

