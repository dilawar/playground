assume(f > 0, b>0 );
assume( f - b > 0 );
a1 : f;
a2 : f;
b1 : b;
b2 : b;

eq1 : 'diff(A(t),t) = - a1*A(t) + b1* B(t)$
eq2 : 'diff(B(t),t) = a1*A(t) - (b1+a2)*B(t) - a2*C(t);
eq3 : 'diff(C(t),t) = a2*B(t) - b2*C(t);

/* Init values */
atvalue(A(t), t=0, a0);
atvalue(B(t), t=0, 0);
atvalue(C(t), t=0, 0);
sol : desolve( [eq1, eq2, eq3], [A(t), B(t), C(t)])$
sol[2];

