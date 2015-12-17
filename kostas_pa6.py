#include <iostream>
#include <string>
#include <gmp.h>

class Factorization {
	public:
	mpz_t N;
	mpz_t p;
	mpz_t q;
};

Factorization *challenge1(const char *NStr) {
	Factorization *factorization = new Factorization();
	
	mpz_t x, A;
	
	mpz_init(factorization->N);
	mpz_set_str(factorization->N, NStr, 10); 

	mpz_init(A);
	mpz_sqrt(A, factorization->N);

	mpz_init(x);

	int result = 0;
	
	// In the first challenge, a single iteration is needed
	while(result == 0)
	{
  		// x = sqrt(N - A^2)
		mpz_mul(x, A, A);
		mpz_sub(x, x, factorization->N);

		result = mpz_perfect_square_p(x);
		if (result == 0)
		{
			mpz_add_ui(A, A, 1);
		}
	}
	
	mpz_sqrt(x, x);
	std::string xStr(mpz_get_str(NULL, 10, x));
	std::cout << "x: " << xStr << "\n";

	mpz_init(factorization->p);
	mpz_set_ui(factorization->p, 0);  
	mpz_sub(factorization->p, A, x);
	
	mpz_init(factorization->q);
	mpz_set_ui(factorization->q, 0);  
	mpz_add(factorization->q, A, x);

	mpz_mul(factorization->N, factorization->p, factorization->q);

	std::string pStr(mpz_get_str(NULL, 10, factorization->p));
	std::string qStr(mpz_get_str(NULL, 10, factorization->q));
	std::string pqStr(mpz_get_str(NULL, 10, factorization->N));
	std::cout << "\n" << pStr << "\n" << qStr << "\n" << pqStr << "\n";

	mpz_clear(A);
	mpz_clear(x);

	return factorization;
}

void challenge3(const char *NStr) {
	mpz_t N, p, q, temp, sqrt6N, A;
	
	mpz_init(N);
	mpz_set_str(N, NStr, 10); 

	// A = 3p + 2q = 2*sqrt(6N)
	// Ap = 3p^2 + 2N => p = (A - sqrt(A^2 - 24N))/6
	mpz_init(sqrt6N);
	mpz_mul_ui(sqrt6N, N, 6);
	mpz_sqrt(sqrt6N, sqrt6N);
	mpz_mul_ui(sqrt6N, sqrt6N, 2);

	mpz_init(A); 
	mpz_init(p);
	mpz_init(temp);
	int result = 0, x = 0;
	
	while(result == 0)
	{
		mpz_add_ui(A, sqrt6N, x);
  
		mpz_mul(p, A, A);
	
		mpz_mul_ui(temp, N, 24);
	
		mpz_sub(p, p, temp);

		result = mpz_perfect_square_p(p);
		
		if (result != 0) break;
		x++;
	}
	
	mpz_sqrt(p, p);
	mpz_sub(p, A, p);
	mpz_div_ui(p, p, 6);
	
	mpz_init(q);
	mpz_div(q, N, p);

	mpz_mul(N, p, q);

	std::string pStr(mpz_get_str(NULL, 10, p));
	std::string qStr(mpz_get_str(NULL, 10, q));
	std::string pqStr(mpz_get_str(NULL, 10, N));
	std::cout << "\n" << pStr << "\n" << qStr << "\n" << pqStr << "\n";

	mpz_clear(N);
	mpz_clear(sqrt6N);
	mpz_clear(A);
	mpz_clear(temp);
	mpz_clear(p);
	mpz_clear(q);
}

void challenge4(mpz_t N, mpz_t p, mpz_t q, const char* cipherStr)
{
	mpz_t cipher, e, d, phiN, m;
	
	mpz_init(cipher);
	mpz_set_str(cipher, cipherStr, 10); 

	mpz_init(d);
	mpz_init(e);
	mpz_init(phiN);
	mpz_init(m);
	
	mpz_set_ui(e, 65537);
	
	mpz_add_ui(phiN, N, 1);
	mpz_sub(phiN, phiN, p);
	mpz_sub(phiN, phiN, q);
	
	int result = mpz_invert(d, e, phiN);
	if (result != 0)
	{
		mpz_powm(m, cipher, d, N);
		std::string mStr(mpz_get_str(NULL, 16, m));
		std::cout << mStr << "\n";
		
		std::size_t found = mStr.find("00");
		std::cout << found << "\n";
		if (found!=std::string::npos)
		{
			std::string mHex = mStr.substr(found + 2);
			std::cout << mHex << "\n";
			
			int len = mHex.length();
			std::string text;
			for(int i=0; i< len; i+=2)
			{
				std::string byte = mHex.substr(i,2);
				char chr = (char) (int)strtol(byte.c_str(), 0, 16);
				text.push_back(chr);
			}
			std::cout << text << "\n";
		}
	}
	else 
	{
		std::cout << "Error!\n";
	}

	mpz_clear(N);
	mpz_clear(p);
	mpz_clear(q);
	
	mpz_clear(cipher);
	mpz_clear(d);
	mpz_clear(e);
	mpz_clear(phiN);
	mpz_clear(m);
}

int main (void)
{
	const char *N1Str =
	
"17976931348623159077293051907890247336179769789423065727343008115 \
77326758055056206869853794492129829595855013875371640157101398586 \
47833778606925583497541085196591615128057575940752635007475935288 \
71082364994994077189561705436114947486504671101510156394068052754 \
0071584560878577663743040086340742855278549092581";
	
	const char *N2Str = 
	
	"6484558428080716696628242653467722787263437207069762630604390703787 \
9730861808111646271401527606141756919558732184025452065542490671989 \
2428844841839353281972988531310511738648965962582821502504990264452 \
1008852816733037111422964210278402893076574586452336833570778346897 \
15838646088239640236866252211790085787877";

	const char *N3Str =
	
"72006226374735042527956443552558373833808445147399984182665305798191 \
63556901883377904234086641876639384851752649940178970835240791356868 \
77441155132015188279331812309091996246361896836573643119174094961348 \
52463970788523879939683923036467667022162701835329944324119217381272 \
9276147530748597302192751375739387929";

	const char *cipherStr = 
	"22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540";


	std::cout << "Challenge 1\n\n";
	Factorization *factorization1 = challenge1(N1Str);

	std::cout << "\n\nChallenge 2\n\n";
	Factorization *factorization2 = challenge1(N2Str);

	std::cout << "\n\nChallenge 3\n\n";
	challenge3(N3Str);
	
	std::cout << "\n\nChallenge 4\n\n";
	challenge4(factorization1->N,
	           factorization1->p,
	           factorization1->q,
	           cipherStr);
	
	delete(factorization1);
	delete(factorization2);
	
  	return 0;
}

