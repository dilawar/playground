/*
 * =====================================================================================
 *
 *       Filename:  read_file.cc
 *
 *    Description: See the header file. 
 *
 *        Version:  1.0
 *        Created:  Sunday 08 August 2010 12:26:21  IST
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

#include  <vector>
#include	<cmath>
#include	<string>
#include	<stdio.h>
#include	<stdlib.h>
#include	<cstdlib>
#include	<string.h>
#include	<iostream>
#include	"./../include/read_file.h"


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  ReadFile
 *  Description:  Constructor of this class
 * =====================================================================================
 */
ReadFile::ReadFile()
{	
#ifdef  DEBUG
	std::cout<<"\nReadFile Class: Entering Constructor...\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  ~ReadFile
 *  Description:  Destructor
 * =====================================================================================
 */
ReadFile::~ReadFile()
{
#ifdef  DEBUG
	std::cout<<"\nReadFile Class: Entering destructor...\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  setFilePointer
 *  Description:  Set the class private member FILE* equal to the given arg.
 * =====================================================================================
 */
void ReadFile::setFilePointer(std::string myFile)
{
	
#ifdef  DEBUG
	std::cout<<"\nFuntion ReadFile::setFilePointer ...\n";
	std::cout<<"\nPassed argument is:"<<myFile<<"\t"<<myFile.c_str()<<"\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	//ReadFile::myFileStream.open(myFile.c_str());
	fp = fopen(myFile.c_str(), "r+");
	std::cout<<"AD";
	if(NULL != fp)
	{

#ifdef  DEBUG
		std::cout<<"\nWe have successfully opened the file... \n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	}
	else
	{
		std::cout<<"\nFATAL ERROR : Can not open the file. Either file is missing"
						 <<"\nor I do not have enough privileges to open this file. This"
						 <<"\nis really embarrassing.\n";
		exit(EXIT_FAILURE);
	}
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  checkFileForErrors(FILE* pMyFile)
 *  Description:  this function will check the file for format errors. If error
 *  found, application will exit. It will continue with warnings. See
 *  README_FILE_FORMAT for more details.
 * =====================================================================================
 */
int ReadFile::checkFileForErrors()
{

#ifdef  DEBUG
	std::cout<<"\nInside ReadFile::checkFileForErrors ... \n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	//unsigned int lineNum = 1;
	//unsigned int countNum = 0;
	//std::vector<int> pairOfInt;
	//char myLine[100];
	char ch;
	char aChar[10];
	int numNext= 0;
	int size = 0;
	if(NULL != fp)
	{
#ifdef  DEBUG
		std::cout<<"\n\tFile is open...\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
		while(( ch = getc(fp)) != EOF)
		{
#ifdef  DEBUG
			std::cout<<"\tch is: "<<ch;
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
			if(isdigit(ch))
			{
				numNext++;
				{
					aChar[numNext-1] = ch;
			//	std::cout<<"aChar :"<<aChar[numNext-1];
			//	printf("%c and %d", aChar[numNext-1],aChar[numNext-1]); 
			//	vecOfPairs.push_back(ch - 48);
				
				}
			//printf("NumNext: %d", numNext);
			}
			else{
			//printf("\nEntering else loop..\n");
				int p = 0;
				for(int i =1; i <= numNext; i++)
				{
					p = p + (aChar[i-1]-48)*pow(10, numNext-i);
				}
				if( p != 0) // Avoid non-digit zero being pushed into vector.
				{
					vecOfPairs.push_back(p);
				}
				numNext = 0;
			}
		}
			
		if(size % 2 != 0)
		{
			std::cout<<""
				<<"Note :"
				<<"\n\tIn given input file. One or more pair are not complete. I recommend"
				<<"\n\tthat you check your file. I am ignoring this pair and continuing...\n";
		}	
	
#if 0	
				for(unsigned int i = 0; i < strlen(myLine); i++)
				{	
						std::cout<<"AA";
					if(isdigit(myLine[i]))
					{
						std::cout<<"AA";
							vecOfPairs.push_back(myLine[i] - 48);
						  std::cout<<"Push at "<<i<<": num "<<myLine[i]-48;
					   	countNum++;
					}
				}
				if(2 != countNum)
				{
					std::cerr<<"\nError is input file.\n";
					return EXIT_FAILURE;
				}
				vecOfPairs.push_back(pairOfInt[0]);
				vecOfPairs.push_back(pairOfInt[1]);
				lineNum++;
			}
		}
		// Remove last two entries from the vector.
		vecOfPairs.erase(vecOfPairs.end());
		vecOfPairs.erase(vecOfPairs.end());
#endif
		fclose(fp);
  	return EXIT_SUCCESS;
	}
	else
	{
		std::cerr<<"\n\tFile is not open...\n";
		return EXIT_FAILURE;
	}
}

#if 0
/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  checkLine
 *  Description:  utility to check if the line read from a file is OK!
 * =====================================================================================
 */
std::vector<int> ReadFile::checkLine(std::string thisLine, int lineNum)
{
	
#ifdef  DEBUG1
	std::cout<<"\nInside ReadFile::checkLine...\n"<<thisLine<<"and number is "<<lineNum;
#endif     /* -----  not DEBUG  ----- */
  unsigned int i = 0;
	unsigned int countNum = 0;
	bool ifComment = false;
	std::vector<int> pairInt;
#if 0
	//before making is #if 1, change the thisLine to myLine is function args.
	char* thisLine;
	thisLine = new char[myLine.size()+1];
	strcpy(thisLine, myLine.c_str());
#endif
	for(i = 0; i <= thisLine.length(); i++)
	{
		//std::cout<<"thisLine[0]"<<thisLine[0];
#ifdef  DEBUG1
			std::cout<<"\nValues found.\n";	
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
#if 0	
			if(isspace(thisLine[i]) == true /*|| thisLine[i] == '\t'*/)
			{
				i++;
			}
#endif
				if(isdigit(thisLine[i]))
				{
					countNum++;
					pairInt.push_back(thisLine[i] - 48);	
#ifdef  DEBUG1
				std::cout<<"\nValue is: "<<thisLine[i];
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
			}
		}
	if(countNum != 2 &&  countNum != 0)
	{
		std::cout<<"\nError in input file at line: "<<lineNum;
		exit(EXIT_FAILURE);
	}
	return pairInt;
}
#endif

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  copyFileIntoVector
 *  Description:  see header file
 * =====================================================================================
 */
void ReadFile::copyFileIntoAVector()
{
	
#ifdef  DEBUG1
	std::cout<<"\nInside ReadFile::copyFileIntoAVector ...\n"; 
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	if(NULL != fp)
	{
		if(EXIT_SUCCESS == checkFileForErrors())
		{
#ifdef  DEBUG
			std::cout<<"\n\tData in Vec is :\n";
			for(std::vector<unsigned long int>::size_type i = 0; i < vecOfPairs.size(); i++)
			{
				std::cout<<"\t"<<vecOfPairs[i];
			}
			std::cout<<'\n';
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
		}
	}
	else
	{
		std::cout<<"\n\tI am sorry. It must have not happened. I am messed up!"
		 <<"\n\tContact dilawar@ee.iitb.ac.in \n";
	}
}



/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  copyVecToVec
 *  Description:  Interface to other object
 * =====================================================================================
 */
std::vector<int> ReadFile::copyVecToVec()
{
	std::vector<int> thisVec;
	for(std::vector<int>::size_type i = 0; i < vecOfPairs.size(); i++)
	{
		thisVec.push_back(vecOfPairs[i]);
	}
	return thisVec;
}
