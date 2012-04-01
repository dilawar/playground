/*
 * =====================================================================================
 *
 *       Filename:  linear_feedback_shift_register.cc
 *
 *    Description:  Implementation of Linear Feedback Shift Register in C++.
 *    							Clock bit and polynomial which represents which are the bits
 *    							to be xor-ed should be modifiable. These private variables
 *    							can be modified by using public methods given in this
 *    							implementation.
 *
 *        Version:  1.0
 *        Created:  Saturday 14 August 2010 01:17:05  IST
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


#include	"linear_feedback_shift_register.h"
#include	<iostream>
#include	<bitset>
#include	<string>
#include	<cstdlib>

/* Constructor and destructor. */

LFSR::LFSR()
{
	
#ifdef  DEBUG
	std::cout<<"\nLFSR::Entering the Constructor... \n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
}

LFSR::~LFSR()
{

#ifdef  DEBUG
	std::cout<<"\nEntering the destructor ... \n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  setClockBit
 *  Description:  Lets set the clock bit
 * =====================================================================================
 */
bool LFSR::setClockBit(int pos)
{

#ifdef  DEBUG
	std::cout<<"\nSetting clock bit. \n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	posClockBit = pos;
	return EXIT_SUCCESS;
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  getClockBitPos
 *  Description:  get the value of clock bit.
 * =====================================================================================
 */
int LFSR::getClockBitPos()
{

#ifdef  DEBUG
	std::cout<<"\nGetting clock bit pos ... ";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	std::cout<<"\nPosition of clock bit is :"<<posClockBit;
	return posClockBit;
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  getClockBit
 *  Description:  get whether clock bit is high of low.
 * =====================================================================================
 */
bool LFSR::getClockBit()
{

#ifdef  DEBUG
	std::cout<<"\nGetting the value of clock bit ...";
#endif     /* -----  not DEBUG  ----- */
	return myRegister[posClockBit]; 
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  getRegister
 *  Description:  get the register
 * =====================================================================================
 */
std::bitset<SIZE_REGISTER> LFSR::getRegister()
{
	return myRegister;
}
/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  initializeRegister()
 *  Description:  This will initialize the register and put all the bits equal
 *  to zero.
 * =====================================================================================
 */

void LFSR::initializeRegister()
{

#ifdef  DEBUG
	std::cout<<"\n Initializing a register ... \n";
#endif     /* -----  not DEBUG  ----- */

	for(int i = 0; i < SIZE_REGISTER; i++)
	{
		myRegister[i] = 0;
	}
}



/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  setSecretKey
 *  Description:  see the header file.
 * =====================================================================================
 */
void LFSR::setSecretKey(std::bitset<SIZE_SECRET> thisKey)
{
#ifdef  DEBUG
	std::cout << "\nMixing the secret key ... \n";
#endif     /* -----  not DEBUG  ----- */
	for(int i = 0; i < (SIZE_SECRET); i++)
	{
		secretKey[i] = thisKey[i];
		totalKey[i] = thisKey[i];
	}
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  mixSecretiAndPublicKey()
 *  Description:  This will mix the secret key with public key. It also sets the
 *  public key of the class. Any scheme can be implemented. Here, we are augmenting 
 *  one with another.
 * =====================================================================================
 */
void LFSR::mixSecretAndPublicKey(std::bitset<SIZE_PUBLIC> thisKey)
{
#ifdef  DEBUG
	std::cout<<"\nMixing secret and public keys ... \n";
#endif     /* -----  not ->DEBUG  ----- */
	for(int i =0 ; i < SIZE_PUBLIC; i++)
	{
		totalKey[SIZE_SECRET + i] = thisKey[i];
		publicKey[i] = thisKey[i];
	}
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  mixKey
 *  Description:  mix public and secret key to make a key. In this
 *  implementation we are just augmenting. A sophisticated approach is
 *  desirable.
 * =====================================================================================
 */
void LFSR::mixKey()
{
#ifdef  DEBUG
	std::cout << "\nMixing the secret key with the register.";
#endif     /* -----  not DEBUG  ----- */
	for(int i = 0; i < SIZE_REGISTER; i++)
	{
		myRegister[i] = totalKey[i];
	}
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  setPoly
 *  Description:  This will set the polynomial coefficient.
 * =====================================================================================
 */
void LFSR::setPoly()
{
#ifdef  DEBUG
	std::cout<<"\n Setting the polynomial coefficients ...\n";
#endif     /* -----  not DEBUG  ----- */
	int n; // number of the coeffcient;
	std::cout<<"\nEnter the number of the coefficients: ";
	std::cin >> n;
	for(int i = 0; i < n; i++)
	{
		int num;
		std::cout<<"\nEnter the "<<i+1<<" coefficient :";
		std::cin >> num;
		coeffPoly.push_back(num);
	}
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  majorityChecking
 *  Description:  see the header file.
 * =====================================================================================
 */
int LFSR::majorityChecking()
{

#ifdef  DEBUG
	std::cout<<"\nGetting majority ... ";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */

	return 0;
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  updateRegister
 *  Description:  see the header file.
 * =====================================================================================
 */

void LFSR::updateRegister()
{
#ifdef  DEBUG
	std::cout<<"\nUpdating the register .. \n";
#else      /* -----  not DEBUG  ----- */

#endif /* -----  not DEBUG  ----- */
	bool bit = myRegister[coeffPoly[0]];
	for(int i = 0; i < 100; i++)
	{
		/* xor the location given by  poly */
		for(unsigned int i = 1; i < coeffPoly.size(); i++)
		{
			bit = bit ^ myRegister[coeffPoly[i]];
		}
		/* shift everything one step left . */
		myRegister <<= 1;
		myRegister[0] = bit;
	}
}	
