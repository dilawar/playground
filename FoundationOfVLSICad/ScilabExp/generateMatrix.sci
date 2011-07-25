// Scilab file. 
// Funtion
// Dilawar Singh, Sepp 19, 2010.
//
// This script will compute the matrices required to solve the electric circuit
// as described in a text file. To generate the matrix we will use data
// structure returned by a function defined in parseCircuitFile.sce file.
//

// matM : coefficient matrix.
// matB : source matrix.
// listNodes : list having distince nodes at which equations are written.
// nodeV : nodes where voltage sources are attached.
// etc.
function [matM, matB, listNodes, nodeV] = generateMatrix(myFileName)
exec('./parseCircuitFile.sci');
// open file and parse the file.
[vS, iS, rS, numS] = parseCircuitFile(myFileName);
// We got all the sources.

// Build the matrix.
// calculate the no of voltage sources.
nV = numS(1);
// no of current source.
nI = numS(2);
// no of resistors
nR = numS(3);

////////////////////////////////////////////////// 
//To do : Extract the topology of the network here.

// First get the node lists.
nodeV = [];
nodeI = [];
nodeR = [];
// node with voltage source.
for j = 1 : nV,
    nodeV = [nodeV, vS((j-1)*7 + 4), vS((j-1)*7 + 5)];
end;
//nodes with current sources.
for j = 1 : nI,
    nodeI = [nodeI, iS((j-1)*7 + 4), iS((j-1)*7 + 5)];
end;
// nodes with resistance
for j = 1 : nR,
    nodeR = [nodeR, rS((j-1)*7 + 4), rS((j-1)*7 + 5)];
end;

// We can now have some sort of circuit topology.

// Extract nodes on which we need to write the nodal equations. This is
// neccessary since a node mostly have repeated entry due to more than one
// element incident to it.
// diffNodes store all such nodes.
// TODO : This is not an efficient implementation.
tempNodes = [nodeV, nodeI, nodeR];
diffNodes = []; // Different node
n = length(length(tempNodes));
i = 1;
allMatch = [];
while i < n then
    j = i +1;
    while j < n then
        if tempNodes(i) ~= tempNodes(j) then
            //disp('Dont Match');
            j = j + 1;
        else
            //disp('Match.');
            allMatch = [allMatch, j];
            tempNodes(j) = []; //Delete it.
            j = j;
            n = length(length(tempNodes));
        end;
    end;
    if length(allMatch) == 0 then
        diffNodes = [diffNodes, tempNodes(i)];
        i = i + 1;
    else
        for p = 1 : length(allMatch),
            tempNodes(j) = [];
        end;
        diffNodes = [diffNodes, tempNodes(i)];
        i = i + 1;
    end;
   n = length(length(tempNodes)); 
end;

// Discard n0 since by constrain this is our ground node.
// Now we can use any method to solve it. Either MNA or NAL-NBK methods.
// Here we use MNA since it will take less time to implement now.

// Now we will have numNodes + nV variables.
// Add all the resistance incident on one node. They will form the diagonal
// entries for matrix for node equations. Non-diagonal entries can also be
// generated inside this part only. But we give another block of code to make it
// look more straigtforward. Both of these loops should be merged into one for
// less time consumption.
matM = [];
diagM = [];
 // Remove n0 from the diff nodes and use it to build the conducatance matrices.
 // This way it is more natural. We could have ignored this node previously but
 // we keep it, just in case if we need it in future.
 listNodes = [];
 for i = 1 : length(length(diffNodes)),
     if diffNodes(i) ~= 'n0' then
         listNodes = [listNodes, diffNodes(i)];
     end;
 end;

 
numNodes = length(length(listNodes)); // total nodes excluding ground 'n0'.
for i = 1 : numNodes,
    diagR = 0;
    for p = 1 : (lstsize(rS)/7),
        if listNodes(i) == rS((p-1)*7 + 4) then
            diagR = diagR + 1/evstr(rS((p-1)*7 + 6)); // get the conductance.
        elseif listNodes(i) == rS((p-1)*7 + 5) then
            diagR = diagR + 1/evstr(rS((p-1)*7 + 6));
        end;
    end;
    matM(i, i) = diagR;  
