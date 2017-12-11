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
import numpy
from lazyflow.operators.opTrackSlotVersion import OpTrackSlotVersion
from lazyflow.operators import OpArrayPiper
from lazyflow.graph import Graph


class TestOpTrackSlotVersion(object):
    def setup(self):
        self.graph = Graph()

    def test_data_changes(self):
        op_source = OpArrayPiper(graph=self.graph)
        op_version = OpTrackSlotVersion(graph=self.graph)

        data = numpy.random.randint(0, 256, (10, 12, 13, 2), dtype=numpy.uint8)

        # Provide input, before connecting (hence, version = 0)
        op_source.Input.setValue(data)

        # Connect the ops
        op_version.Input.connect(op_source.Output)

        output = op_version.Output[None].wait()

        index = 0
        for i in range(index, index + 10):
            op_source.Input.setDirty()
            index += 1
            assert (data == output).all()
            assert op_version.Version.value == index

        new_data = numpy.random.randint(0, 256, (10, 12, 13, 2), dtype=numpy.uint8)

        # Once already connected, the version should start at 1 (connect callback is executed)
        index = 1
        op_source.Input.setValue(new_data)
        print(op_version.Version.value)
        assert op_version.Version.value == index
