import GetPrograms
import ComparePrograms as CP
import Data.Map as M
import Control.Monad (liftM)

homeDir = "/home/dilawar/Works/hpc21/2012ee677/Assignment01/Submissions"

main = do
  myPrograms <- listPrograms [".py"] homeDir
  print myPrograms
  let result = CP.processPrograms myPrograms
  print (length result)
  putStrLn "Done"

