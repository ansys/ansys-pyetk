# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: Apache-2.0
#
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from ansys.aedt.toolkits.electronic_transformer.backend.workflows.geometry_common import GeometryCreatable


class Region(GeometryCreatable):
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
        self.aedtapp = aedtapp
        self.__offset = int(float(self.__setup_definitions.region_offset))

    def create_geometry(self):
        """Create the region geometry."""
        self.aedtapp.modeler.create_region(
            [self.__offset, self.__offset, self.__offset, self.__offset, self.__offset, self.__offset]
        )
        self.aedtapp.modeler.fit_all()
