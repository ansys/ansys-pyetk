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

from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

try:
    THIS_PATH = Path(__file__).parent
except NameError:
    THIS_PATH = Path.cwd()

toml_path = (
    THIS_PATH.parent
    / "src"
    / "ansys"
    / "aedt"
    / "toolkits"
    / "electronic_transformer"
    / "ui"
    / "frontend_properties.toml"
)
with toml_path.open("rb") as f:
    config = tomllib.load(f)

version = config["defaults"]["version"]
with (Path(THIS_PATH) / "VERSION").open(mode="w") as v:
    v.write(version)
