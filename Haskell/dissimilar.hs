import Data.List 


rewrite str = helper str str
    where
        helper [ ] str = [ ]
        helper (x:xs) str = (takeWhile (==x) str) : (helper xs str)

teststring = "12345" 

test = map rewrite  [ teststring ] -- $ permutations teststring
    
