# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR?=$(shell amusifier --get-amuse-dir)
-include $(AMUSE_DIR)/config.mk

MPICXX   ?= mpicxx

CFLAGS   += -Wall -g
#CXXFLAGS += $(CFLAGS)
LDFLAGS  += -lm $(MUSE_LD_FLAGS)

OBJS = interface.o

CODELIB = src/libtsunami.a

TSUNAMI_SRC_DIR = $(AMUSE_DIR)/src/amuse/community/tsunami/tsunamisrc
TSUNAMI_INCLUDES = -I$(TSUNAMI_SRC_DIR)/lib/utils/ -I$(TSUNAMI_SRC_DIR)/lib/ARchain/

TSUNAMI_BUILDDIR = $(TSUNAMI_SRC_DIR)/build
TSUNAMI_LD = $(TSUNAMI_BUILDDIR)/lib/libbase.a


CMAKE_DEPS = $(TSUNAMI_SRC_DIR)/CMakeLists.txt
CMAKE_GENERATOR ?= Unix Makefiles

CXXFLAGS += $(TSUNAMI_INCLUDES)

all: $(TSUNAMI_BUILDDIR)/Makefile tsunami_worker

$(TSUNAMI_BUILDDIR)/Makefile: $(CMAKE_DEPS)
	cd $(TSUNAMI_BUILDDIR) && cmake $(TSUNAMI_SRC_DIR) -Damuse=on  -DCMAKE_CXX_COMPILER="$(CXX)"  -DCMAKE_CXX_FLAGS="$(CXXFLAGS)" -DCMAKE_BUILD_TYPE=Amuse -G "$(CMAKE_GENERATOR)"
	cd $(TSUNAMI_BUILDDIR) && make

clean:
	$(RM) -r $(TSUNAMI_BUILDDIR)/*
	$(RM) -rf __pycache__
	$(RM) -f *.so *.o *.pyc worker_code.cc worker_code.h 
	$(RM) *~ tsunami_worker worker_code.cc
	make -C src clean

distclean: clean
	make -C src distclean

$(CODELIB):
	make -C src all

worker_code.cc: interface.py
	$(CODE_GENERATOR) --type=c interface.py TsunamiInterface -o $@

worker_code.h: interface.py
	$(CODE_GENERATOR) --type=H interface.py TsunamiInterface -o $@

tsunami_worker: worker_code.cc worker_code.h $(CODELIB) $(OBJS)
	$(MPICXX) $(CXXFLAGS) $< $(OBJS) $(TSUNAMI_LD) $(CODELIB) -o $@

.cc.o: $<
	$(CXX) $(CXXFLAGS) -c -o $@ $<
