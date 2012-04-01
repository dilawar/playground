/*
 * =====================================================================================
 *
 *       Filename:  main.cc
 *
 *    Description:  Assignment 01 : check primality of a given number.
 *
 *        Version:  1.0
 *        Created:  Wednesday 04 August 2010 03:59:26  IST
 *       Revision:  none
 *       Compiler:  g++/gcc 
 *
 *         Author:  Dilawar (nuts), dilawar[AT]ee[dot]iitb[dot]ac[dot]in
 *      Institute:  Indian Institute of Technology, Bombay
 *
 * Released under GNU Lesser Public License.	You are free to copy, distribute
 * or use it for any non-commercial activity. But you are not allowed to
 * modified it (at least ethically). Please see the GNU Lesser Public license 
 * for more details.
 *
 * NOTE : No propriety software is used in this material.
 * Almost all of the code is written in VIM editor with c-support plugin which is
 * more awesome than Kung Fu Panda. 
 * This program is made using a bit for here,  a bit from there under, and few
 * references under the influence of a lot of burnt out neurons.
 * Report bugs : dilawar.in@gmail.com
 * =====================================================================================
 */

#include  <iostream> 
#include	<string>
#include  <getopt.h>
#include  <stdlib.h>
#include	<error.h>
#include	<stdio.h>

#include	"check_if_prime.h"
#define FALSE 				0
#define TRUE 					1

