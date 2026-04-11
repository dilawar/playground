// =====================================================================================
//
//       Filename:  switch_in_for.cpp
//
//    Description: Break in switch loop.
//
//        Version:  1.0
//        Created:  23/05/21 06:53:27 AM IST
//       Revision:  none
//       Compiler:  g++
//
//         Author:  Dilawar Singh (), dilawar@subcom.tech
//   Organization:  Subconscious Compute
//
// =====================================================================================

#include <iostream>
using namespace std;

int main()
{
    int i = 0;
    for (i = 0; i < 4; ++i) {
        switch(i) {
            case 0:
                cout << 0 << endl;
                break;
            case 1:
                cout << 1 << endl;
                break;
            default:
                cout << 2 << endl;
                break;
        }
    }
}
