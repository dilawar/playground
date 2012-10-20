module ComparePrograms where 
import Data.Map (toList)
import Data.List.Split (splitOn)

processPrograms programsMap = compareProgLists (toList programsMap)

compareProgLists :: [(String, String)] -> [(String, String)]
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
  = (map (\y -> compareTwoPrograms p1 y) p2s ++ compareListOfPrograms p1s p2s)

compareTwoPrograms p1 p2 = (p1, p2)
