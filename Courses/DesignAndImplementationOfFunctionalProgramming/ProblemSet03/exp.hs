primes = 2 : [ x | x <- [3..400], all (\p -> (mod x p) /= 0) primes]
