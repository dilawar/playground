#include <iostream>
using namespace std;

int main(int argc, const char *argv[])
{
    double t1 = 0.1;
    double t2 = 0.4;

    double& a(t1);
    double& b(a);   // a and b are linked now.

    cout << " a is " << a << " and b is " << b << endl;

    a = 9.0;
    cout << " a is " << a << " and b is " << b << endl;

    b = 11.0;
    cout << " a is " << a << " and b is " << b << endl;
    
    return 0;
}

