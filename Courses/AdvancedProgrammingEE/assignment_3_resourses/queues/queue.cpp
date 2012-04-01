// test formula based queue class

#include <iostream>
#include "queue.h"
using namespace std;

int main()
{
   Queue<int> Q(3);
   int x;

   try 
   {
       Q.Add(1);
       Q.Add(2);
       Q.Add(3);
       Q.Add(4);
       cout << "No queue add failed" << endl;
   }
   catch (NoMem)
   {
       cout << "A queue add failed" << endl;
   }

   cout << "Queue is now 123" << endl;
   x = Q.First();
   Q.Delete();
   cout << "Deleted " << x << endl;
   cout << Q.First() << " is at front" << endl;
   cout << Q.Last() << " is at end" << endl;

   try 
   {
      x = Q.First();
      Q.Delete();
      cout << "Deleted " << x << endl;
      x = Q.First();
      Q.Delete();
      cout << "Deleted " << x << endl;
      x = Q.First();
      Q.Delete();
      cout << "Deleted " << x << endl;
      cout << "No queue delete failed " << endl;
   }
   catch (OutOfBounds)
   {
       cout << "A delete has failed" << endl;
   }
}
