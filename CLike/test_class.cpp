// =====================================================================================
//
//       Filename:  test_class.cpp
//
//    Description:  
//
//        Version:  1.0
//        Created:  19/05/19 01:02:15 PM IST
//       Revision:  none
//       Compiler:  g++
//
//         Author:  Dilawar Singh (), dilawar.s.rajput@gmail.com
//   Organization:  NCBS Bangalore
//
// =====================================================================================

#include <iostream>

using namespace std;

class test_class
{
    public:
        test_class()
        {
            cout << "Callinng default contrctor." << endl;
            cout << " Name " << name << " age " << age << endl;
        }

        ~test_class() 
        {
            cout << "Callinng default decontructor." << endl;
        }

    private:
        /* data */
        double age = 0.0;
        string name = "Dumb guy.";

};

int main(int argc, const char *argv[])
{
    test_class a;
    //test_class* pA = new test_class();
    //delete pA;
    
    return 0;
}
