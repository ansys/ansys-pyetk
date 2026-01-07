import pytest
from pathlib import Path

json_files_path = Path(__file__).parents[1] / "json_files"
vol_limit = 1e-5

pytestmark = [pytest.mark.backend_API]


class TestBackendAPI:

    def test_create_bobbin_geometry_planar_rectangular(self, aedt_common_fixture_function):
        json_file_name = "EI_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        bobbin = aedt_common_fixture_function.create_bobbin_geometry()

        assert (bobbin.volume > 0 and
                round(abs(bobbin.volume - 204.8), 4) < vol_limit)

    def test_create_bobbin_geometry_planar_circular(self, aedt_common_fixture_function):
        json_file_name = "RM_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        bobbin = aedt_common_fixture_function.create_bobbin_geometry()

        assert (bobbin.volume > 0 and
                round(abs(bobbin.volume -1086.5826510971026), 4) < vol_limit)

    def test_create_bobbin_geometry_wound_circular(self, aedt_common_fixture_function):
        json_file_name = "EC_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        bobbin = aedt_common_fixture_function.create_bobbin_geometry()

        assert (bobbin.volume > 0 and
                round(abs(bobbin.volume - 110.30603045651762), 4) < vol_limit)

    def test_create_bobbin_geometry_wound_rectangular(self, aedt_common_fixture_function):
        json_file_name = "U_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)
        aedt_common_fixture_function.properties.bobbin.draw_bobbin = True

        bobbin = aedt_common_fixture_function.create_bobbin_geometry()

        assert (bobbin.volume > 0 and
                round(abs(bobbin.volume - 337.62411801165206), 4) < vol_limit)

    def test_create_bobbin_geometry_wound_rectangular_ecore(self, aedt_common_fixture_function):
        json_file_name = "E_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)
        aedt_common_fixture_function.properties.bobbin.draw_bobbin = True

        bobbin = aedt_common_fixture_function.create_bobbin_geometry()

        assert (bobbin.volume > 0 and
                round(abs(bobbin.volume - 422.8865923767842), 4) < vol_limit)