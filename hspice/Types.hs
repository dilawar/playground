module Types where 
import qualified Data.Map as M
import qualified Data.Graph as G

data DeviceType = Resistor
    | Capacitor
    | Inductor
    | Diode 
    | FET
    | MOSFET
    deriving (Show, Eq)

-- Device model. Currently dysfunctional.
data Model = NullModel 
    | Model  {
        description :: String 
    } deriving Show 

data Connection = Connection {
    inPorts :: [Device]
    , outPorts :: [Device]
} deriving Show 

data Device = Device {
    dname :: String
    , dvalue :: Double
    , dtype :: DeviceType  
    , connectionMap :: M.Map Device Connection
    , spiceRep :: String
    , model :: Model 
} deriving Show 

defR = Device "" 0.0 Resistor M.empty "R " NullModel 

-- This is our structure 
data Circuit = Circuit {
    name :: String
    , device :: [Device]
    , subckt :: [Circuit]
    , topology :: M.Map Device Connection
} deriving Show 


