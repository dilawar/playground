import System.Directory
import Control.Monad
import qualified Data.Map as M

homeDir = "/home/dilawar/Works/myrepo/Courses/VLSIDesignLab/Assignment-1 Submission/"

-- Get subdirectories of a dirctory. If the directory does not exists then
-- return Nothing.
studentList dir = do 
    dirExists <- doesDirectoryExist dir
    if dirExists then 
        do
            stList <- getDirectoryContents dir
            return (Just stList)
        else 
            do 
                return Nothing
            
studentList1 dir =
    doesDirectoryExist dir >>= \x -> 
        if x then 
            getDirectoryContents dir >>= 
            (\ds ->return (Just ds))
            else 
                return Nothing
        

stList = studentList1 homeDir

-- Now for each student we need to get all files and save them in a dictionary
--getStudentFiles :: Maybe (IO [FilePath]) -> IO [(FilePath, [FilePath])]
getStudentFiles dirs = do 
    setCurrentDirectory homeDir
    ds <- dirs 
    if (ds == Nothing) then do 
        return Nothing 
        else do 
            let Just (x:xs) = ds
            if xs == [] then  do
                files <- getDirectoryContents x
                return $ Just [(x, files)]
                else do
                    files <- getDirectoryContents x
                    return $ Just [(x, files)]
                    getStudentFiles (return (Just xs))


