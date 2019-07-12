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


def get_default_axisordering(shape):
    """Given a data shape, return the default axis ordering

    For data types that do not support axistags, we assume a default axis
    ordering, given the shape, and implicitly the number of dimensions.

    Args:
        shape (tuple): Shape of the data

    Returns:
        str: String, each position represents one axis.

    Examples:
        >>> get_default_axisordering((10, 20))
        'yx'
        >>> get_default_axisordering((10, 20, 30))
        'zyx'
        >>> get_default_axisordering((10, 20, 30, 3))
        'zyxc'
        >>> get_default_axisordering((5, 10, 20, 20, 3))
        'tzyxc'
        >>> get_default_axisordering(())  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        ValueError
        >>> get_default_axisordering((1,))  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        ValueError
        >>> get_default_axisordering((1, 2, 3, 4, 5, 6))  # doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
          ...
        ValueError
    """
    axisorders = {2: "yx", 3: "zyx", 4: "zyxc", 5: "tzyxc"}
    ndim = len(shape)

    if ndim == 3 and shape[2] <= 4:
        # Special case: If the 3rd dim is small, assume it's 'c', not 'z'
        return "yxc"

    try:
        return axisorders[ndim]
    except KeyError:
        raise ValueError(f"{ndim}-dimensional shapes are not supported")
