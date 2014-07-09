# distutils: language = c++
# distutils: extra_compiler_args = -DCYTHON
cimport b as _b
cimport a as _a

cdef class PyA:
    cdef _a.A* thisptr

    def __cinit__(self):
        self.thisptr = new _a.A()

    def get(self):
        return self.thisptr.get()

cdef class PyB:
    cdef _b.B *thisptr

    def __cinit__(self):
        print("Calling PyB constructor")
        self.thisptr = new _b.B()

    def __dealloc__(self):
        del self.thisptr

    # Now how to get A.
    def getA(self):
        cdef _a.A retA
        retA = self.thisptr.getA()
        a = PyA()
        a.thisptr = &retA
        print("Value of a is %s" % a.get())
        return a
    
    # This is a pure python function.
    def printSomething(self):
        print("Printing something here")
