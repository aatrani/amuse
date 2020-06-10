# standard amuse configuration include
# config.mk will be made after ./configure has run
AMUSE_DIR?=$(shell amusifier --get-amuse-dir)
-include $(AMUSE_DIR)/config.mk

MPICXX   ?= mpicxx

CFLAGS   += -Wall -g
#CXXFLAGS += $(CFLAGS)
LDFLAGS  += -lm $(MUSE_LD_FLAGS)

OBJS = interface.o


TSUNAMI_SRC_DIR = $(AMUSE_DIR)/src/amuse/community/tsunami/tsunamisrc
TSUNAMI_INCLUDES = -I$(TSUNAMI_SRC_DIR)/lib/utils/ -I$(TSUNAMI_SRC_DIR)/lib/ARchain/

TSUNAMI_BUILDDIR = $(TSUNAMI_SRC_DIR)/build
TSUNAMI_LIB = $(TSUNAMI_BUILDDIR)/lib/libbase.a


CMAKE_DEPS = $(TSUNAMI_SRC_DIR)/CMakeLists.txt
CMAKE_GENERATOR ?= Unix Makefiles

CXXFLAGS += $(TSUNAMI_INCLUDES)

all: tsunami_worker

clean:
	$(RM) -rf __pycache__
	$(RM) -f *.so *.o *.pyc worker_code.cc worker_code.h
	$(RM) *~ tsunami_worker worker_code.cc
	make -C $(TSUNAMI_BUILDDIR) clean

distclean: clean
	make -C $(TSUNAMI_BUILDDIR) distclean

$(TSUNAMI_LIB):
	cmake -S $(TSUNAMI_SRC_DIR) -B $(TSUNAMI_BUILDDIR) -Damuse=on  -DCMAKE_CXX_COMPILER="$(CXX)"  -DCMAKE_CXX_FLAGS="$(CXXFLAGS)" -DCMAKE_BUILD_TYPE=Amuse -G "$(CMAKE_GENERATOR)"
	make -C $(TSUNAMI_BUILDDIR) all

worker_code.cc: interface.py
	$(CODE_GENERATOR) --type=c interface.py TsunamiInterface -o $@

worker_code.h: interface.py
	$(CODE_GENERATOR) --type=H interface.py TsunamiInterface -o $@

tsunami_worker: worker_code.cc worker_code.h $(TSUNAMI_LIB) $(OBJS)
	$(MPICXX) $(CXXFLAGS) $< $(OBJS) $(TSUNAMI_LIB) -o $@

.cc.o: $<
	$(CXX) $(CXXFLAGS) -c -o $@ $<
