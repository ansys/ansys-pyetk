import pytest
from pathlib import Path

json_files_path = Path(__file__).parents[1] / "json_files"
vol_limit = 1e-5

pytestmark = [pytest.mark.backend_API]


class TestBackendAPI:

    def test_material_class(self, aedt_common_fixture_function):
        json_file_name = "EI_planar_rectangular.json"
        json_path = Path(json_files_path) / json_file_name
        aedt_common_fixture_function.read_props_from_json(json_path)

        assert(aedt_common_fixture_function.properties.materials["3F3"].conductivity==0.5)
        assert(aedt_common_fixture_function.properties.materials["3F3"].density == 4750.0)
        assert(aedt_common_fixture_function.properties.materials["3F3"].power_ferrite_loss_params.x==1.561)
        assert(aedt_common_fixture_function.properties.materials["3F3"].power_ferrite_loss_params.cm == 0.195)
        assert(aedt_common_fixture_function.properties.materials["3F3"].power_ferrite_loss_params.y == 2.15)
        assert(aedt_common_fixture_function.properties.materials["3F3"].mu_vs_freq_list == [[0.0, 2000.0], [98459.6815894695, 2027.2],
                                                                   [197983.598439825, 2051.0],
                                                                   [398107.170553497, 2100.0],
                                                                   [494745.693364606, 2124.0],
                                                                   [596047.538592714, 2174.0],
                                                                   [696140.064601457, 2251.3],
                                                                   [788186.901908786, 2304.4],
                                                                   [892404.594894609, 2386.3],
                                                                   [994839.015358011, 2500.2],
                                                                   [1126381.2001137, 2589.1],
                                                                   [1255672.56203026, 2619.4],
                                                                   [1378243.15007929, 2619.4],
                                                                   [1536444.41791644, 2559.1],
                                                                   [1712804.77556574, 2414.3],
                                                                   [1822527.78210077, 2251.3],
                                                                   [1969618.08128912, 2075.0],
                                                                   [2161879.38710699, 1846.9],
                                                                   [2372907.99104522, 1550.8],
                                                                   [2604535.83467541, 1242.9],
                                                                   [2814739.4644536, 1019.6], [3287410.45931894, 603.6],
                                                                   [3780315.8735092, 300.0], [4214238.41031241, 188.3],
                                                                   [4625604.95263426, 122.3], [4846109.89543321, 100.3],
                                                                   [5156553.7681451, 88.3], [5402369.31126385, 77.7],
                                                                   [5659903.00645773, 70.0], [6116695.39929428, 60.1],
                                                                   [6713767.41844878, 49.3], [7963859.60989012, 39.5],
                                                                   [9016877.71231702, 34.3], [10209130.7056581, 31.3],
                                                                   [11559028.8668147, 28.8]])

