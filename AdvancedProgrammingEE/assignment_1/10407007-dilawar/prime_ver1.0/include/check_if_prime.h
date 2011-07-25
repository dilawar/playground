/*
 * =====================================================================================
 *
 *       Filename:  check_if_prime.h
 *
 *    Description:  Header file.
 *
 *        Version:  1.0
 *        Created:  Wednesday 04 August 2010 05:15:03  IST
 *       Revision:  none
 *       Compiler:  g++/gcc 
 *
 *         Author:  Dilawar (nuts), dilawar[AT]ee[dot]iitb[dot]ac[dot]in
 *      Institute:  Indian Institute of Technology, Bombay
 *
 * This material is released under GNU Lesser Public License.	
 * You are free to copy, distribute or use it for any non-commercial activity.
 * But you are not allowed to modify it. If you are a student, you can use its
 * part in your work with or without mentioning it.
 * 
 * For additional details, please see the GNU Lesser Public license.
 *
 * NOTE : No propriety software is used in this material.
 * Almost all of the code is written and modified in VIM editor with c-support 
 * plugin which is more awesome than Kung Fu Panda. Just kidding, no one is more
 * awesome than Kung Fu Panda with or without a light saber.
 * 
 * This program is made using a bit for here,  a bit from there under the influence
 *  of a lot of burnt out neurons.
 * Report bugs : dilawar.in@gmail.com
 * =====================================================================================
 */

#ifndef  _check_if_prime_h__INC
#define  _check_if_prime_h__INC

#include	"stats_algo.h"
#include	<vector>
/*
 * =====================================================================================
 *        Class:  PrimeNumber
 *  Description:  Check whether a given number is prime or not.
 * =====================================================================================
 */
class PrimeNumber
{
	private:
				/* ========================== DATA MEMBER ======================================*/

		unsigned long long int num;
		std::vector<unsigned long int> vecFactors;
		bool ifPrime;
		std::vector<int> vecRandomNumber;
		
	public:
		/* ====================  LIFECYCLE     ======================================= */
		PrimeNumber ();                             /* constructor */
	 
		virtual ~PrimeNumber(); 										/* Destructor */ 
		CollectStats* pObjCollectStats;
		/* ======= Functions to get and set private member =============================*/
		bool getIfPrime();
		std::vector<unsigned long int> getFactors();
		unsigned long long int getNumber();
		bool setNumber(unsigned long long int);
		/* 
		 * ===  FUNCTION  ======================================================================
		 *         Name:  algorithmFirst
		 *  Description:  Divide number by 2, 3, floor(root(number)). If remainder is zero.
		 *  Number is composite else prime.
		 * =====================================================================================
		 */
		void algorithmFirst(void);


		/* 
		 * ===  FUNCTION  ======================================================================
		 *         Name:  algorithmSecond
		 *  Description:  Divide number by 2, 3, 6k+1 where k < floor(root(number)).
		 *  If remainder is zero, number is composite else prime. Bingo! 
		 * =====================================================================================
		 */
		void algorithmSecond(void);


		/* 
		 * ===  FUNCTION  ======================================================================
		 *         Name:  testAlgorithmsWithRamdomData
		 *  Description:  This will test the algorithm with random numbers.
		 *  @args : Random number vector.
		 *  @args : algorithm
		 *  @ret  : void	
		 * =====================================================================================
		 */
		void testAlgorithmsWithRamdomData(std::vector<int>* pArrayNumber, void* pAlgorithm);

		
}; /* -----  end of class PrimeNumber  ----- */


#endif   /* ----- #ifndef _check_if_prime_h__INC  ----- */

