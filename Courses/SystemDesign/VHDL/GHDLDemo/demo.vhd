-- These are standard libraries one HAS TO include. 
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;

-- WORL library is where all of your current designs are stored. 
-- It is useful to include it.

USE WORK.ALL;

-- VHDL does not differentiate between lower-case and upper-case words. 
ENTITY dff IS 
  PORT(
        a, b : IN BIT;
        reset : IN BIT;
        clk : IN BIT;
        q   : OUT BIT
      );
END ENTITY dff;

-- Structural architecture
ARCHITECTURE structural OF dff IS 
  -- Declare components.
  COMPONENT and2
    port(in1, in2 : in bit;
        out1 : out bit
      );
  end COMPONENT;

  COMPONENT or2
    port(in1, in2 : in bit;
         out1 : out bit
       );
  end COMPONENT;

  COMPONENT not1 
    port(in1 : in bit;
        out1 : out bit 
      );
  end COMPONENT;

  COMPONENT dff 
    port(d : IN BIT;
        clk : IN BIT;
        reset : IN BIT;
        q : OUT BIT
      );
  END COMPONENT;

  -- Local signal (like local variables in C).
  signal andOut, notOut : bit;
  signal orOut : bit;

BEGIN 
  -- Now inside the architecture, describe the structure of model.
  A1 : and2 port map(a, b, andOut);
  N1 : not1 port map(b, notOut);
  O1 : or2 port map(andOut, notOut, orOut);
  D1 : dff port map(orOut, clk, reset, q);

END structural;

