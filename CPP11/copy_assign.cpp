#include <iostream>
#include <memory>

using namespace std;

struct Another {
    Another( string a, int c): name(a), value(c) {;}
    string name;
    int value;
};



// =====================================================================================
//        Class:  Test
//  Description:  Test class for copy contructor.
// =====================================================================================
class Test
{
    public:
        // ====================  LIFECYCLE     ======================================= 
        Test() :
            a_( make_shared<string>("hellow a"))
            , b_( make_shared<double>(19.1) )
            , c_( make_shared<Another>("aaaa", 111) )
        { ; }

        // ====================  ACCESSORS     ======================================= 

        // ====================  MUTATORS      ======================================= 

        // ====================  OPERATORS     ======================================= 
        Test& operator=(const Test& t)
        {
            a_ = t.a_;
            b_ = t.b_;
            c_ = t.c_;
            return *this;
        }

        void print()
        {
            cout << "a: " << a_.get() << "(" << *a_ << ") "
                 << " b: " << b_.get() << "(" << *b_ << ")" 
                 << " c: " << &c_ << c_.get() << " " << c_->name << ", " << c_->value
                 << endl;
        }

    protected:
        // ====================  METHODS       ======================================= 

        // ====================  DATA MEMBERS  ======================================= 

    private:
        // ====================  METHODS       ======================================= 

        // ====================  DATA MEMBERS  ======================================= 
        shared_ptr<string> a_;
        shared_ptr<double> b_;
        shared_ptr<Another> c_;

}; // -----  end of class Test  ----- 


int main(int argc, const char *argv[])
{
    Test t1, t2;
    t2 = t1;
    t1.print();
    t2.print();
    return 0;
}
