# distutils: language = c++
# distutils: extra_compiler_args = -DCYTHON
cimport b as _b
cimport a as _a

cdef class PyB:
    cdef _b.B *thisptr

    def __cinit__(self):
        self.thisptr = new _b.B()

    def __dealloc__(self):
        del self.thisptr

    # Now how to get A.
    def getA(self):
        cdef _a.A* retA
        retA = self.thisptr.getA()
    
    # This is a pure python function.
    def printSomething(self):
        print("Printing something here")
