-- This example is from Haskell wiki 
-- http://www.haskell.org/haskellwiki/Random_Processes

import Data.RandProc 

-- Here comes a fair coin

fairCoin = ProbSpace 
    [ point 0.0, point 1.0 ]
    [ Measure [Empty] 0, Measure [point 0] 0.5
        , Measure [point 1] 0.5, Measure [point 0, point 1] 1.0]
