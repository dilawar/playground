cimport a as _a
cdef extern from "B.h":
    cdef cppclass B:
        B()
        _a.A getA()
