import System.Directory
import System.FilePath ((</>))
import Control.Monad (forM, liftM)
import qualified Data.Map as M

homeDir = "/home/dilawar/Works/myrepo/Courses/VLSIDesignLab/Assignment-1 Submission/"

{- 
 - Get subdirectories of a dirctory. If the directory does not exists then
 - return an empty string. 
 -}
studentList dir = do 
    dirExists <- doesDirectoryExist dir
    if dirExists 
        then do
            stList <- getDirectoryContents dir
            return stList
        else do
            return [""::FilePath]
            
studentList1 dir =
    doesDirectoryExist dir >>= \x -> 
        if x then 
            getDirectoryContents dir >>= 
            (\ds ->return (Just ds))
            else 
                return Nothing
        

stList = do (studentList1 homeDir >>= \(Just list) -> return list)

{-
-- Now for each student we need to get all files and save them in a dictionary
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
-}

{-
 - Following function is like unix find utility. It returns all files present
 - in a directory (recursively).
 -}
getContentRecursively topDir = do 
    names <- getDirectoryContents topDir
    let properNames = filter (`notElem` [".", ".."]) names 
    paths <- forM properNames $ \name -> do 
        let path = topDir </> name 
        isDirectory <- doesDirectoryExist path 
        if isDirectory 
            then getContentRecursively path 
            else return [path]
    return (concat paths)

{- This function list all files present in a list of directory. Each directory
 - belongs to a student. 
 -}
getStudentFiles topDir = do 
    students <- studentList topDir
    dirs <- forM students $ \name -> do 
        let path = topDir </> name 
        return path 
    files <- forM dirs getContentRecursively
    return files


{- 
 - Now from students each file, we need to filter out files of similar
 - extentions.
 -}
getFilesWithExtention ext list = do 
    file <- forM list $ (liftM . filter ) hasExtension ".vhd"
    return file

