/* Autocatalysis */
load( contrib_ode )$
load( draw )$

A : a0; /* A remains constant */
x0 : 10$
rhsEq : ev( -kf * A * X + kb * X^2, kf=0.1, kb=0.1, a0=15)$
eqx : 'diff( X,t) = rhsEq;
xGeneral : contrib_ode( eqx, X, t ); 
xImplicit : first( ic1( xGeneral, X = x0, t = 0 ) );

plota : gr2d( explicit( rhsEq, X,0, 100), xlabel = "X", ylabel="dX/dt" );
plotb : gr2d( implicit( xImplicit, t,0,10,X,0,200)
    , xlabel = "t", ylabel = "X(t)"
    );

draw( plota, plotb
    , dimensions = [1000, 500]
    , terminal = pdfcairo
    , file_name = "232_solution"
    , columns = 2
);

