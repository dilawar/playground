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
#include	<cstdlib>
#include	<math.h>
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
 *         Name:  setFileName
 *  Description:  set the file path.
 * =====================================================================================
 */
void GenerateFile::setFileName(std::string str)
{
	myOutFile = str;
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  openFileToWrite
 *  Description:  
 * =====================================================================================
 */
void GenerateFile::openFileToWrite(void)
{
	
#ifdef  DEBUG
	std::cout<<"\nFuntion GenerateFile::openFileToWrite ...\n";
	std::cout<<"\nPassed argument is:"<<myOutFile<<"\t"<<myOutFile.c_str()<<"\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	//ReadFile::myFileStream.open(myFile.c_str());
	pOutFile = fopen(myOutFile.c_str(), "w+");
	if(NULL != pOutFile)
	{
		std::string s1 = "// Automatically created by gv-interface v0.1.\n// To be used by dot file.\n// Report all Bugs to dilawar.in@gmail.com. Or you may like to kill few of them.\n";
		fputs(s1.c_str(), pOutFile);
		s1 = "\ndigraph diaG01\n{";
		fputs(s1.c_str(), pOutFile);
		//
#ifdef  DEBUG
		std::cout<<"\nWe have successfully opened the file... \n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	}
	else
	{
		std::cout<<"\nFATAL ERROR : Can not create the file!"
						 <<"\nI do not have enough privileges to create this file. This"
						 <<"\nis really embarrassing.\n";
	//	fclose(pOutFile);
		exit(EXIT_FAILURE);
	}
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
 	/* convert these integer values to characters. */
	for(unsigned int i =0; i < vecOfNodes.size(); ++i)
	{
		char a =  i + 'a';
		vecNamesOfNodes.push_back(a);
	}
#if DEBUG
	for(unsigned int i = 0; i < vecNamesOfNodes.size(); i++)
	{
		std::cout<<"\tNode :"<<vecNamesOfNodes[i];
	}
#endif
	return EXIT_SUCCESS;
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  initializeNodeData
 *  Description:  initializeNodeData
 *
 * =====================================================================================
 */

int GenerateFile::initializeNodeData()
{
	int lenVec = vecQuickFind.size();
	int lenVecNode = vecOfNodes.size();

	if(lenVec == lenVecNode)
	{
		std::cout<<"\nVector is already initialized...\n";
		return EXIT_SUCCESS;
	}
	if(lenVec == 0)
	{
		for(int i = 0; i < lenVecNode; i++)
		{
			vecQuickFind.push_back(vecOfNodes[i]);
		}
		return EXIT_SUCCESS;
	}
	else
	{
		std::cerr<<"\nVector is corrupt...";
		return EXIT_FAILURE;
	}
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  quickFind
 *  Description:  do quick find on the data.
 * =====================================================================================
 */

void GenerateFile::quickFindOnce(std::vector<int> vecCoupleData)
{
	int lenVecData = vecCoupleData.size();
#ifdef  DEBUG
	std::cout<<"\nEntering GenerateFilen::quickFind function...\n";
	for(int i =0 ; i < lenVecData; i++)
	{
		std::cout<<"\tData :"<<vecCoupleData[i];
	}
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */

	if(lenVecData == 0)
		std::cerr<<"\nVector with zero element passed. What you are doing?...\n";

	else{
		std::vector<int> copyVecData; /* copy to hold data. */
		for(int i = 0; i < lenVecData; i++)
		{
			copyVecData.push_back(vecCoupleData[i]);
		}
	}
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  quickFind
 *  Description:  top level function for quickFind
 * =====================================================================================
 */

void GenerateFile::quickFind()
{

#ifdef  DEBUG
	std::cout<<"\nInside quickFind ... \n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	if(EXIT_SUCCESS == initializeNodeData())
	{
		unsigned int sizeVecPairs = vecPairs.size();
		for(unsigned int i =0 ; i < sizeVecPairs ; i = i+2)
		{
			int firstElement = vecPairs[i];
			int secondElement = vecPairs[i+1];
#if DEBUG_CHECKED
			std::cout<<"fstEle: "<<firstElement<<"second elem :"<<secondElement;
#endif
			for(unsigned int j = 0; j < vecQuickFind.size(); j++)
			{
				/* search big element and set is equal so smaller one. */
				std::vector<int> index1;
				std::vector<int> index2;
				// get all the index for these two numbers.
				if(firstElement == vecOfNodes[j])
				{
					index1.push_back(i);
				}
				if(secondElement == vecOfNodes[j])
				{
					index2.push_back(j);
				}
				int i1 = index1[0];
				int i2 = index2[0];

				if(vecQuickFind[i1] <= vecQuickFind[i2])
				{
					for(int k = 0; k < index2.size(); k++)
					{
						int p = index2[k];
						vecQuickFind[p] = vecQuickFind[i1];
					}
				}
				else
				{
					for(int k = 0; k < index1.size(); k++)
					{
						int p = index1[k];
						vecQuickFind[p] = vecQuickFind[i2];
					}
				}
#if 0
				if(firstElement <= secondElement)
				{
					if(vecOfNodes[j] == secondElement)
					{
						if(vecQuickFind[j] < vecQuickFind[
					}
				}
				else
				{
					if(vecOfNodes[j] == firstElement)
					{
						vecQuickFind[j] = secondElement;
					}
				}
			}
			drawQuickFindGraph(i/2+1); // draw the graph for every step.
		}
#endif
#ifdef  DEBUG_MAIN

		for(int i = 0 ; i < vecQuickFind.size(); i++)
		{
			std::cout<<"vecQuickFind "<<vecQuickFind[i];
		}
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
		/* when all done, close the txt file. */
		std::string st = "\n}";				
		if(fseek(pOutFile, 0, SEEK_END) == 0)
		{
			fputs(st.c_str(), pOutFile); // using c++ type string in c function.
		}
		else
			printf("\nSorry, I can not write properly. I am taught well.\n");
	}
	fclose(pOutFile);
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  drawQuickFindGraph
 *  Description:  quick find implementation with dot tool interface.
 * =====================================================================================
 */
void GenerateFile::drawQuickFindGraph(int idParent)
{
	// set edgeId for 
	int idP = idParent;
	// initialize vector.
	
	if(EXIT_SUCCESS == initializeNodeData())
	{
		generateDotFile(vecQuickFind, true, idP);
	}
}

/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  generateDotFile
 *  Description:  
 * =====================================================================================
 */
void GenerateFile::generateDotFile(std::vector<int> vecData, bool ifSubgraph, int idParent)
{
	std::cout<<"\nIn function generateDotFile.... \n";
	//freopen(myOutFile.c_str(), "at", pOutFile);
	bool subG = ifSubgraph;
	char labelSubGraph =  idParent+48;
	std::cout<<"\nsubG :"<<subG;
	std::cout<<"\n labelSubGraph :"<<labelSubGraph;
	if(true == subG)
	{
		//std::cout<<"from file.."<<getc(pOutFile);
		std::string st = "\n\tsubgraph subG";
		st = st+labelSubGraph+"{";
		// go to the end of the file.
		if(fseek(pOutFile, 0, SEEK_END) == 0)
		{
			fputs(st.c_str(), pOutFile); // using c++ type string in c function.
		}
		else
			printf("\nSorry, I can not write properly. I am taught well.\n");

		/*
		 * Now, we extract out nodes connected with anyone.
		 */
		std::vector<int> vecOfCouples;

		//bool ifSingle = false;
		
		/* Create a copy of vecId*/
		std::vector<int> copyVecData;
		for(unsigned int i = 0; i < vecData.size(); i++)
		{
			copyVecData.push_back(vecData[i]);
		//	std::cout<<"\tcvd"<<copyVecData[i]; // checked
		}
		
		std::vector<int>::iterator itP2 = copyVecData.begin();
		std::vector<int>::iterator itP1 = vecData.begin();
		
		/* Carry on , Fellas */
		for(unsigned int i = 1 ; i <= vecData.size(); i++)
		{
			unsigned int lenCopyVecData = copyVecData.size();
#if DEBUG_ALL
			std::cout<<"\nlength : "<<lenCopyVecData;
#endif
			if(i < lenCopyVecData)
			{
				std::cout<<"";
				itP2 = copyVecData.begin(); 
				for(unsigned int p = 0; p < i ; p++)
				{
					itP2 = itP2 + 1;
				}
#if DEBUG1
				std::cout<<"\ncopyVecData.begin()"<<*itP2<<" next :"<<*(itP2+1);
#endif
#if DEBUG1
				std::cout<<"\nitP2 :"<<*itP2<<"\titP1 :"<<*itP1;
#endif
				for(unsigned int j = i+1; j <= lenCopyVecData; j++)
				{
					if(*itP1 == *itP2)
						{
#if DEBUG_ALL
							std::cout<<"\tFound.";
#endif
							vecOfCouples.push_back(vecOfNodes[i-1]); /* get the id of the node */
							vecOfCouples.push_back(vecOfNodes[j-1]); /* and the second node. */
							copyVecData.erase(itP2);			 // pointer already updated to next
						}
					else
					{
#if DEBUG_ALL
						std::cout<<"\tNtEq";
#endif
						itP2 = itP2+1; // update the pointer.
					}
				}
				itP1 = itP1 + 1; // point to ith element now.
			}
		}

#ifdef  DEBUG
		std::cout<<"\nPairs are : \n";
		for(unsigned int i = 0; i < vecOfCouples.size(); ++i)
		{
			std::cout<<"\t"<<vecOfCouples[i];
		}
		std::cout<<"\nNodes are :\n";
		for(unsigned int i = 0; i < vecOfNodes.size(); ++i)
		{
			std::cout<<"\t"<<vecOfNodes[i];
		}
		std::cout<<"\nData are :\n";
		for(unsigned int i = 0; i < vecData.size(); ++i)
		{
			std::cout<<"\t"<<vecData[i];
		}
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */

		/*
		 * now we write these values inside the file.
		 */
		std::string thisNode = "";
		std::string nextNode = "";
		st = "\n\t\t// Node are the followings.";
		if(fseek(pOutFile, 0, SEEK_END) == 0)
		{
			fputs(st.c_str(), pOutFile); // using c++ type string in c function.
		}
		else
			printf("\nSorry, I can not write properly. I am taught well.\n");

		st = "";
		for(unsigned int i = 0; i < vecOfNodes.size(); i++)
		{
			std::string nd = "";
			int a = vecOfNodes[i];
			if( a > 100)
			{
				char ch = a%100 + 48;
				nd = nd+ch;
				a = a/100;
			}
			if(a>10)
			{
				char ch = a%10 + 48;
				nd = nd+ch;
				a = a/10;
			}
			char ch = a+48;
			nd = nd+ch;
			st = st+"\n\t\t"+nd+";";
		}
		st = st+"\n\t// Here are our cute couples. \n";
		/* get the couples. */
		for(unsigned int i = 0; i < vecOfCouples.size(); i = i+2)
		{
			char ch;
			std::string nd = "";
			std::string ndd ="";
			int a = vecOfCouples[i];
			int b = vecOfCouples[i+1];
			// get char of a
			if( a > 100)
			{
				ch = a%100 + 48;
				nd = nd+ch;
				a = a/100;
			}
			if(a>10)
			{
				ch = a%10 + 48;
				nd = nd+ch;
				a = a/10;
			}
			ch = a+48;
			nd = nd+ch;
		// do same for next node
			if( b > 100)
			{
				ch = b%100 + 48;
				ndd = ch+ndd;
				b = b/100;
			}
			if(b>10)
			{
				ch = b%10 + 48;
				ndd = ndd+ch;
				b = b/10;
			}
			ch = b+48;
			ndd = ndd+ch;
			st = st+"\n\t\t"+nd+" -> "+ndd+";"; // couples are done
		}
		st = st+"\n\t}"; // close the subgraph module.
	
		if(fseek(pOutFile, 0, SEEK_END) == 0)
		{
			fputs(st.c_str(), pOutFile); // using c++ type string in c function.
		}
		else
			printf("\nSorry, I can not write properly. I am taught well.\n");
	}
}
