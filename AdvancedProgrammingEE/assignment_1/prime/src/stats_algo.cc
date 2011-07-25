/*
 * =====================================================================================
 *
 *       Filename:  stats_algo.cc
 *
 *    Description: Added function to calculate the complexity of the algorithms. 
 *
 *        Version:  1.0
 *        Created:  Wednesday 04 August 2010 07:36:11  IST
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


#include	"./../include/stats_algo.h"
#include	<iostream>

//constructor
CollectStats::CollectStats()
{

#ifdef  DEBUG
	std::cout<<"\n Entering CollectStats constructor...\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
	operation allOps;
	allOps.op_name = "nothing";
	allOps.num_op = 0;
	allOps.weight_op = 0;
	allOps.total_cost = allOps.num_op * allOps.weight_op;
}
//Destructor
CollectStats::~CollectStats()
{
	
#ifdef  DEBUG
	std::cout<<"\n Entering CollectStats Destructor...\n";
#else      /* -----  not DEBUG  ----- */

#endif     /* -----  not DEBUG  ----- */
}


/* 
 * ===  FUNCTION  ======================================================================
 *         Name:  calcCostOfOp
 *  Description:  It takes the vector and calculate the full cost of the
 *  implementation. 
 *  TODO : Implement it.
 * =====================================================================================
 */
void calcCostOfOp(std::vector<CollectStats::operation>* pVec)
{
}

