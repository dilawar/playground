weakSolution = [(s,e,n,d,m,o,r,y) | s <- [8,9] , e <- [0..9], n <- [0..9], d <-[0..9], m <- [1]
                            , o <- [0,1], r <- [0..9],  y <-[0..9]
                            , d+e==y || d+e == 10+y
                            , n+r==e || n+r==10+e || 1+n+r==e || 1+n+r==10+e
                            , e+o==n || e+o==10+n || 1+e+o==n || 1+n+o==10+n
                            , s+m==10+o || 1+s+m==10+o
                            , m==1
                            , s /= e , s /= n, s /= d, s /= m , s /=o, s /= r, s /= y
                            , e /= n, e /= d, e /= m , e /=o, e /= r, e /= y
                            , n /= d, n /= m , n /=o, n /= r, n /= y
                            , d /= m , d /=o, d /= r, d /= y
                            , m /=o, m /= r, m /= y
                            , o /= r, o /= y
                            , r /= y]

strongSolution = [(s,e,n,d,m,o,r,y) | s <- [8,9] , e <- [0..9], n <- [0..9], d <-[0..9], m <- [1]
                            , o <- [0,1], r <- [0..9],  y <-[0..9]
                            , s /= e , s /= n, s /= d, s /= m , s /=o, s /= r, s /= y
                            , e /= n, e /= d, e /= m , e /=o, e /= r, e /= y
                            , n /= d, n /= m , n /=o, n /= r, n /= y
                            , d /= m , d /=o, d /= r, d /= y
                            , m /=o, m /= r, m /= y
                            , o /= r, o /= y
                            , r /= y
                            , (1000 * s + 100 * e + 10*n + d) + (1000 * m + 100*o + 10*r + e) 
                                == (10000*m + 1000*o + 100*n + 10*e + y)]

crazySolution = [(s,e,n,d,m,o,r,y) | s <- [8,9] , e <- [0..9], n <- [0..9], d <-[0..9], m <- [1]
                            , o <- [0,1], r <- [0..9],  y <-[0..9]
                            , (d+e==y &&
                                (n+r==e && 
                                    (e+o==n && (s+m==10+o||s+m==9+o)||(e+o==10+n && (s+m==10+o || s+m==9+o))))
                                 || (n+r==10+e &&
                                    ((1+e+o==n) && (s+m==10+o||s+m==9+o))||(1+e+o==10+n && (s+m==10+o || s+m==9+o))))
                             || (d+e==10+y &&
                                (1+n+r==e && 
                                    ((e+o==n && (s+m==10+o||s+m==9+o))||(e+o==10+n && (s+m==10+o || s+m==9+o))))
                                 || (1+n+r==10+e &&
                                    ((1+e+o==n) && (s+m==10+o||s+m==9+o))||(1+e+o==10+n && (s+m==10+o || s+m==9+o))))
                            , s /= e , s /= n, s /= d, s /= m , s /=o, s /= r, s /= y
                            , e /= n, e /= d, e /= m , e /=o, e /= r, e /= y
                            , n /= d, n /= m , n /=o, n /= r, n /= y
                            , d /= m , d /=o, d /= r, d /= y
                            , m /=o, m /= r, m /= y
                            , o /= r, o /= y
                            , r /= y]


