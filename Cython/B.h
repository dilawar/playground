/*
 * ==============================================================================
 *
 *       Filename:  B.h
 *
 *    Description:  
 *
 *        Version:  1.0
 *        Created:  Wednesday 09 July 2014 02:16:29  IST
 *       Revision:  none
 *       Compiler:  gcc
 *
 *         Author:  Dilawar Singh (), dilawar@ee.iitb.ac.in
 *   Organization:  
 *
 * ==============================================================================
 */

#include <iostream>

class A;

using namespace std;

class B
{
    public:
        B()
        {
            cout << "Creating B" << endl;
        }

        void printB(A& a)
        {
            cerr << "B " << endl;
        }

        A* getA(void)
        {
            return a;
        }

    private:
        A* a;
};
