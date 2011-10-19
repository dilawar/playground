#include <stdio.h>
#include <math.h>
void dispnum(float x);
int main()
{
float x;

printf("Give a floating point number to represent: ");
scanf("%f", &x);
/* Function dispnum is useful to see how floats are represented */
dispnum(x);
}
void dispnum(float x)
{
unsigned char *cp;
/* Coerce the stored value of x to an array of bytes */
cp = (unsigned char*) &x;
/* Now print each byte of the representation in Hex.
 * Remember, Intel uses the little endian convention. */
printf("%13.7e : %.2x %.2x %.2x %.2x \n", x, cp[3],cp[2], cp[1], cp[0]);
/* Format of float representation is:
 * 1bit sign; 8 bits of exponent biased by 127; 23 bit significand */
}
