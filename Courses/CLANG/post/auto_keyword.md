2011 standard of C++ has many useful feature. Some additions are just syntactic
sugar to make coding easier in c++, few are new additions.  Standard template
library (STL) has been enhanced; regular expressions are borrowed from
boost::regex and there is proposal to include graph in STL. GNU <a
href="http://gcc.gnu.org/projects/cxx0x.html"> GCC 4.7+</a> supports many of 
these new features. You can enable them by using `--std=c++0x` or `--std=c++11`. 

One of my favorites is following (other one is `labda` which is borrowed from
functional programming which I do not include here in this brief note.)
  

*Keyword auto*

This is different from `auto` in C which is a storage class specifier. `auto` in
C tells compiler that place this variable in a register of processor whenever
possible because I am going to use this variable frequently; it will save me
some time. In 2011 std of C++, it tells compiler: I am too busy to write the
type of variable myself, could you please figure it out for me by looking at the
right hand side of the expression. 


For example, by writing `int a = 5;` I tell compiler that my `a` has the type
`int`; by writing `auto a = 5`, I request compiler to infer it for me by looking
at the RHS or expression i.e. 5 (Is it `int`, `unsigned`, or `long`?). If
compiler can, it will; when it can't it would raise an error. 

Now this example is not very convincing.  Keyword `auto` can be incredibly
useful when you are using templates or using containers.

Let's iterate over a container.

~~~~~
  // Declare a set of int 
  set<int> mySet;
  
  // Fill this set here 

  // Now iterator over set.
  set<int>::iterator iter;
  for(iter = mySet.begin(); iter != mySet.end(); iter++)
  {
    int elem = *iter;
    // Do something with elem.
  }
~~~~~

Rewrite it with using `auto`

~~~~~
  // Declare a set of int 
  set<int> mySet;
  
  // Fill this set here 

  // Now iterator over set.
  for(auto iter = mySet.begin(); iter != mySet.end(); iter++)
  {
    int elem = *iter;
    // Do something with elem.
  }
~~~~~~

Saved me a line, big deal. Now consider this.

~~~~~~
   // Declare a set of int 
  set<int> mySet;
  
  // Fill this set here 

  // Now iterator over set.
  for(auto elem : mySet) { // Do something with elem }
~~~~~

 
Let's take another example from boost::graph library.

~~~~~~
  // flow_graph_t is declared somewhere else as a type of graph
  flow_graph_t flowGraph;

  // Without auto I have to write something like this to access any vertex of
  // graph.
  flow_graph_t::vertex_descriptor v = vertex(0, flowGraph); // 0'th vertex.

  // With auto I can do something similar like this.
  auto v = vertex(0, flowGraph);

~~~~~~

To much of `auto`ing will make the code less readable.
