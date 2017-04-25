# FlyCapture2Test makefile
# To compile the debug verison need to overwrite CXXFLAGS variable to include -ggdb
PROJECT_ROOT=../../
OPT_INC = ${PROJECT_ROOT}/common/make/common.mk
-include ${OPT_INC}
# Handle environment variables
ifeq ($(wildcard ${OPT_INC}),) 
	CC = g++
	ODIR = .obj/build${D}
	SDIR = .
	MKDIR = mkdir -p
	MV = mv
endif
BASE_NAME = FlyCapture2Test
NAME = ${BASE_NAME}${D}
INC = -I../../include -I/usr/include/flycapture
LIBS = -L../../lib -lflycapture${D} ${FC2_DEPS}
OUTDIR = ${PROJECT_ROOT}/bin

_OBJ = ${BASE_NAME}.o
SRC = $(_OBJ:.o=.cpp)
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

# Master rule
.PHONY: all
all: ${NAME}

# Output binary
${NAME}: ${OBJ}
	${CC} ${OBJ} -o ${NAME} ${LIBS}
	-@${MV} ${NAME} ${OUTDIR}/${NAME}

# Intermediate object files
${OBJ}: ${ODIR}/%.o : ${SDIR}/%.cpp
	@${MKDIR} ${ODIR}
	${CC} ${CFLAGS} ${LINUX_DEFINES} ${INC} -Wall -c $< -o $@

# Cleanup intermediate objects
.PHONY: clean_obj
clean_obj:
	rm -f ${OBJ}
	@echo "obj cleaned up!"

# Cleanup everything
.PHONY: clean
clean: clean_obj
	rm -f ${OUTDIR}/${NAME} ${OBJ}
	@echo "all cleaned up!"

