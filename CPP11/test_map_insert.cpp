// =====================================================================================
//
//       Filename:  test_util.cpp
//
//        Version:  1.0
//        Created:  08/06/21 10:24:19 PM IST
//       Revision:  none
//       Compiler:  g++
//
//         Author:  Dilawar Singh (), dilawar@subcom.tech
//   Organization:  Subconscious Compute
//
// =====================================================================================


#include <iostream>
#include <utility>
#include <map>


using namespace std;

struct mystruct {
    int a;
    int b;
};

int main()
{
    mystruct* a = new mystruct({.a = 1, .b = 1});
    mystruct* b = new mystruct({.a = 2, .b = 2});
    map<size_t, pair<size_t, mystruct*>> map_{ {0, make_pair(1, a)}, {1, make_pair(2, b)}};
    for(auto a : map_)
        cout << a.first << " " << a.second.first << endl;

    map_[0].first += 10;

    for(auto a : map_)
        cout << a.first << " " << a.second.first << endl;

    std::cout << "Done" << std::endl;
    return 1;
}
