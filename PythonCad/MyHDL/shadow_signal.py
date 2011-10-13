def permute(x, a, mapping):
   
""" Permute input bits,

    x : output port
    a : input port
    mapping : tuple that maps input to output
"""

    p = [a(m) for m in mapping] # index signal.

    q = ConcatSignal(*p)

    @always_comb
    def assign():
        x.next = q

    return assign

