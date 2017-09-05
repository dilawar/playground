from myhdl import *
import random


def Inc(out, in1):

    """ Incrementer with enable.

    count -- output
    enable -- control input, increment when 1
    clock -- clock input
    reset -- asynchronous reset input

    """

    event = Signal( bool(0) )

    @always( event )
    def incLogic():
        out.next = in1 + 1
        print( '.. %5d, %5d' % (now(), out.val ) )

    return incLogic

# Main function.
def main( ):
    c = Signal( 0 )
    clk = Signal( bool(1) )

    inc = Inc( c, clk )

    tb = Simulation( inc )

    tb.run( 100 )


if __name__ == '__main__':
    main()

