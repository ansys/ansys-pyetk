# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Region:
    """Manages the air region."""

    def __init__(self, aedtapp, setup_def):
        """Initialize and launch the region component.

        Parameters
        ----------
        aedtapp : :class:`pyaedt.Maxwell3d`
            AEDT application instance.
        setup_def : :class:`ansys.aedt.toolkits.common.properties.SetupProperties`
            Setup properties.
        """
        self.__setup_definitions = setup_def
        self.__aedt = aedtapp
        self.__offset = int(float(self.__setup_definitions.region_offset))

    def crete_geometry(self):
        """Create the region geometry."""
        self.__aedt.modeler.create_region(
            [self.__offset, self.__offset, self.__offset, self.__offset, self.__offset, self.__offset]
        )
        self.__aedt.modeler.fit_all()
