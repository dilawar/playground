from myhdl import *

ACTIVE_LOW, INACTIVE_HIGH = 0, 1

def Inc(count, enable, clock, reset, n):

    @always(clock.posedge, reset.negedge)
    def incLogic():
        if reset == ACTIVE_LOW:
            acount.next = 0
        else:
            if enable:
                count.next = (count + 1) % n

    return incLogic


def bin2gray(B, G, width):

    @always_comb
    def logic():
        Bext = intbv(0)[width+1:]
        Bext[:] = B
        for i in range(width):
            G.next[i] = Bext[i+1] ^ Bext[i]
    return logic
