#include <stdio.h>
#include <math.h>
char infile[85], outfile[85], linebuf[135], wrkbuf[135];
FILE *dat, *out;

main (argc, argv)
     int argc;
     char *argv[];
{
float a, b, c, discriminant, x1, x2, x3;
/* This program illustrates the effect of round off
 * during the calculation of the roots of a quadratic. */

/* Choose coefficients such that ac << b^2 */
printf("Give the coefficient of x^2 (a):  ");
scanf("%f", &a);
printf("Give the coefficient of x   (b):  ");
scanf("%f", &b);
printf("Give the constatnt term     (c):  ");
scanf("%f", &c);

/* Normally, all intermediate values are computed in
 * extended precision and their precision is reduced to
 * double or float only at the time of storing their values.
 * Therefore we calculate the discriminant in steps
 * storing all intermediate values as float.
 * This converts each term from extended precision to float */
discriminant =  b*b;
discriminant -= 4.0*a*c;
discriminant = sqrt(discriminant);
/* Traditional calculation for roots */
x1 = (-b + discriminant)/(2.0*a);
x2 = (-b - discriminant)/(2.0*a);
printf("---------------------------------\n");
printf("x1= %13.7e\n", x1);
printf("x2= %13.7e\n", x2);
/* Improved calculation */
if(b < 0){
    x3 = c/(a * x1);
    printf("replace x2 by x3 = %13.7e\n", x3);
}
else {
    x3 = c/(a * x2);
    printf("replace x1 by x3 = %13.7e\n", x3);
}
printf("---------------------------------\n");
/* Now verify roots by substituting in the equation
 * and calculating the resideue. */
printf("       ROOT            RESIDUE \n");
printf("x1= %13.7e:   %13.7e\n", x1, a*x1*x1 + b*x1 + c);
printf("x2= %13.7e:   %13.7e\n", x2, a*x2*x2 + b*x2 + c);
printf("x3= %13.7e:   %13.7e\n", x3, a*x3*x3 + b*x3 + c);
}
