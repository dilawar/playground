// Dilawar, dilawar@ee.iitb.ac.in
// Sep 18, 2010
// This Scilab function should parse file describing a circuit and should return
// list containing V, I and R.
// Only a circuit which has resistance, voltage
// sources and current sources as elements are dealt with 
//. We do not take responsibility for
// any harm caused by using this script. Nonetheless my best wishes.

///////////////////////////////////////////////////////////////////////////////////
//
// About : Parse a file containing circuit elements and return a list containing
// structure. This structure holds information about the current, voltage, and
// resistance available in the circuit.
//
///////////////////////////////////////////////////////////////////////////////////
function [voltSource, curSource, valResistance, number] = parseCircuitFile(myCircuitFilePath)

//Error checking.
[lhs, rhs] = argn(0)
if( rhs == 0) then
    error("Expecting file path.");
end

// Open file.
[fd, err] = mopen(myCircuitFilePath, "r");

// Initialize numbers of entity in file.
noOfcomments = 0;
noOfVoltageSources = 0;
noOfCurrentSources = 0;
noOfResistance = 0;

// Create generic structure to store the data.This is not to be stored. Just an
// overview how it should be used.
stComponent = struct('type', 'V_I_R', 'node1', 'nX', 'node0', 'nY', 'val', 00)

// create lists to store data for each type of element.
curSource= list();
voltSource = list();
valResistance = list();


