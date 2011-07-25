/*
 * =====================================================================================
 *
 *       Filename:  generate_file.cc
 *
 *    Description:  Create a txt file which can be read by graphviz.
 *
 *        Version:  1.0
 *        Created:  Sunday 08 August 2010 01:23:42  IST
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


#include	"./../include/generate_file.h"
#include	<stdio.h>
#include	<iostream>
#include	<vector>
#include	<stdlib.h>

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  GenerateFile
 *  Description:  constructor
 * =====================================================================================
 */
GenerateFile::GenerateFile()
{
#ifdef  DEBUG
	printf("\nGenerarateFile:: Entering the default constructor...\n");
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
}
/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  ~GenerateFile
 *  Description:  destructor
 * =====================================================================================
 */
GenerateFile::~GenerateFile()
{
#ifdef  DEBUG
	printf("\n~GenerateFile destructor...\n");
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	//delete pObjReadFile;
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  generateVecOfNodes
 *  Description:  see header file
 * =====================================================================================
 */

int GenerateFile::generateVecOfNodes(std::vector<int> myVec)
{
	vecPairs = myVec; // set this for further manipulation
#ifdef  DEBUG1
	printf("\nGenerarateFile::generateVecOfNodes() ... \n");
#endif     /* -----  not DEBUG  ----- */
	char indexVector[myVec.size()];
	//std::vector<int>::size_type j =0;
	indexVector[0] = myVec[0];
	myVec.erase(myVec.begin());
	int n = 1;
	int count = 0;
	while(0 < myVec.size())
	{
		for(int i = 0; i < n; i++)
		{
			if(myVec[0] != indexVector[i]){
				//std::cout<<"\tv0:"<<myVec[0];
				count++;
			}
		}
		//std::cout<<"\ncount :"<<count;
		if(count == n)
		{
			//std::cout<<"\nYes\t";
			indexVector[n] = myVec[0];
			myVec.erase(myVec.begin());
			count = 0;
			n++;
		}
 		else{
			count = 0;
			myVec.erase(myVec.begin());
		}

	}
	for(int i = 0; i < n; i++)
	{
		vecOfNodes.push_back(indexVector[i]);
	}

#if DEBUG1
	for(int i = 0; i < n; i++)
	{
		printf("vec[%d] : %d", i, indexVector[i]);
	}
#endif     /* -----  not DEBUG  ----- */
	//vecOfNodes = indexVector;
	return EXIT_SUCCESS;
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  drawQuickFindGraph
 *  Description:  quick find implementation with dot tool interface.
 * =====================================================================================
 */
void GenerateFile::drawQuickFGraph( void)
{
	vecQuickFind = vecOfNodes;

	int i = 9;
}
