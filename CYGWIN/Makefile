all : ./test.exe test.mingw.exe


%.exe : %.cpp
	g++ -static -o $@ -Wall $<

%.mingw.exe : %.cpp
	x86_64-w64-mingw32-g++.exe -o $@ -Wall $<
