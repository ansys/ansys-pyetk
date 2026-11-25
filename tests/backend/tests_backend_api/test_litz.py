# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 - 2026 Synopsys, Inc. and ANSYS, Inc. All rights reserved.
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

"""Integration coverage for Litz wire."""

import copy
import json
from pathlib import Path

import pytest

from ansys.aedt.toolkits.electronic_transformer.backend.workflows.winding import Winding

pytestmark = [pytest.mark.backend]


@pytest.mark.parametrize(
    ("conductor_type", "dimensions"),
    [
        ("Litz", {"diameter": 2.05}),
        ("Litz Rectangular", {"width": 2.05, "height": 2.05}),
    ],
)
def test_create_litz_model(aedt_common_fixture_function, tmp_path, monkeypatch, conductor_type, dimensions):
    source = Path(__file__).parents[1] / "json_files" / "RM_wound_circular.json"
    data = json.loads(source.read_text())
    conductor = data["winding"]["layers"]["layer_1"]["conductor"]
    conductor.pop("diameter")
    conductor.update(type=conductor_type, strand_diameter=0.1, strand_number=100, **dimensions)
    path = tmp_path / "litz.json"
    path.write_text(json.dumps(data))
    backend = aedt_common_fixture_function
    backend.load_properties_from_json(path)
    monkeypatch.setattr(
        "ansys.aedt.toolkits.electronic_transformer.backend.workflows.etk.Circuit.create_circuit",
        lambda self: None,
    )
    assert backend.create_model()
    backend.connect_design("Maxwell3D")
    app = backend.aedtapp
    plot = next(plot for plot in app.post.plots if str(plot) == "Stranded Loss")
    assert set(plot.expressions) == {"StrandedLoss", "StrandedLossAC"}
    objects = [obj for obj in app.modeler.object_list if obj.name.startswith("Layer1") and "_Section" not in obj.name]
    assert objects
    material = app.materials[objects[0].material_name]
    assert material.stacking_type == "Litz Wire"
    assert material.wire_type == "Round"
    assert str(material.strand_number) == "100"
    assert str(material.wire_diameter) == "0.1mm"
    for obj in objects:
        assert not app.oboundary.GetEddyEffect(obj.name)


def test_create_planar_rectangular_litz_geometry(aedt_common_fixture_function, tmp_path):
    source = Path(__file__).parents[1] / "json_files" / "EI_planar_rectangular.json"
    data = json.loads(source.read_text())
    for layer in data["winding"]["layers"].values():
        layer["conductor"].update(type="Litz Rectangular", strand_diameter=0.02, strand_number=10)
    path = tmp_path / "planar_litz.json"
    path.write_text(json.dumps(data))
    backend = aedt_common_fixture_function
    backend.load_properties_from_json(path)
    backend.connect_design("Maxwell3D")
    app = backend.aedtapp
    app.solution_type = "EddyCurrent"
    props = backend.properties
    winding = Winding("Windings", app, props.winding, props.core, props.settings, props.bobbin)
    winding.set_class_obj_material(props.materials["Copper"])
    assert winding.create_geometry()
    winding.set_material(props.materials["Copper"], props.circuit.connections)
    assert winding.objects_list
    for obj in winding.objects_list:
        assert app.materials[obj.material_name].stacking_type == "Litz Wire"
        assert not app.oboundary.GetEddyEffect(obj.name)


def test_assign_distinct_litz_materials(aedt_common_fixture_function, tmp_path):
    source = Path(__file__).parents[1] / "json_files" / "RM_wound_circular.json"
    data = json.loads(source.read_text())
    data["winding"]["layers"]["layer_1"]["conductor"].update(type="Litz", strand_diameter=0.1, strand_number=100)
    second_layer = copy.deepcopy(data["winding"]["layers"]["layer_1"])
    second_layer["conductor"].update(strand_diameter=0.2, strand_number=20)
    data["winding"]["layers"]["layer_2"] = second_layer
    data["circuit"]["connections"]["2"] = {"2": "Layer"}
    data["circuit"]["side_loads"].append(1e-6)
    path = tmp_path / "litz.json"
    path.write_text(json.dumps(data))
    backend = aedt_common_fixture_function
    backend.load_properties_from_json(path)
    backend.connect_design("Maxwell3D")
    app = backend.aedtapp
    app.solution_type = "EddyCurrent"
    props = backend.properties
    winding = Winding("Windings", app, props.winding, props.core, props.settings, props.bobbin)
    winding.set_class_obj_material(props.materials["Copper"])
    assert winding.create_geometry()
    winding.set_material(props.materials["Copper"], props.circuit.connections)
    layer2_objects = [obj for obj in winding.objects_list if obj.name.startswith("Layer2")]
    assert layer2_objects
    second_material = app.materials[layer2_objects[0].material_name]
    assert str(second_material.strand_number) == "20"
    assert str(second_material.wire_diameter) == "0.2mm"
    for obj in winding.objects_list:
        assert not app.oboundary.GetEddyEffect(obj.name)
        expected = "copper_pyetk_litz_side_1" if obj.name.startswith("Layer1") else "copper_pyetk_litz_side_2"
        assert obj.material_name.lower().startswith(expected)