int main ( int argc, char **argv )
{
#if DEBUG
	std::cout<<"Entering the main()\n";
	std::cout<<"\nNo of args are: "<<argc;
#endif
	/* Here, we parse our argument passed to this application from command line*/
	if(argc < 2)
	{
		std::cout<<"\nOh Snap!"
			<<"\nWassup, Fellow Human.."
			<<"\nAt least, you need to specify algorithm name. Use --help to see your options.\n";
	 	return EXIT_FAILURE;
	}
  int c;	
  unsigned long long int number;
	int do_help = 0;
 	int do_verbose = 0;
 	bool ifInvalid = FALSE;	/* flag variables. */  
	std::string algo;
	std::vector<unsigned long int> prime_factors;
	while(1)
	{
		int option_index = 0;
		static struct option long_options[] = {
			{"number", 		required_argument, 		NULL, 		'n'},
			{"help", 			no_argument, 		 			&do_help, 	1},
			{"verbose", 	no_argument, 				 	&do_verbose, 1},
			{"algorithm", required_argument, 		NULL, 		 'a'},
			{0, 0, 0 , 0}
		};

		c = getopt_long(argc, argv, "hvn:a:", long_options, &option_index);
		if (c == -1)
			break;

		switch(c) {
			
			case 'n' :
#if DEBUG
				std::cout<<"\nFrom main() - Option --number with value '"
					<<optarg<<"'\n";
				if( 0 > atoll(optarg))
				{
					std::cout<<"\n Number is negative. Converting it into positive and continuing..."
					 <<"\nI am using unsigned integer so that I can handle larger numbers...\n";
					number = 0 - atoll(optarg);
				}
#endif
				number = atoll(optarg);
				break;

			case 'a':
#if DEBUG
				std::cout<<"\nFrom main() - Option --algorithm with value '"
					<<optarg<<"'\n";
#endif
				algo = optarg;
				break;

			
			case 0:
#ifdef DEBUG
				std::cout<<"\noption "<<long_options[option_index].name;
				if (optarg)
					std::cout<<"with arg "<<optarg;
				//std::cout<<"Bad option. x-(\n";
#endif
				break;

			case 'v':
			  do_verbose = 1;
#ifdef  DEBUG
				std::cout<<"\nFrom main() : Verbose output is set.\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
				break;
			
			case 'h':
				do_help = 1;
				break;

			case ':': /* missing option arguement. */
				fprintf(stderr, " option %s requires an argument. \n",
						argv[1]);
				ifInvalid = TRUE;
			 	break;

			case '?':

			default:
				fprintf(stderr, "option %s is invalid : ignored\n",
						argv[1]);
				ifInvalid = TRUE;
				break;
		}

	}

	/* We got the options. Do the stuff. */
	if(TRUE == ifInvalid || 1 == do_help)
	{
		std::cout<<"\n-------------------------------------------------------";
		std::cout<<"\nUSAGE :";
		std::cout<<"\n\t --number <number>" 
			<<"\n\t\t provide the number to be checked for primarily."
		  <<"\n\t\t If you DO NOT specify a number, I'll use a big garbage value."
		  <<"\n\t\t which you may not like!"
			<<"\n\t --help"
			<<"\n\t\t to see the help. Should be used alone."
			<<"\n\t --algorithm <name_algo> (a or b or c)"
			<<"\n\t\t name the algorithm name. See README file for more details."
			<<"\n\t\t available options are a, b, and c. THIS OPTION IS MUST"
			<<"\n\t --verbose"
			<<"\n\t\t for verbose output.";
		std::cout<<"\n-------------------------------------------------------\n";
		return EXIT_FAILURE;
	}

#ifdef DEBUG
	std::cout<<"Number is :" <<number<<"\t\n";
#endif
	if(0 == number )
	{
		std::cout<<"Number is either zero or you are trying to give me some crap. Screw you guys, I am going home.\n";
		return EXIT_FAILURE;
	}
	if( 0 > number)
	{
		std::cout<<"Number is negative. We are converting it into a positive. Wouldn't matter to me. This message is FYI.\n";
		number = 0 - number;
	}

	PrimeNumber* pObjPrimeNumber = new PrimeNumber;
	pObjPrimeNumber->setNumber(number);
	std::cout<<"Number is :"<<pObjPrimeNumber->getNumber();
//	std::cout<<"Test number is"<<pObjPrimeNumber->pObjCollectStats->test<<"\n";
	if(algo == "a")
	{
			
#ifdef  DEBUG
		std::cout<<"\nIf verbose set :"<<do_verbose;
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
		
		if(1 == do_verbose)
		{
				std::cout<<""
					<<"\n============================================================================"
					<<"\nABOUT THIS ALGORITHM:"
					<<"\n\tThis algorithm checks the primality by dividing the number by all possible" 
					<<"\n\tintegers from 2 to floor(sqrt(num)). If there is any factor, number is NOT"
				  <<"\n\tprime, else number is prime. I DO NOT PRODUCE ALL OF THE FACTORS"
					<<"\n============================================================================";
		}
		pObjPrimeNumber->algorithmFirst();
		pObjPrimeNumber->getFactors();

		return EXIT_SUCCESS;
		
	}
	else if(algo == "b")
	{

#ifdef  DEBUG
		std::cout<<"\n Algorithm b is specified.\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
		if( 1 == do_verbose)
		{
			std::cout<<""
				<<"\n=================================================================================="
				<<"\nABOUT THIS ALGORITHM:"
				<<"\n\tThis algorithm divide the number by 2, 3, n where n is 6k+1 < floor[root(num)]" 
				<<"\n\twhere k takes the values 1, 2, 3, etc... If there any factor, number is composite"
  			<<"\n\telse PRIME. I DO NOT PRODUCE ALL OF THE FACTORS."
			 	<<"\n==================================================================================\n";
		}
		pObjPrimeNumber->algorithmSecond();
		pObjPrimeNumber->getFactors();

		return EXIT_SUCCESS;
	}
	else if(algo == "c")
	{
		std::cout<<"\nWe still have not implemented this algorithm. May be you can help us.\n";
		return EXIT_SUCCESS;
	}

	else
	{
		std::cout<<"\n==========\n SOS :"
						 <<"\nI am not cool enough to support your algorithm. Keep it real with two algorithm a and"
						 <<"\nb. Use them or make your own and let me know.!!\n";
		return EXIT_FAILURE;
	}
}				/* ----------  end of function main  ---------- */