// Now we parse the file to get the components.
while 0 == meof(fd) then // till end of file is not reached.

	line = mgetl(fd, 1); // get a line.
	if 0 == length(line) 
		// empty line, break. Else needed a mechanism to handle this bug.
		break;
	
	else		
		ch = part(line, 1); // get first letter of line.
		if ch == "#" then
			//disp('Comment found.');
			// Do something.
			noOfcomments = noOfcomments + 1;

		elseif ch == "I" then
			//disp('We got a current source.');

			noOfCurrentSources = noOfCurrentSources + 1;

			n = length(line);
			
			//disp(n);
			// Get the name of the current source.
			countSpace = 0;
			j = 0;
		  for i = 1: n,
				//disp('Inside for.', i);
				if part(line, i) == " " then
					//disp('Found space.');
					
					if 0 == countSpace then // first space delimit names.
			 	 		nameCurSource = part(line, 2:i-1);
				 		countSpace = countSpace + 1;
				 		//disp(nameCurSource);
				 		j = i; // remember the location of previous space.
					
				  elseif	1 == countSpace then // we got a node.
						upperNode = part(line, j+1:i-1);
				 		countSpace = countSpace + 1;
						j = i;
						//disp(upperNode);
				
					elseif 2 == countSpace then // we got a node
						lowerNode = part(line, j+1:i-1);
						countSpace = countSpace + 1;
						j = i;
						//disp(lowerNode);
					end; // inside if-elseif end here.
				end; // outside if ends here.

				// Now there is no space left at the end of line. So we can not read
				// value of the component using this algorithm. We use ';' to read
				// this value.

				if part(line, i) == ";" then // we got a value, uhuu
					val = part(line, j+1:i-1);
					countSpace = countSpace + 1;
					j = i;
					//disp('Value is:', val);
				end;

			end; // for-loop ends here. 

			// Put all the data into matrix.
			stComponent.type = "I"; // this is a current source.
			stComponent.name = nameCurSource;
			stComponent.node1 = upperNode;
			stComponent.node0 = lowerNode;
			stComponent.val = val;
			
			// This list will contain information in this order. Index [1] stores
			// a matrix in which entries specify that stored is an struct. Index[2]
			// will provide with a matrix [1, 1] which I am not sure what it is.
			// Index[3] is the type of the component. I for current source, V for
			// voltage, R for resistance. Index[4] is name of the component. Index[5]
			// is the upper node of connection of this component in circuit and
			// Index[6] is the lower node. Index[7] is the corresponding value in
			// string which must be converted into double before use.  
			curSource = lstcat(curSource, stComponent);
		
		elseif ch == "R" then
			//disp('We got a resistance.');
			// Do something.
			noOfResistance = noOfResistance + 1;

			n = length(line);
			
			countSpace = 0;
			j = 0;
		  for i = 1: n,
				//disp('Inside for.', i);
				if part(line, i) == " " then
					//disp('Found space.');
					
					if 0 == countSpace then // first space delimit names.
			 	 		nameResistance = part(line, 2:i-1);
				 		countSpace = countSpace + 1;
				 		//disp(nameResistance);
				 		j = i; // remember the location of previous space.
					
				  elseif	1 == countSpace then // we got a node.
						upperNode = part(line, j+1:i-1);
				 		countSpace = countSpace + 1;
						j = i;
						//disp(upperNode);
				
					elseif 2 == countSpace then // we got a node
						lowerNode = part(line, j+1:i-1);
						countSpace = countSpace + 1;
						j = i;
						//disp(lowerNode);
					end; // inside if-elseif end here.
				end; // outside if ends here.

				// Now there is no space left at the end of line. So we can not read
				// value of the component using this algorithm. We use ';' to read
				// this value.

				if part(line, i) == ";" then // we got a value, uhuu
					val = part(line, j+1:i-1);
					countSpace = countSpace + 1;
					j = i;
					//disp('Value is:', val);
				end;

			end; // for-loop ends here. 

			// Put all the data into matrix.
			stComponent.type = "R"; // this is a resistance.
			stComponent.name = nameResistance;
			stComponent.node1 = upperNode;
			stComponent.node0 = lowerNode;
			stComponent.val = val;
			
			// This list will contain information in this order. Index [1] stores
			// a matrix in which entries specify that stored is an struct. Index[2]
			// will provide with a matrix [1, 1] which I am not sure what it is.
			// Index[3] is the type of the component. I for current source, V for
			// voltage, R for resistance. Index[4] is name of the component. Index[5]
			// is the upper node of connection of this component in circuit and
			// Index[6] is the lower node. Index[7] is the corresponding value of the
			// component.
     valResistance = lstcat(valResistance, stComponent);
	

		elseif ch == "V" then
			//disp('We got a voltage source.');
			// Do something.
			noOfVoltageSources = noOfVoltageSources + 1;

			n = length(line);
			
			//disp(n);
			// Get the name of the current source.
			countSpace = 0;
			j = 0;
		  for i = 1: n,
				//disp('Inside for.', i);
				if part(line, i) == " " then
					//disp('Found space.');
					
					if 0 == countSpace then // first space delimit names.
			 	 		nameVoltSource = part(line, 2:i-1);
				 		countSpace = countSpace + 1;
				 		//disp(nameVoltSource);
				 		j = i; // remember the location of previous space.
					
				  elseif	1 == countSpace then // we got a node.
						upperNode = part(line, j+1:i-1);
				 		countSpace = countSpace + 1;
						j = i;
						//disp(upperNode);
				
					elseif 2 == countSpace then // we got a node
						lowerNode = part(line, j+1:i-1);
						countSpace = countSpace + 1;
						j = i;
						//disp(lowerNode);
					end; // inside if-elseif end here.
				end; // outside if ends here.

				// Now there is no space left at the end of line. So we can not read
				// value of the component using this algorithm. We use ';' to read
				// this value.

				if part(line, i) == ";" then // we got a value, uhuu
					val = part(line, j+1:i-1);
					countSpace = countSpace + 1;
					j = i;
					//disp('Value is:', val);
				end;

			end; // for-loop ends here. 

			// Put all the data into matrix.
			stComponent.type = "V"; // this is a voltage source.
			stComponent.name = nameVoltSource;
			stComponent.node1 = upperNode;
			stComponent.node0 = lowerNode;
			stComponent.val = val;
			
			// This list will contain information in this order. Index [1] stores
			// a matrix in which entries specify that stored is an struct. Index[2]
			// will provide with a matrix [1, 1] which I am not sure what it is.
			// Index[3] is the type of the component. I for current source, V for
			// voltage, R for resistance. Index[4] is name of the component. Index[5]
			// is the upper node of connection of this component in circuit and
			// Index[6] is the lower node. Index[7] is the corresponding value of the
			// component.  
			voltSource = lstcat(voltSource, stComponent);
	

		else	
			disp('Mayday. Alien found. Check your circuit file.');
			// Please do something
		end; // if elseif else ends here.
	end; //if else ends here.
end; // while ends here.
mclose(fd);
// return number of elements in circuit.
number = [noOfVoltageSources, noOfCurrentSources, noOfResistance];

endfunction
