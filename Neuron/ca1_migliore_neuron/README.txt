Hippocampal CA1 pyramidal neuron model from the paper 
M.Migliore, D.A Hoffman, J.C. Magee and D. Johnston 
Role of an A-type K+ conductance in the back-propagation of
action potentials in the dendrites of hippocampal pyramidal neurons
J. Comput. Neurosci. 7, 5-15, 1999.

Different kinetics are used for proximal and distal dendritic 
KA channels, with increasing density with distance from the soma.
The kinetics for the Na conductance includes a gate variable 
for the slow inactivation.

To compile the mod files on a unix system use the command nrnivmodl.
Under Windows use the "mknrndll DOS box" from the NEURON program menu
and follow on-screen instructions.

running the simulation hoc files with the command

nrngui fig_1a.hoc
or
nrngui fig_1c.hoc

will generate the simulations shown in Fig.1A and Fig.1C of the
paper, respectively.

Questions on how to use this model should be directed to
michele.migliore@pa.ibf.cnr.it





