/* Solve ODE and plot trajectories */
load( contrib_ode )$
load( implicit_plot )$

eq : 'diff(x,t) = (x+1)^2*x*(x-2);
sol : contrib_ode( eq, x, t );
icc : ic1( sol, x= 0.5, t=0 );
ratsimp( icc );
implicit_plot( icc, [t, 0, 1], [x, -2, 2] );
