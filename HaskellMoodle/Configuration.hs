module Configuration where 
import Database.HDBC 
import Database.HDBC.Sqlite3
import Data.List.Split (splitOn)
import Data.Text as T

parseConfigFile fileName = do
  fp <- readFile fileName 
  updateDB (pack fp)
  putStrLn "Config file loaded."

updateDB configText = do
  insertLineIntoDataBase (T.lines configText)
  putStrLn "Updating database."

insertLineIntoDataBase :: [Text] -> IO ()
insertLineIntoDataBase [] = return ()
insertLineIntoDataBase lines = do 
  putStrLn "Over"
