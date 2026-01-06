import pytest
from pathlib import Path

json_files_path = Path(__file__).parents[1] / "json_files"
vol_limit = 1e-5

pytestmark = [pytest.mark.backend_API]

class TestBackendAPI:

    def test_create_core_geometry_E(self, aedt_common_fixture_function):
        json_file_name = "E_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        core = aedt_common_fixture_function.create_core_geometry()

        assert (core.volume > 0 and
                round(abs(core.volume - 39185.968), 4) < vol_limit)


    def test_create_core_geometry_EC(self, aedt_common_fixture_function):
        json_file_name = "EC_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        core = aedt_common_fixture_function.create_core_geometry()

        assert (core.volume > 0 and
                round(abs(core.volume - 7604.5672486990425), 4) < vol_limit)

    def test_create_core_geometry_EI(self, aedt_common_fixture_function):
        json_file_name = "EI_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        core = aedt_common_fixture_function.create_core_geometry()

        assert (core.volume > 0 and
                round(abs(core.volume - (62.50555737 + 83.89463332) * 2), 4) < vol_limit)

    def test_create_core_geometry_EQ(self, aedt_common_fixture_function):
        json_file_name = "EQ_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        core = aedt_common_fixture_function.create_core_geometry()

        assert (core.volume > 0 and
                round(abs(core.volume - 12998.21599628344), 4) < vol_limit)

    def test_create_core_geometry_RM(self, aedt_common_fixture_function):
        json_file_name = "RM_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        core = aedt_common_fixture_function.create_core_geometry()

        assert (core.volume > 0 and
                round(abs(core.volume -9649.227258880906), 4) < vol_limit)

    def test_create_core_geometry_U(self, aedt_common_fixture_function):
        json_file_name = "U_wound_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        core = aedt_common_fixture_function.create_core_geometry()

        assert (core.volume > 0 and
                round(abs(core.volume -20334.080000000005), 4) < vol_limit)