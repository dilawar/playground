module Global where 
import Control.Monad.State
import Control.Monad.Reader

data AppConfig = AppConfig {
  language :: String,
  regex :: String 
} deriving (Show)

global = AppConfig { language = "" 
    , regex = ""
}

setLanguage lang = global { language = lang }
