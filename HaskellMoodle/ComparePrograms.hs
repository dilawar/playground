module ComparePrograms where 
import System.IO
import Data.Map (toList)
import Data.List.Split (splitOn)
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


compareTwoPrograms (f1, f2) = do 
  prog1 <- readFile f1
  prog2 <- readFile f2

  putStrLn "Comparing two programs"
