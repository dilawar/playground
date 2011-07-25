/*
 * =====================================================================================
 *
 *       Filename:  stats_algo.h
 *
 *    Description:  This file contains class responsible for collecting stats.
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


#ifndef  _stats_algo_h__INC
#define  _stats_algo_h__INC

#include  <vector>
#include	<string>


/*
 * =====================================================================================
 *        Class:  CollectStats
 *  Description: Keep the tracks of functions executed. It will give the number
 *  of times a particular function is used. 
 * =====================================================================================
 */
class CollectStats
{
	public:

		std::string op_name;
		int num_op; // number of time this op is executed.
		double weight_op;
		double total_cost;

		std::vector<double> vecOperation;

#if 0
		int num_op1 = 0;
		double weight_op1 = 0.00; // and so on ..
#endif

	public:


		/* 
		 * ===  FUNCTION  ======================================================================
		 *         Name:  calcCostOfOp
		 *  Description:  this will calculate total cost of various algorithms.
		 * =====================================================================================
		 */
		void calcCostOfOp(void);


		/* ====================  LIFECYCLE     ======================================= */
		CollectStats ();                             /* constructor      */
		CollectStats ( const CollectStats &other );   /* copy constructor */
		~CollectStats ();                            /* destructor       */

		/* ====================  ACCESSORS     ======================================= */

		/* ====================  MUTATORS      ======================================= */



		/* ====================  DATA MEMBERS  ======================================= */
	protected:

}; /* -----  end of class CollectStats  ----- */

#endif   /* ----- #ifndef _stats_algo_h__INC  ----- */
