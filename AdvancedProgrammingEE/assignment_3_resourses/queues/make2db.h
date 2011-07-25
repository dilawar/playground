#ifndef Make2DArray_
#define Make2DArray_

template <class T>
void Make2DArray(T ** &x, int rows, int cols)
{// Create a two-dimensional array.

   // create pointers for the rows
   x = new T * [rows];
      
   // get memory for each row
   for (int r = 0; r < rows; r++)
      x[r] = new T [cols];
}

#endif
