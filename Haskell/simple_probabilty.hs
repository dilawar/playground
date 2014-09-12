import qualified Numeric.Probability.Distribution as Dist
import qualified Numeric.Probability.Transition as Tran
import qualified Numeric.Probability.Random as Random
import qualified Numeric.Probability.Object as Obj
import qualified System.Random as Rnd

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
