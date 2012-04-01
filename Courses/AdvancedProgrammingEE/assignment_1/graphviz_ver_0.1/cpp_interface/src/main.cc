/*
 * =====================================================================================
 *
 *       Filename:  main.cc
 *
 *    Description:  main file.
 *
 *        Version:  1.0
 *        Created:  Sunday 08 August 2010 12:48:44  IST
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

#include	<iostream>
#include	<getopt.h>
#include	<stdlib.h>
#include	<error.h>
#include	<fstream>
#include	<stdio.h>
#include	<vector>
#include	"./../include/read_file.h"
#include  "./../include/generate_file.h"
int main(int argc, char** argv)
{
	
#ifdef  DEBUG
	std::cout<<"\nEntering the main function...\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	if(argc < 2)
	{
		std::cout<<""
			<<"\nHowdy! Fellow Humans. At least you need to provide me with input file name."
			<<"\nUse --file or -f followed by file_name."
			<<"\n";
		return EXIT_FAILURE;
	}

	int c;
	int do_help;
	bool ifInvalid = false;
	std::string fileName;
	std::vector<int> vecOfPairs;
	std::string inputFilePath;
	std::string outPutFileName;
	while(1)
	{
		int option_index = 0;
		static struct option long_options[] = {
			{"file", 		required_argument,		NULL,			'f'},
			{"help", 		no_argument,					&do_help,	 1},
			{"output", 	required_argument,		NULL,			 'o'},
			{0, 0, 0, 0}
		};

		c = getopt_long(argc, argv, "f:ho:", long_options, &option_index);
		if(c == -1)
			break;

		switch(c) 
		{
			case 'f':
				
#ifdef  DEBUG
				std::cout<<"\nFrom main() : -Option --file with value '"<<optarg<<"'\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
				inputFilePath = optarg;
				break;
			
			case 'h':
				do_help =1;
				break;

			case 0:
				break;

			case 'o':

#ifdef  DEBUG
				std::cout<<"\nFrom main() : Option --output with value ;"<<optarg<<"'\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
				outPutFileName = optarg;
				break;

			case ':':
				fprintf(stderr, "option %s requires an argument.\n",
						argv[1]);
				ifInvalid = true;
				break;

			case '?':
				break;
			
			default:
				fprintf(stderr, "option %s is invalid : ignored\n",
						argv[1]);
						ifInvalid = true;
						break;
		}

		/* we are asked to help this creature, so be it! */
		if(ifInvalid == true || 1 == do_help)
		{
			std::cout<<""
				<<"-------------------------------------------------------------------"
				<<"\nUSAGE : "
				<<"\n\t --file <file_name>"
				<<"\n\t\tName of the file with path which contains the data."
				<<"\n\t --help"
				<<"\n\t\tIf need help, you need to ask. Right?"
				<<"\n\t--output"
				<<"\n\t\tOutput file name. Optional!"
				<<"\n-----------------------------------------------------------------";
			return EXIT_FAILURE;
		}

		/* Now we open the file.*/
	 ReadFile* pObjReadFile = new ReadFile();
	 pObjReadFile->setFilePointer(inputFilePath);
	 pObjReadFile->copyFileIntoAVector();
	 GenerateFile* pObjGenerateFile = new GenerateFile();

	 std::vector<int> vecPairs = pObjReadFile->copyVecToVec();
	 std::cout<<"\nSize"<<vecPairs.size();
	 pObjGenerateFile->generateVecOfNodes(vecPairs);

	return 0;
	}
}

