myLength :: [Int] -> Int
-- We have to give a 'initial value' to myCount which will replace [] in the
-- list. This is the reason why we have two arguments for the function myCount.
myLength = foldr myCount 0
    where 
        myCount :: Int -> Int -> Int
        myCount a n = n + 1

