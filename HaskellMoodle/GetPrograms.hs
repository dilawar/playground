module GetPrograms where 

import System.Directory
import System.FilePath 
import System.FilePath.GlobPattern
import Control.Monad (forM, liftM)
import DilString
import qualified Data.Map as M
import Data.Either.Utils (forceEither)
import System.Directory 
import Control.Monad (liftM)
import Control.Monad.Error 
import Data.ConfigFile as CF



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
        
{-
stList = do (studentList1 homeDir >>= \(Just list) -> return list)
-}

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
 - in a directory (recursively). Arg id is an associated id with topDir.
 -}
getContentRecursively (id, topDir) = do 
    names <- getDirectoryContents topDir
    let properNames = filter (`notElem` [".", ".."]) names 
    paths <- forM properNames $ \name -> do 
        let path = topDir </> name 
        isDirectory <- doesDirectoryExist path  
        if isDirectory 
            then getContentRecursively (id, path)
            else return [(id, path)]
    return (concat paths)

{- This function list all files present in a list of directory. Each directory
 - belongs to a student. 
 -}
getStudentFiles topDir = do 
    students <- studentList topDir
    let properStudents = filter (`notElem` [".", ".."]) students 
    let mapStudent = M.empty 
    dirs <- forM properStudents $ \name -> do 
        let path = topDir </> name 
        return (name, path) -- name is id for getContentRecursively function.
    files <- forM dirs (getContentRecursively)
    return (concat files)

{-
buildMap studentDataMap xs = foldr (insertIntoMap) (M.empty) xs where 
    insertIntoMap path = M.insertWith (getKey path) (getFile path)
    getKey path = head (split homeDir path)
    getFile path = split homeDir path
-}

{- 
 - Now from students each file, we need to filter out files of similar
 - extentions.
 -}
{-
getFilesWithExtention :: [String] -> IO [FilePath] -> IO [FilePath] -- (M.Map String FilePath)
getFilesWithExtention pat listFiles = do 
   -- let mapPrograms = M.empty 
    list <- listFiles
    let properFile = filter (\x -> match pat (takeExtension x)) list where
        match xs fileExtension = or $ map (== fileExtension) xs
    return (properFile)
-}
getFilesWithExtention :: [String] -> IO [(String, FilePath)] -> IO [(String, FilePath)] -- (M.Map String FilePath)
getFilesWithExtention pat listFiles = do 
   -- let mapPrograms = M.empty 
    list <- listFiles
    let properFile = filter (\(y,x) -> match pat (takeExtension x)) list where
        match fileName fileExtension = or $ map (== fileExtension) fileName
    return (properFile)


{- This function will list out all vhdl files in a Data.Map  " -}
listPrograms pat topDir = do 
    -- Note that a single * does not match directory separator / .
    let listfiles = getStudentFiles topDir
    vhdlFiles <- getFilesWithExtention pat (listfiles)
    let mapFiles = M.fromListWith (\x y->x++"<->"++y) vhdlFiles
    let message =  "Total "++show (M.size mapFiles)++" programs found."
    putStrLn message
    return mapFiles

{- get all programs according to the list -}
getAllPrograms global 
    | lang == "python" = do 
                            programs <- listPrograms ["*.py"] dir
                            return programs
    | otherwise = do 
                    putStrLn "This langauge is not supported."
                    return $ M.fromList [] 
    where 
        lang = forceEither $ CF.get global "DEFAULT" "language" 
        dir = forceEither $ CF.get global "DEFAULT" "dir"
