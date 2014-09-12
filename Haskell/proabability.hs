import qualified Numeric.Probability.Distribution as Dist
import qualified Numeric.Probability.Random as Rnd
import Numeric.Probability.Distribution ((??), )
import Numeric.Probability.Simulation ((~.), )

import Numeric.Probability.Percentage (Dist)

import Control.Monad.Trans.State (StateT(StateT, runStateT), evalStateT, )
import Control.Monad (liftM2, replicateM, )

import qualified Data.List.HT as ListHT
import System.Random (Random)


type Spread a = [a] -> Dist a

-- Throw a die 
die = Dist.uniform [1..6]

-- A function which either adds or does not add to a number
-- Choose which equal probability eitehr x or (x+1)
succOrId x = Dist.choose 0.5 x (x+1)
