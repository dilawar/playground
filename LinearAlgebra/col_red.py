import numpy as np

def main():
    a = np.matrix( '1 1 1;1 2 3;2 3 4' )
    print( a )
    ainv = a ** -1
    print( ainv )
    print( np.dot(a, ainv) )

if __name__ == '__main__':
    main()
