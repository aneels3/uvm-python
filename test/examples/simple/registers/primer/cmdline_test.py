#//
#// -------------------------------------------------------------
#//    Copyright 2004-2011 Synopsys, Inc.
#//    Copyright 2010 Mentor Graphics Corporation
#//    Copyright 2010-2011 Cadence Design Systems, Inc.
#//    Copyright 2019-2020 Tuomas Poikela (tpoikela)
#//    All Rights Reserved Worldwide
#//
#//    Licensed under the Apache License, Version 2.0 (the
#//    "License"); you may not use this file except in
#//    compliance with the License.  You may obtain a copy of
#//    the License at
#//
#//        http://www.apache.org/licenses/LICENSE-2.0
#//
#//    Unless required by applicable law or agreed to in
#//    writing, software distributed under the License is
#//    distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#//    CONDITIONS OF ANY KIND, either express or implied.  See
#//    the License for the specific language governing
#//    permissions and limitations under the License.
#// -------------------------------------------------------------
#//

import cocotb

from uvm.comps.uvm_test import UVMTest
from uvm import (UVMCoreService, sv, uvm_top, UVMCmdlineProcessor, UVMSequence)
from uvm.reg import (uvm_reg_sequence)
from uvm.macros import *
from tb_env import tb_env


class dut_reset_seq(UVMSequence):

    def __init__(self, name="dut_reset_seq"):
        super().__init__(name)
        self.tb_top = None

    @cocotb.coroutine
    def body(self):
        self.tb_top.rst = 1
        for i in range(5):
            yield RisingEdge(self.tb_top.clk)
        self.tb_top.rst = 0


uvm_object_utils(dut_reset_seq)


class cmdline_test(UVMTest):
    #
    #
    def __init__(self, name, parent):
        super().__init__(name, parent)


    @cocotb.coroutine
    def run_phase(self, phase):
        cs_ = UVMCoreService.get()
        env = None  # tb_env
        phase.raise_objection(self)
        arr = []
        if sv.cast(arr, uvm_top.find("env$"), tb_env):
            env = arr[0]

        # dut_reset_seq rst_seq
        rst_seq = dut_reset_seq.type_id.create("rst_seq", self)
        rst_seq.start(None)
        env.model.reset()

        # uvm_cmdline_processor
        opts = UVMCmdlineProcessor.get_inst()
        seq = None  # uvm_reg_sequence
        factory = cs_.get_factory()
        seq_name = []
        opts.get_arg_value("+UVM_REG_SEQ=", seq_name)
        print("+UVM_REG_SEQ plusarg is now " + seq_name[0])
        seq_name = seq_name[0]

        seq = factory.create_object_by_name(seq_name, self.get_full_name(), "seq")
        #print("Created obj is " + str(created_obj))
        #if not sv.cast(seq, created_obj, uvm_reg_sequence) or seq is None:
        #    uvm_fatal("TEST/CMD/BADSEQ", "Sequence " + seq_name + " is not a known sequence " + str(seq))
        seq.model = env.model
        yield seq.start(None)
        phase.drop_objection(self)


uvm_component_utils(cmdline_test)