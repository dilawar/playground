import graph3; 
import palette;

import solids;
size(7cm,0);

currentprojection=perspective(camera=(5,-4,2));
viewportmargin=(.5cm,.5cm);
currentlight=White;

triple f(pair p){
  real x=1+cos(p.x);
  real y=sin(p.x);
  real z=p.y*sqrt(4.0001-x^2-y^2);
  return (x,y,z);
}
triple g(pair p, real k){
  real x=1+cos(p.x);
  real y=p.y*sin(p.x);
  real z=k*sqrt(4.0001-x^2-y^2);
  return (x,y,z);
}
triple g1(pair p){ return g(p,1); }
triple gm1(pair p){ return g(p,-1); }

int n=100;
pen stylo = yellow, stylo2 = red;
draw(surface(f,(0,-1),(2pi,1),n),stylo);
//draw(surface(g1,(0,-1),(2pi,1),n),stylo2);
//draw(surface(gm1,(0,-1),(2pi,1),n),stylo2);


