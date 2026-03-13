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


import glob
import os
import sysconfig

from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_dynamic_libs

datas = collect_data_files("ansys.aedt.core")
binaries = collect_dynamic_libs("ansys.aedt.core")

# collect_dynamic_libs misses .pyd files nested inside syslib — add them explicitly
_site_packages = sysconfig.get_path("purelib")
_nastran_src = os.path.join(_site_packages, "ansys", "aedt", "core", "syslib", "nastran_import")
_dest = os.path.join("ansys", "aedt", "core", "syslib", "nastran_import")

for _pyd in glob.glob(os.path.join(_nastran_src, "*.pyd")):
    binaries.append((_pyd, _dest))
