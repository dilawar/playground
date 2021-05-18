#include <boost/algorithm/string.hpp>

#include <algorithm>
#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main()
{
    const string a("|ab|cd|ef|");

    std::vector<std::string> fs;
    boost::split(fs, a, boost::is_any_of("|"));
    for(auto v: fs)
        cout << "f=" << v << " " << v.length() << endl;

    return 0;
}
