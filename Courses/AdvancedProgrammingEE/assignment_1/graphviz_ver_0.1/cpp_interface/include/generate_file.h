/*
 * =====================================================================================
 *
 *       Filename:  generate_file.h
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  Sunday 08 August 2010 01:24:52  IST
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


#ifndef  generate_file_INC
#define  generate_file_INC

#include	"./../include/read_file.h"
#include	<vector>
#include	<iostream>

/*
 * =====================================================================================
 *        Class:  GenerateFile
 *  Description:  generate txt file which can be given to graphviz.
 * =====================================================================================
 */
class GenerateFile 
{
	public:
		/* ====================  LIFECYCLE     ======================================= */
		GenerateFile ();                             /* constructor */
		virtual ~GenerateFile();
		

		/* ====================  ACCESSORS     ======================================= */

		/* 
		 * ===  FUNCTION  ======================================================================
		 *         Name:  generateVecOfNodes
		 *  Description:  This function will generation our node names.
		 * =====================================================================================
		 */
		int generateVecOfNodes(std::vector<int>);
			

		/* 
		 * ===  FUNCTION  ======================================================================
		 *         Name:  drawQuickFindGraph
		 *  Description:  
		 * =====================================================================================
		 */
		void drawQuickFGraph();

		/* ====================  MUTATORS      ======================================= */

		/* ====================  OPERATORS     ======================================= */

		/* ====================  DATA MEMBERS  ======================================= */
	protected:

	private:
		/* this vector will contain our nodes. */
		std::vector<int> vecPairs;

		std::vector<int> vecOfNodes;

		std::vector<int> vecQuickFind;

		std::vector<int> vecQuickUnion;

}; /* -----  end of class GenerateFile  ----- */

#endif   /* ----- #ifndef generate_file_INC  ----- */
