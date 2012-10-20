{-# LANGUAGE OverloadedStrings #-}
import Network.HTTP.Conduit 

-- The streaming interface uses conduits 
import Data.Conduit 
import Data.Conduit.Binary (sinkFile)

import qualified Data.ByteString.Lazy as L
import Control.Monad.IO.Class (liftIO)
import Text.Html

url = "http://moodle.iitb.ac.in/login/index.php"

main :: IO ()
main = do 
    case parseUrl url of 
        Nothing -> putStrLn "Invalid url"
        Just req -> withManager $ \manager -> do 
            Response _ _ lbs <- httpLbs req manager 
            (requestBody lbs) 

