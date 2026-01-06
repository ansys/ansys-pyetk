import pytest
from pathlib import Path

json_files_path = Path(__file__).parents[1] / "json_files"
vol_limit = 1e-5

pytestmark = [pytest.mark.backend_API]


class TestBackendAPI:

    def test_create_winding_geometry_layer_type_planar_cross_section_rec(self, aedt_common_fixture_function):
        json_file_name = "EI_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        winding = aedt_common_fixture_function.create_winding_geometry()

        assert (winding.volume > 0 and
                round(abs(winding.volume - (28.413999191615822)), 4) < vol_limit)

    def test_create_winding_geometry_layer_type_wound_cross_section_rec(self, aedt_common_fixture_function):
        json_file_name = "EC_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        winding = aedt_common_fixture_function.create_winding_geometry()

        assert (winding.volume > 0 and
                round(abs(winding.volume - (945.493725024382)), 4) < vol_limit)

    def test_create_winding_geometry_layer_type_wound_cross_section_circ(self, aedt_common_fixture_function):
        json_file_name = "RM_wound_circular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        winding = aedt_common_fixture_function.create_winding_geometry()

        assert (winding.volume > 0 and
                round(abs(winding.volume - (1104.917391402094)), 4) < vol_limit)
