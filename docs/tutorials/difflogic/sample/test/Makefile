# Makefile for running the cocotb testbench on top.sv

TOPLEVEL_LANG = verilog # keep verilog even though top level is sv

# Specify top_level and all subsidary modules used in tb
VERILOG_SOURCES = $(shell pwd)/../rtl/*.sv
TOPLEVEL = top
MODULE = difflogic_mnist_full_tb
SIM ?= verilator
EXTRA_ARGS = --unroll-count 10000 --build-jobs 10

include $(shell cocotb-config --makefiles)/Makefile.sim
