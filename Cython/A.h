#ifndef  A_INC
#define  A_INC
/*
 * ==============================================================================
 *
 *       Filename:  A.h
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  Wednesday 09 July 2014 02:15:19  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawar@ee.iitb.ac.in
 *   Organization:  
 *
 * ==============================================================================
 */

#include <iostream>
#include <cstdlib>

using namespace std;

class A
{
    public:
        A()
        {
            a = rand() % 1000;
            cout << "Creating A wit a = " << a << endl;
        }

        void printA()
        {
            cerr << "A " << endl;
        }

        int get()
        {
            return a;
        }
        
        int a;
};
#endif   /* ----- #ifndef A_INC  ----- */
