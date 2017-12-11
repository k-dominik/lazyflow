###############################################################################
#   lazyflow: data flow based lazy parallel computation framework
#
#       Copyright (C) 2011-2017, the ilastik developers
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
from lazyflow.operator import Operator, InputSlot, OutputSlot


class OpTrackSlotVersion(Operator):
    """Operator that listens to `propagateDirty` and increments `version`

    The count begins with every reconfiguration of slots at 0 (`setupOuputs` is
    called).
    """
    Input = InputSlot()
    Output = OutputSlot()
    Version = OutputSlot(stype='int')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def execute(self, slot, subindex, roi, result):
        req = self.Input.get(roi)
        req.writeInto(result)
        req.block()

    def setupOutputs(self):
        # reset the slot version
        self.Version.setValue(0)
        # pipe through the input to the output
        self.Output.meta.assignFrom(self.Input.meta)

    def propagateDirty(self, slot, subindex, roi):
        assert slot == self.Input, "Only listening to self.Input"
        # increment the slot version
        self.Version.setValue(self.Version.value + 1)
