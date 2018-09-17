import numpy as np

def main():
    a = np.matrix( '1 1 2;1 2 3;2 3 4' )
    print( a )
    ainv = a ** -1
    print( ainv )
    print( np.dot(a, ainv) )
    print( 'Doing permutation' )
    p1 = np.matrix( '1 -1 -2; 0 1 0; 0 0 1' )
    print( p1 )
    a1 = a*p1
    print( 'p1', p1, '\na1', a1 )
    p2 = np.matrix( '1 0 0;-1 1 -1;0 0 1' )
    a2 = a1 * p2
    print( 'p2', p2, '\na2', a2 )
    p3 = np.matrix( '1 0 0;0 1 0;1 1 1' )
    a3 = a2 * p3
    print( 'p3', p3, '\na3', a3 )
    ainv1 = p1 * p2 * p3
    print( '================' )
    print( ainv1 )
    print( ainv )


if __name__ == '__main__':
    main()
