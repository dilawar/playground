import GetPrograms
import ComparePrograms as CP
import Data.Map as M
import Control.Monad (liftM)

homeDir = "/home/dilawar/Works/myrepo/Courses/VLSIDesignLab/Assignment-1 Submission/"

main = do
  myVHDLPrograms <- listPrograms [".vhd", ".vhdl"] homeDir
  let result = CP.processPrograms myVHDLPrograms
  print (length result)
  putStrLn "Done"

