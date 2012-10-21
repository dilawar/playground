module ComparePrograms where 
import Data.Map (toList, empty, insert)
import Data.Char
import Data.List.Split (splitOn)
import qualified Data.ByteString as B

--import Language as L

processPrograms programsMap = compareProgLists (toList programsMap)

compareProgLists :: [(String, String)] -> [(String, String)]
compareProgLists [] = []
compareProgLists (x:[]) = [] 
compareProgLists (x:xs) = concat (map (\y -> compareTwoStudents x y) xs) ++ compareProgLists xs
  where 
    compareTwoStudents :: (String, String) -> (String, String) -> [(String, String)]
    compareTwoStudents (student1, prog1) (student2, prog2)
              = compareListOfPrograms (splitOn "<->" prog1) (splitOn "<->" prog2)

compareListOfPrograms :: [String] -> [String] -> [(String, String)]
compareListOfPrograms [] _ = []
compareListOfPrograms _ [] = []
compareListOfPrograms (p1:p1s) p2s
  = (map (\y -> programToCompare p1 y) p2s ++ compareListOfPrograms p1s p2s)
    where programToCompare p1 p2 = (p1, p2)


{-
 - Format the Byte Strings. Remove lines, whitespaces, etc. 
 -}
formatText text =  B.filter(/= 0) (B.map (f) text) where 
    f x | x == (fromIntegral (ord '\n')) = 0
        | x == (fromIntegral (ord ' ')) = 0
        | x == (fromIntegral (ord '\t')) = 0
        | otherwise = x
                
{- Process results after comparing two text stream -}
processText t1 t2 = longestSubSequence (B.unpack t1) (B.unpack t2) [] empty

longestSubSequence (x:xs) (y:ys) seq map 
    | x == y = longestSubSequence (x:seq) 
  

compareTwoPrograms (f1, f2) global = do 
  prog1 <- B.readFile f1
  prog2 <- B.readFile f2
  let text1 = formatText prog1
  let text2 = formatText prog2
  let result = processText text1 text2
  print result
  putStrLn "Comparing two programs"
