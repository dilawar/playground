-- These are standard libraries one HAS TO include. 
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL
-- WORL library is where all of your current designs are stored. 
-- It is useful to include it.
USE WORK.ALL;

-- VHDL does not differentiate between lower-case and upper-case words. 
ENTITY dff IS 
  PORT(
        a, b : IN BIT;
        reset : IN BIT;
        clk : IN BIT;
        out   : OUT BIT
      );
END ENTITY dff;
