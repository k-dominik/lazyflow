###############################################################################
#   lazyflow: data flow based lazy parallel computation framework
#
#       Copyright (C) 2011-2014, the ilastik developers
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
# 		   http://ilastik.org/license/
###############################################################################

import logging

logger = logging.getLogger(__name__)

from lazyflow.graph import Operator

from . import generic
from . import filterOperators
from . import classifierOperators
from . import valueProviders
from . import operators


def _unique_subclasses_of(cls):
    """Get unique sublcasses of a class.

    Args:
        cls: class with the `subclasses` attribute containing all it's subclasses

    Returns:
        {subclass_name: subclass} dict

    Raises:
        ImportError: duplicate subclass names
    """
    subs = {}
    dupes = set()

    for sub in cls.subclasses:
        name = sub.__name__
        if name in subs:
            dupes.add(name)
        subs[name] = sub

    if dupes:
        raise ImportError(f"some {cls.__name__} subclasses have identical names: {dupes}")

    return subs


logger.debug("Loading default Operators...")
subops = _unique_subclasses_of(Operator)
globals().update(subops)
logger.debug(" ".join(subops))
del subops


from .opSimpleStacker import OpSimpleStacker
from .opBlockedArrayCache import OpBlockedArrayCache
from .opVigraWatershed import OpVigraWatershed
from .opVigraLabelVolume import OpVigraLabelVolume
from .opFilterLabels import OpFilterLabels
from .opObjectFeatures import OpObjectFeatures
from .opCompressedCache import OpCompressedCache
from .opCompressedUserLabelArray import OpCompressedUserLabelArray
from .opLabelImage import OpLabelImage
from .opCachedLabelImage import OpCachedLabelImage
from .opInterpMissingData import OpInterpMissingData
from .opReorderAxes import OpReorderAxes
from .opLabelVolume import OpLabelVolume
from .opRelabelConsecutive import OpRelabelConsecutive
from .opPixelFeaturesPresmoothed import OpPixelFeaturesPresmoothed
