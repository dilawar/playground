/* Solve ODE and plot trajectories */
load( contrib_ode )$
load( implicit_plot )$

eq : 'diff(x,t) = (x+1)*x*(x-1)^3;
sol : contrib_ode( eq, x, t );
icc : ic1( sol, x=1.2, t=0 );
ratsimp( icc );
implicit_plot( icc, [t, 0, 20], [x, -5, 5] );
