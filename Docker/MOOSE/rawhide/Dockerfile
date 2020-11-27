# dilawars/moose-opensuse
FROM fedora:rawhide
RUN dnf update
RUN dnf install -y gcc-c++ gsl-devel ctags vim cmake python3-devel python-numpy git
WORKDIR /root
RUN git clone https://dilawar@github.com/dilawar/moose-core ~/moose-core
RUN git clone https://dilawar@github.com/dilawar/vim ~/.vim --recursive 
