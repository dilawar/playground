# distutils: language = c++
# distutils: extra_compiler_args = -DCYTHON
cimport b as _b

cdef class PyB:
    cdef _b.B *thisptr

    def __cinit__(self):
        self.thisptr = new _b.B()

    def __dealloc__(self):
        del self.thisptr
