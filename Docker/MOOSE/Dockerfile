FROM opensuse/leap
RUN zypper ref
RUN zypper install -y gcc-c++ 
RUN zypper install -y gsl-devel 
RUN zypper install -y boost-devel 
RUN zypper install -y ctags vim
RUN zypper install -y git cmake tmux
RUN zypper install -y python-devel python-numpy-devel python-matplotlib
RUN git clone https://dilawar@github.com/dilawar/moose-core ~/moose-core
RUN git clone https://dilawar@github.com/dilawar/vim ~/.vim --recursive 
RUN git clone https://dilawar@github.com/dilawar/Scripts ~/Scripts
