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
import filecmp
import logging
import os
import shutil
import tempfile
import unittest

import numpy
import pytiff
import vigra

from lazyflow.graph import Graph
from lazyflow.operators import OpArrayPiper
from lazyflow.operators.ioOperators import OpBigTiffWriter

class TestOpBigTiffWriter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Generate some example data, write data as bigtiff using pytiff"""
        cls.tmp_data_folder = tempfile.mkdtemp()
        # Todo: python3 f"formatstring"
        cls.test_file_name = "{}/bigtiff_testfile.tif".format(cls.tmp_data_folder)

        cls.data = numpy.random.randint(0, 255, (800, 1200)).astype('uint8')
        cls.dataShape = cls.data.shape
        cls.testData = vigra.VigraArray(
            cls.dataShape,
            axistags=vigra.defaultAxistags('yx'),
            order='C',
            dtype=cls.data.dtype)
        cls.testData[...] = cls.data
        # Will do binary comparison with this file:
        try:
            t = pytiff.Tiff(cls.test_file_name, file_mode='w', bigtiff=True)
            t.write(cls.data)
        finally:
            t.close()

    @classmethod
    def teardownClass(cls):
        print(cls.tmp_data_folder)
        # shutil.rmtree(cls.tmp_data_folder)

    def test_small_file_writing(self):
        """Test if bigtiff can be written with a small dataset"""
        g = Graph()
        opWriter = OpBigTiffWriter(graph=g)

        opPiper = OpArrayPiper(graph=g)
        opPiper.Input.setValue(self.testData)

        out_file_name = '{}/bigtiff_writer_test.tif'.format(self.tmp_data_folder)
        opWriter.Filename.setValue(out_file_name)
        opWriter.Image.connect(opPiper.Output)

        # Write it...
        opWriter.WriteImage[:].wait()

        self.assertTrue(os.path.exists(out_file_name))

        self.assertTrue(filecmp.cmp(out_file_name, self.test_file_name))

    def test_big_file_writing(self):
        """Test if bigtiff can be written with out of RAM data

        WARNING: this will probably take a lot of time and use a lot of
          disk space.
        """
        pass

if __name__ == "__main__":
    import sys
    import nose
    sys.argv.append("--nocapture")    # Don't steal stdout.  Show it on the console as usual.
    sys.argv.append("--nologcapture") # Don't set the logging level to DEBUG.  Leave it alone.
    nose.run(defaultTest=__file__)
