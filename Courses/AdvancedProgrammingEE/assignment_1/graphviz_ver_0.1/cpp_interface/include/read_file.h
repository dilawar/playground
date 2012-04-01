/*
 * =====================================================================================
 *
 *       Filename:  read_file.h
 *
 *    Description:  This file contains the class which is responsible to read a file 
 *    							having pairs of connections. It also checks if the format of
 *    							the given file is OK. See README_FILE_FORMAT file for more
 *    							details. 
 *
 *        Version:  1.0
 *        Created:  Sunday 08 August 2010 12:09:37  IST
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


#ifndef  read_file__INC
#define  read_file__INC
#include	<stdio.h>
#include	<iostream>
#include	<string>
#include	<vector>

/*
 * =====================================================================================
 *        Class:  ReadFile
 *  Description:  handle the file from command line.
 * =====================================================================================
 */
class ReadFile
{
	public:
	

		/* ====================  LIFECYCLE     ======================================= */
		ReadFile ();                             /* constructor */
		
		virtual ~ReadFile();
		/* ====================  ACCESSORS     ======================================= */
		
		/*
		 * This will set the private member for reading this file
		*/
		void setFilePointer(std::string);

		/* 
		 * This will show what is inside the file.
		 */
		void showFileContent();
		
		/*
		 * This will copy the pairs into two a vectors.
		 */
		void copyFileIntoAVector();

		/*
		 * This will check the file for errors.
		 */
		int checkFileForErrors();

		/*
		 * This will provide the interface to other object.
		 */
		std::vector<int> copyVecToVec();


		/* ====================  MUTATORS      ======================================= */

		/* ====================  OPERATORS     ======================================= */

		/* ====================  DATA MEMBERS  ======================================= */
	protected:

	private:
		FILE* fp;
	//	std::ifstream myFileStream;
		std::vector<int> vecOfPairs;
		

}; /* -----  end of class ReadFile  ----- */

#endif   /* ----- #ifndef read_file__INC  ----- */
