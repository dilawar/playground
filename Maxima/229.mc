/* Solve ODE and plot trajectories */
load( contrib_ode )$
load( draw )$

keepfloat:true$
eq : 'diff(x,t) = (x+1)*x*(x-1)^3;
sol : contrib_ode( eq, x, t );
icc : ic1( sol, x= 1.2, t=0 );

subplot1: gr2d( implicit( first(icc),t,0,10,x,-5,5 ) 
    , grid = true
    , xlabel = "t", ylabel = "x" )$
subplot2: gr2d( xlabel = "x", ylabel = "dx"
    , explicit( rhs(eq), x, -2, 3) 
    , grid = true
    )$

draw( subplot1, subplot2
    , dimensions = [1000,500]
    , columns = 2
    , terminal = pdfcairo
    , file_name = "229_fig" 
    );
