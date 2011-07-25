// Scilab file
// Top level script file to solve a circuit using MNA method which I do not like
// very much.

// See respective function files for more details.
// Algorithm implemented is standard MNA method.

// Execute file to load function definition.
exec('./generateMatrix.sci');

// Make sure following file exists.
[matCoeff, matSource, listNodes, nV] = generateMatrix('./myCircuit');
//disp(matCoeff);
//disp(matSource);
//disp(listNodes);
 // solve these equations. matCoeff*x= matSource.
[ansNodes] = linsolve(matCoeff, -matSource);

disp('Node potentials.')
// Display the results.
n = length(length(listNodes));
for i = 1 : n
    mprintf("Node %s votage is : %f\n", listNodes(i), ansNodes(i));
end; 
disp('Current through voltage sources.');
for i = n+1 : length(ansNodes),
    mprintf("\nCurrent through voltage source (%s, %s) is : %f", nV(i-n),...
    nV(i-n+1), ansNodes(i));
end;

// This ends our endeavor.
exit();
