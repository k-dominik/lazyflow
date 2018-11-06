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
from lazyflow.graph import Graph
from lazyflow.operators.opValuePiper import OpValuePiper


class TestOpValuePiper(object):
    def setUp(self):
        self.graph = Graph()
        self.op_pipe = OpValuePiper(graph=self.graph)

    def test1(self):
        # Generate a random dataset and see if it we get the right masking from the operator.
        data = [
            'Somestring',
            1,
            "Different string",
            object(),
        ]

        for dat in data:
            # Provide input read all output.
            self.op_pipe.Input.setValue(dat)
            output = self.op_pipe.Output.value
            assert output == dat, f"{output} != {dat}"