end;
// Here we extract non-diagonal entries. Since matM should be symetrical about
// its diagonal. Life is slightly easy.
for i = 1 : numNodes,
    nonDiagR = 0;
    for  j = i+1 : numNodes,
        for p = 1 : lstsize(rS)/7,
            if listNodes(i) == rS((p-1)*7 + 4) then
                if listNodes(j) == rS((p-1)*7 + 5) then
                    nonDiagR = nonDiagR + 1/evstr(rS((p-1)*7 + 6)); // conductance.
                end;
            // it might happen that we have reversed the order of nodes while writing R.
            // Though, the way we are extracting the nodes, it should never happen. But
            // anyway if someone modifies a paet there should not be any bug here.   
            elseif listNodes(i) == rS((p-1)*7 + 5) then
                 if listNodes(j) == rS((p-1)*7 + 4) then
                    nonDiagR = nonDiagR + 1/evstr(rS((p-1)*7 + 6)); // conductance.
                end;
            end;
        end;
        matM(i, j) = -nonDiagR;
        matM(j, i) = -nonDiagR;
    end;
end;  

// Now we need to extend this matM with entries which came from voltage sources.
// Generate a column to be appended to matM for each voltage entry.
// Same time we push these values into matrix B which contains sources. Its
// dimenstion is listNodes+nV by 1.
matB = zeros(numNodes+nV, 1); // mat to hold sources.

for i = 1 : numNodes, // for each node check if there is a voltage source.
    colVoltS = zeros(numNodes,1);
    for j = i+1 : numNodes,
        for p = 1 : lstsize(vS)/7,
            if listNodes(i) == vS((p-1)*7 + 4) then // i is the first node.
                //disp('A voltage source node.');
                if listNodes(j) == vS((p-1)*7 + 5) then // j is the second node.
                    colVoltS(i, 1) = 1;
                    colVoltS(j, 1) = -1;
                    matB(numNodes+i, 1) = evstr(vS((p-1)*7 + 6)); // value V.
                    //disp(colVoltS, 'A');
                else // the second node is n0
                    colVoltS(i, 1) = 1;
                    //disp(colVoltS, 'B');
                    matB(numNodes+i, 1) = evstr(vS((p-1)*7 + 6)); // value V.
                end;
            end;
//            // To avaid reverse ordering of nodes.
//            elseif listNodes(i) == vS((p-1)*7 + 5) then // i is the first node.
//                if listNodes(j) == vS((p-1)*7 + 4) then // j is the second node.
//                    colVoltS(i, 1) = -1;
//                    colVoltS(j, 1) = 1;
//                else // the second node is n0
//                    colVoltS(i, 1) = 1;
//                end;
        end;
    end;
    //disp(colVoltS, 'D');
    // If this vector is non zero. Push it into matM.
    if rank(colVoltS) ~= 0 then
        n = length(matM(1,:));
        for i = 1 : length(colVoltS),
            //disp(length(colVoltS, 'A'));
            matM(i, n + 1) = colVoltS(i);
            matM(n + 1, i) = colVoltS(i);
        end;
    end; // our matrix is ready.
end;

// Final step. We have to push current source into source matrix (vector).
for i = 1 : numNodes, // for each node check if there is a current.
    curS = 0; // to hold current source values.
    for j = i+1 : numNodes,
        for p = 1 : lstsize(iS)/7,
            if listNodes(i) == iS((p-1)*7 + 4) then // i is the first node.
                //disp('A current source node.');
                if listNodes(j) == iS((p-1)*7 + 5) then // j is the second node.
                    curS = curS + evstr(iS((p-1)*7 + 6)); // value i.
                    matB(i, 1) = curS;
                    matB(j, 1) = -curS
                else // the second node is n0
                    curS = curS + evstr(iS((p-1)*7 + 6)); // value i.
                    matB(i, 1) = curS;
                end;
            end;
        end;
    end;
end;

// matM is our coefficient matrix. matB contains sources. Solve it.
msprintf("Your circuit contains %d current sources, %d voltage sources, and ...
%d resistance. PLEASE NOTE THAT at this point we do not check topology of ...
the circuit. Make sure your file describing your circuit is error free.", ...
nI, nV, nR);

endfunction;
