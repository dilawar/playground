module Sniffer where 
import Global as G
import Configuration as C
import GetPrograms
import ComparePrograms as CP
import Data.Map as M
import System.Directory 
import Control.Monad (liftM)

homeDir = "/home/dilawar/Works/hpc21/2012ee677/Assignment01/Submissions"
main = do
  home <- getHomeDirectory
  C.parseConfigFile (home++"/.snifferrc")
  myPrograms <- listPrograms [".py"] homeDir
  let progsToCompare = CP.processPrograms myPrograms
  let f = (head progsToCompare)
  result <- CP.compareTwoPrograms f
  putStrLn "Over"


