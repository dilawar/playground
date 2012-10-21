module Sniffer where 
import GetPrograms as GP
import ComparePrograms as CP
import Data.Map as M
import Data.Either.Utils (forceEither)
import System.Directory 
import Control.Monad (liftM)
import Control.Monad.Error 
import Data.ConfigFile as CF

main = do
  -- Get the home directory. We have configuration file here.
  home <- getHomeDirectory
  -- read the configuration file.
  val <- CF.readfile CF.emptyCP (home++"/.snifferrc")
  let global = forceEither val
  -- Now get all the programs in directory
  myPrograms <- GP.getAllPrograms global
  let progsToCompare = CP.processPrograms myPrograms
  let messgae =  " ++ Total "++show (length progsToCompare)++" comparisons." 
  putStrLn messgae
  -- Compare any two programs and verify the result.
  let f = (head progsToCompare)
  result <- CP.compareTwoPrograms f
  putStrLn "Over"

