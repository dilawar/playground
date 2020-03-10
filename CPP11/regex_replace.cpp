// =====================================================================================
//
//       Filename:  regex_replace.cpp
//
//    Description:  
//
//        Version:  1.0
//        Created:  Tuesday 10 March 2020 01:01:06  IST
//       Revision:  none
//       Compiler:  g++
//
//         Author:  Dilawar Singh (), dilawar.s.rajput@gmail.com
//   Organization:  NCBS Bangalore
//
// =====================================================================================

#include <iostream>
#include <regex>
#include <list>

using namespace std;

string moosePathToColumnName(const string& path, char delim='.', size_t maxLevel=2)
{
    string s(path);
    static std::regex e0("\\[(0+)\\]");         // Remove [0+]  
    static std::regex e1("\\[(\\d+)\\]");       // Replace [xyz] by xyz
    s = std::regex_replace(s, e0, "");
    s = std::regex_replace(s, e1, "$1");

    // Keep just last two levels. E.g. /a0/b1/c23/d2 -> /c23/d2
    string s2;
    string colname="";
    size_t nBreak = 0;
    for(auto rit = s.rbegin(); rit != s.rend(); rit++)
    {
        if(*rit=='/')
        {
            colname = s2 + delim + colname;
            s2="";
            nBreak += 1;
            if(nBreak == maxLevel)
                break;
        }
        else
            s2 = *rit + s2;
    }
    colname.pop_back();
    return colname;
}

int main(int argc, const char *argv[])
{
    vector<string> paths = { "/aa[0]/b[1]/c[0]" };
    for(auto p : paths)
        cout << p << " to " << moosePathToColumnName(p) << endl;
    return 0;
}

