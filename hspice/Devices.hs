module Devices where 

-- Node is a point in fabric. 
data Node = Node {node :: (Int, Int)} deriving (Show, Eq) 

-- Wire is a list of Nodes which are connected. 
data Wire = Wire { wire :: [Node] } deriving (Show, Eq)

-- Fabric has devices and wires. It can be used to draw the circuit.
data Fabric = Fabric {network :: [Device], connection :: [Wire] } deriving Show 

-- This is port 
data Port = Port {
    portID :: String
    , position :: Node
    , voltage :: Float 
    , current :: Float 
    } deriving (Show, Eq)

-- Device 
data DeviceType = Res 
    | Cap 
    | Ind 
    | Mos 
    | Fet 
    | Dio 
    | Zen
    deriving (Show)


data Device = Device {
    id :: Int
    , type :: DeviceType
    , postition :: Node
    , ports :: ([Port], [Port])
    , parameters :: [String]
    }  deriving (Show, Eq)
