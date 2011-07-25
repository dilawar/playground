/*
 * =====================================================================================
 *
 *       Filename:  check_if_prime.cc
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  Wednesday 04 August 2010 05:08:57  IST
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

#include	"../include/check_if_prime.h"
#include	"../include/stats_algo.h"

#include	<iostream>
#include	<stdlib.h>
#include	<vector>
#include	<cmath>
/* =============================== Life Cycle * =================================*/
 /* 
	* constructor 
 */
PrimeNumber::PrimeNumber()
{
#ifdef DEBUG
	std::cout<<"\n Class PrimeNumber:: Entering default constructor...";
#endif
	num = 1;
	vecFactors.push_back(1);
	ifPrime = false;
	vecRandomNumber.push_back(1);

	pObjCollectStats = new CollectStats;
	if( NULL == pObjCollectStats)
	{
		std::cout<<"\nBug : Can not create object for class CollectStat..\n";
		exit(0);
	}
}		/* -----  end of method PrimeNumber::PrimeNumber  ----- */

#if 0
/* Second constructor. */
PrimeNumber::PrimeNumber(int n)
{
	
#ifdef  DEBUG
	std::cout<<" \nClass PrimeNumber:: Entering non-default constructor...";
#endif     /* -----  not DEBUG  ----- */
	num = n;
	ifPrime = true;
}		/* -----  end of method PrimeNumber::PrimeNumber  ----- */
#endif

/* Destructor */
PrimeNumber::~PrimeNumber()
{
#ifdef DEBUG
	std::cout<<"\n Entering the destructor ... \n";
#endif     /* -----  not DEBUG  ----- */
}

/* =================== get private data member ======================================*/
bool PrimeNumber::getIfPrime()
{
	bool if_prime = false;
	if(true == ifPrime)
	{
		std::cout<<"\nThe number is prime.\n";
		if_prime = true;
	}
	else
	{
	  std::cout<<"\nThe number is NOT prime.\n";
		if_prime = false;
	}
	return if_prime;
}

/* ============================ get Factors ==========================*/
std::vector<unsigned long int> PrimeNumber::getFactors()
{
 //	std::cout<<"\n====\n Factor of number are...\n";
	std::vector<unsigned long int> vec_factors;
	if(1 >= vecFactors.size())
	{
		std::cout<<"\nNumber is prime. There are no factors.\n";
	}
	else{
		for(std::vector<unsigned long int>::size_type i = 0; i < vecFactors.size(); i++)
		{
			vec_factors.push_back(vecFactors[i]);
		}
		if( vec_factors.size() != vecFactors.size())
		{
			std::cout<<"\nBug : Size of temp vector does not match with the original one."
			 <<"Report this Bug to dilawar.in@gmail.com\n";
		}
		std::cout<<"\n==========\n"
		<<"Factors are :\n";
		for(std::vector<unsigned long int>::size_type i = 0; i < vecFactors.size(); i++)
		{
			std::cout<<"\t"<<vecFactors[i];
		}
		std::cout<<"\n";

	}
	return vec_factors;
}

/* ========================= set the number ===================================*/
bool PrimeNumber::setNumber(unsigned long long int n)
{
	num = n;
	if( 0 > num)
		return EXIT_FAILURE;
	else
		return EXIT_SUCCESS;
}

/* ===================== get the number ======================================*/
unsigned long long int PrimeNumber::getNumber()
{
	unsigned long long int n = num;
	return n;
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  checkNumber
 *  Description:  See header file.
 * =====================================================================================
 */
#if 0
void PrimeNumber::checkNumber (int num )
{

#ifdef  DEBUG
	std::cout<<"\n Entering PrimeNumber::checkNumber function...";
#endif     /* -----  not DEBUG  ----- */
}		/* -----  end of method PrimeNumber::checkNumber  ----- */
#endif

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  algorithmFirst
 *  Description:  see header file
 * =====================================================================================
 */
void PrimeNumber::algorithmFirst(void)
{
	/* Here we calculate the floor value square root of the number. */
	int floor_sqrt = 	floor(sqrt(num));	
#ifdef DEBUG
	std::cout<<"Floor of square root of  num is :" <<floor_sqrt<<"\n";
#endif
	unsigned long long n = num;
	if(n > 3)
	{
		for(int i = 2 ; i <= floor_sqrt; i++)
		{
			if(n % i == 0)
			{
				ifPrime = false;
				n = n / i; // This make sure that we do not keep same factors multiple times.
				vecFactors.push_back(i); // i is a factor. 
			}
			else
				ifPrime = true;
		}
	}
	else
		ifPrime = true;
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  algorithmSecond
 *  Description:  See header file.
 * =====================================================================================
 */
void PrimeNumber::algorithmSecond(void)
{
	int floor_sqrt = floor(sqrt(num));
	
#ifdef  DEBUG
	std::cout<<"\nFloor of square root of num is :"<<floor_sqrt<<"\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */

	unsigned long long n = num;
	int k = 1;
	if(n > 3)
	{
		if( n % 2 == 0)
		{
			ifPrime = false;
			n = n/2;
			vecFactors.push_back(2);
		}
		for(int i = 3; i <= floor_sqrt; i = 6*k + 1)
		{
			if( n % i == 0)
			{
				ifPrime = false;
				n = n/i;
				vecFactors.push_back(i);
				k++;
			}
			else
			{
				ifPrime = true;
				k++;
			}
		}
	}
	else
		ifPrime = true;
}

