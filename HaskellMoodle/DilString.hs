module DilString where
 
 {- This function split a given string at another substring pat. Its behaviour is
 - exactly like python split.
 -}

split :: String -> String -> [String]
split str pat = helper str pat [] [] where 
    helper :: String -> String -> String -> String -> [String]
    helper [] ys n m = [n] ++ []
    helper xs [] n m = [n] ++ (split xs pat)
    helper (x:xs) (y:ys) n m
        | x /= y = helper (xs) pat ((n++m)++[x]) m
        | otherwise = helper xs ys n (m++[y])

