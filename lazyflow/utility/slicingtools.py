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

"""Utilities for numpy-like indices and shapes.

Partial copy of slicingtools.py from volumina.
"""

from typing import Sequence, Tuple, Union


def is_bounded(slicing: Union[slice, Sequence[slice]]) -> bool:
    """Do all slices have upper bounds?

    Examples:
        >>> is_bounded((slice(0, 1), slice(2, 3)))
        True
        >>> is_bounded((slice(0, 1), slice(2, None)))
        False
    """
    if isinstance(slicing, slice):
        slicing = (slicing,)
    return all(sl.stop is not None for sl in slicing)


def slicing2shape(slicing: Union[slice, Sequence[slice]]) -> Tuple[int, ...]:
    """``X[slicing].shape``, where ``X`` is a sufficiently large array with the same number of dimensions.

    Raises:
        ValueError: slice is not bounded

    Examples:
        >>> slicing2shape((slice(0, 5), slice(10, 42)))
        (5, 32)
    """
    if isinstance(slicing, slice):
        slicing = (slicing,)
    try:
        return tuple(sl.stop - (sl.start or 0) for sl in slicing)
    except TypeError:
        raise ValueError(f"slicing {slicing} is not bounded")
