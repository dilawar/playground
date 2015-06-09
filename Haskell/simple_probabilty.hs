import qualified Numeric.Probability.Distribution as Dist
import qualified Numeric.Probability.Transition as Tran
import qualified Numeric.Probability.Random as Random
import qualified Numeric.Probability.Object as Obj
import qualified System.Random as Rnd
import Control.Monad (liftM2)
import qualified Data.Map as M

type Die = Int
type Dist = Dist.T Rational

die :: Dist Die
die = Dist.uniform [1..6]

-- What is the probability of getting 2.
prob2 = (Dist.??) (==2) die

-- What is the probability of getting number n
prob n | n < 0 = error "Need a positive int value"
       | otherwise = (Dist.??) (==n) die


------
-- Now another example, lets create two indepedent die.

die1 = die
die2 = die

-- Now let's join these two distributions.

-- Roll a dice n times
{-dice :: Dist [Int]-}
dice 0 = Dist.certainly []

-- Computing Entropy of a distribution 
entropy dist = sum $ map( \x -> - x * logBase 2 x ) propabilities
    where 
        listOfdistribution = Dist.decons dist 
        events = Prelude.map (\x -> fst x) listOfdistribution
        propabilities = Prelude.map (\x -> snd x) listOfdistribution

-- Create two dice
twoDice :: Dist (Die, Die)
twoDice = liftM2 (,) die die

-- Now we can compute the probability distribution of getting various outcomes
-- i.e. Pr(S = s) where s \in [2,3..12].

oneDieSampleSpace :: [Die]
oneDieSampleSpace = [1..6]

twoDiceSampleSpace :: [(Die, Die)]
twoDiceSampleSpace = [ (x, y) | x <- oneDieSampleSpace, y <- oneDieSampleSpace ]

probilities = map (\x -> (fst x+snd x,(==x) Dist.?? twoDice)) twoDiceSampleSpace

-- This function computes the distribution of outcome when two fair dice are
-- thrown.
twoDiceDistribution = helper probilities M.empty 
    where 
        helper (x:xs) dist = helper xs $ M.insertWith (+) (fst x) (snd x) dist
        helper [] dist = dist
