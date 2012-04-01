#include <iostream>
#include <queue>
using namespace std;

int main()
{
    queue<char> q;
    q.push('a');
    q.push('b');
    q.push('c');

    cout << q.front() << endl;
    cout << q.back() << endl;
    q.pop();
    cout << q.front() << endl;
    q.pop();
    cout << q.front() << endl;
    q.pop();
}
