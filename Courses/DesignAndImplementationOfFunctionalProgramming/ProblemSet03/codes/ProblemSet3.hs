import Test.QuickCheck

ps :: Int -> Int
ps 1 = 1 -- base case, only one arg, second is nil
ps 2 = 1 -- base case, only two args.
ps n = psHelper [1..(n-1)] 0 -- more than two args. 

psHelper :: [Int] -> Int -> Int
psHelper [] s = s
psHelper (x:[]) s = s + (ps x) * (ps x)
psHelper (x:y:[]) s = s + 2 * (ps x) * (ps y)
psHelper (x:xs) s = psHelper (init xs) (s + 2 * (ps x) * (ps (last xs)))

{- This operation can be coded with list comprehension which  is painfully
slow. -}
psWithList :: Int -> Int
psWithList 1 = 1
psWithList 2 = 1
psWithList n = sum [((psWithList x) * (psWithList (n-x))) | x <- [1..(n-1)]]


sendMoreMoney 
    = [[('s',s) ,('e', e),('n',n),('d',d),('m',m),('o',o),('r',r),('y',y)] | 
        s <- [8,9] , e <- [0..9], n <- [0..9], d <-[0..9], m <- [1]
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





listGiven = [(x, y+z) | x <-[1..10], y <-[1..x], z <- [1..y]]

listA m = map (\n -> (m,n))(concat (map (\y -> [1+y..y+y]) [1..m]))
listMine = concat (map (\x -> (listA x)) [1..10])

prop_equal = listGiven == listMine

{- case 1 -}
data Btree1 a = Null | Node1 a (Btree1 a) (Btree1 a) 
    deriving (Show, Eq)

treeBFold1 :: (a -> b -> b -> b) -> b -> Btree1 a -> b
treeBFold1 _ e Null = e
treeBFold1 f e (Node1 x l r)
               = f x (treeBFold1 f e l) (treeBFold1 f e r)



data Btree2 a = Leaf a | Node2 (Btree2 a) (Btree2 a)
    deriving (Show, Eq)

treeBFold2 :: (b -> b -> b) -> (a -> b) -> b -> Btree2 a -> b
treeBFold2 _ g (Leaf x) = g x
treeBFold2 f g (Node2 l r) = f (treeBFold2 f g l) (treeBFold2 f g r)
