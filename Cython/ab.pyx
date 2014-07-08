# distutils: langauge = c++
include "a.pxd"
include "b.pxd"

cdef class B:
    cdef B *thisptr

    def __cinit__(self):
        self.thisptr = new B()

    def __dealloc__(self):
        del self.thisptr
