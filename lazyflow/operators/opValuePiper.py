###############################################################################
#   lazyflow: data flow based lazy parallel computation framework
#
#       Copyright (C) 2011-2018, the ilastik developers
#                                <team@ilastik.org>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the Lesser GNU General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# See the files LICENSE.lgpl2 and LICENSE.lgpl3 for full text of the
# GNU Lesser General Public License version 2.1 and 3 respectively.
# This information is also available on the ilastik web site at:
#          http://ilastik.org/license/
###############################################################################
from lazyflow.graph import Operator, InputSlot, OutputSlot
from lazyflow import stype


class OpValuePiper(Operator):
    name = "OpValuePiper"
    description = "simple piping operator for ValueType Slots"

    # Inputs
    Input = InputSlot(stype=stype.ValueSlotType)
    # Outputs
    Output = OutputSlot(stype=stype.ValueSlotType)

    def setupOutputs(self):
        inputSlot = self.inputs["Input"]
        self.outputs["Output"].meta.assignFrom(inputSlot.meta)
        self.outputs["Output"].setValue(inputSlot.value)

    def execute(self, slot, subindex, roi, result):
        assert False, "Should not go here!"

    def propagateDirty(self, slot, subindex, roi):
        # Check for proper name because subclasses may define extra inputs.
        # (but decline to override notifyDirty)
        if slot.name == 'Input':
            # Dirtyness does not have to be forwarded in this case:
            # this is handled by setupOutputs
            pass
        else:
            # If some input we don't know about is dirty (i.e. we are subclassed by an operator with extra inputs),
            # then mark the entire output dirty.  This is the correct behavior for e.g. 'sigma' inputs.
            self.outputs["Output"].setDirty(())

    def setInSlot(self, slot, subindex, roi, value):
        # Implementations of this method is only needed to satisfy the flow of
        # the __setitem__ method for input slots. Nothing needs to be done here
        # as the input of the value slot is manipulated directly. When the
        # output is requested, execute is called.
        assert subindex == ()
        assert slot == self.Input
