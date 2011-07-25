#include<iostream>

using namespace std;

int main()
{
	unsigned long long int num;
	cout<<"enter the no :";
	cin>>num;
	unsigned long long int floor_sqrt;

	bool isFound = 0;
	bool isBigger = 0;
	bool isSmaller = 0;
	unsigned long long int p = num/2;
	unsigned long long int i = 0;
	unsigned long counter = 1;
	while(counter <= 1000000)
	{
		if(isFound == 0)
		{
			if(p*p > num && p*(p-1) > num) 
			{
				isBigger = true;
				cout<<"\nisBigger: "<<isBigger<<"and num "<<p;
				p = (p + i)/2;
				cout<<"\t Next p :"<<p <<" i :" << i;
				isFound = false;
			}
			if(p*p < num && p*(p+1) < num)
			{
				isSmaller = true;
				cout<<"\nIsSmaller: "<<isSmaller<<"and num "<<p;
				i = p;
				p = p + p/2;
				cout<<"\t next p :"<<p<<"i: "<<i;
				isFound = false;
			}
			if(p*p == num) 
			{
				isFound = 1;
				floor_sqrt = p;
				cout<<"Equal :num is :"<<floor_sqrt;
			}

			if(p*p < num && (p+1)*(p+1) > num)
			{
				isFound = 1;
				floor_sqrt = p;
				cout<<"small and big, num is :"<<floor_sqrt<<"\n";
			}
		}
		counter++;
	}
	cout<<"\nCounter is :"<<counter<<endl;
	return 0;
}

