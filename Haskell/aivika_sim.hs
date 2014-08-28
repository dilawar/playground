-- Example showing how to run simulation in haskell.

import Control.Monad.Trans
import Simulation.Aivika

meanUpTime = 1.0 

meanRepairTime = 0.5

specs = Specs {
    spcStartTime = 0.0,
    spcStopTime = 1000.0,
    spcDT = 1.0,
    spcMethod = RungeKutta4,
    spcGeneratorType = SimpleGenerator 
}

model :: Simulation Double 
model = do
    totalUpTime <- newRef 0.0
    let machineBroken :: Double -> Event ()
        machineBroken startUpTime = do
            finishUpTime <- liftDynamics time 
            modifyRef totalUpTime ( + (finishUpTime - startUpTime))
            repairTime <- liftParameter $ randomExponential meanRepairTime 
            -- enque a new event
            let t = finishUpTime + repairTime 
            enqueueEvent t machineRepaired 

        
        machineRepaired :: Event ()
        machineRepaired = do
            startUpTime <- liftDynamics time 
            upTime <- liftParameter $ randomExponential meanUpTime
            -- enqueue a new event 
            let t = startUpTime + upTime 
            enqueueEvent t $ machineBroken startUpTime 

    runEventInStartTime $ do 
        machineRepaired 
        machineRepaired 

    runEventInStopTime $ do 
        x <- readRef totalUpTime 
        y <- liftParameter stoptime 
        return $ x / (2 * y )

main = runSimulation model specs >>= print

