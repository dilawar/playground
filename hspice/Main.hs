{-# LANGUAGE FlexibleContexts #-}
module Main where 

import Text.Parsec hiding (spaces)
import Text.Parsec.String (parseFromFile)
import Text.Parsec.Expr
import Text.Parsec.Language (emptyDef)
import System.Environment
import qualified Text.Parsec.Token as T

jeeraDef = emptyDef { 
    T.commentStart = "/*"
    , T.commentEnd = "*/"
    , T.commentLine = "//"
    , T.nestedComments = True
    , T.identStart     = letter <|> char '_'
    , T.identLetter    = alphaNum <|> oneOf "_'"
    , T.opStart        = T.opLetter emptyDef
    , T.opLetter       = oneOf ":!#$%&*+./<=>?@\\^|-~"
    , T.reservedOpNames= [":=", "="]
    , T.reservedNames  = [ "resistor"
                        , "capacitor"
                        , "inductor"
                        , "source"
                        , "pulse"
                        ]
    , T.caseSensitive  = True
}

lexer = T.makeTokenParser jeeraDef

spaces :: (Stream s m Char) => ParsecT s u m ()
spaces = skipMany1 space 

jeera = do
    stmt <- many1 (deviceDeclaration <|> networkComposition)
    return "Top rule"

deviceDeclaration = do
    deviceName 
    (string ":=") 
    deviceType 
    (char '{') 
    deviceParams 
    (char '}')
    return "DeviceType"

deviceName = do 
    (T.identifier lexer)
    return "Device name"

deviceType = do 
    (T.identifier lexer)
    return "Device type"

networkComposition = do
    deviceName 
    compositionOp 
    deviceName 
    return "Composition rule"

compositionOp = do 
    string "||" <|> string "--"
    return "Composition rule"


deviceParams = do 
    sepBy (char ',') (paramName >>  (char '=') >> (T.identifier lexer))
    return "Device parameters"

paramName = do
    (T.identifier lexer)
    return "Parameter name"


main :: IO()
main = do
    result <- parseFromFile jeera "./Tests/cir1.jeera"
    putStrLn "Done"
