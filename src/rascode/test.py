import unittest
from wdc import WebDataConnector
from main import DataCube

serverUrl = "https://ows.rasdaman.org/rasdaman/ows"
    
# Initialize library object and one DataCube
wdc_instance = WebDataConnector(serverUrl)
dbo = wdc_instance.createDBO()
cube = DataCube("AvgLandTemp")

class TestDataCube(unittest.TestCase):

    # Return a single value to the user
    def test_single_value1(self):
        lat = 53.08
        long = 8.80
        ansi = "2014-07"
        dbo.add_operation(cube.get_single_value(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, 'Result: 25.984251', "Error")

    def test_single_value2(self):
        lat = 42.13
        long = 3
        ansi = "2014-09"
        dbo.add_operation(cube.get_single_value(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, 'Result: 28.740158', "Error")

    # From a 3d set a 1 dimensional subset is returned
    def test_3d_to_1d_subset1(self):
        lat = 53.08
        long = 8.80
        ansi = '"2014-01":"2014-12"'
        expected_result = "2.834646,4.488189,11.10236,20.19685,21.02362,21.29921,25.98425,24.33071,22.12598,16.06299,8.897637,2.283465"
        dbo.add_operation(cube.get_3d_to_1d_subset(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, expected_result, "Error")

    def test_3d_to_1d_subset2(self):
        lat = 42.13
        long = 3
        ansi = '"2014-01":"2014-12"'
        expected_result = "10.82677,12.48032,19.92126,21.85039,25.15748,30.3937,29.01575,29.01575,28.74016,23.50394,15.7874,11.65354"
        dbo.add_operation(cube.get_3d_to_1d_subset(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, expected_result, "Error")

    # Out of degrees Celsius the Kelvin temperature is returned
    def test_celsius_to_kelvin1(self):
        lat = 53.08
        long = 8.80
        ansi = '"2014-01":"2014-12"'
        expected_result = "275.9846457481384,277.6381887435913,284.2523626327514,293.346849822998,294.1736225128174,294.4492134094238,299.1342510223388,297.4807094573974,295.2759841918945,289.2129920959472,282.0476373672485,275.4334646701813"
        dbo.add_operation(cube.get_celsius_to_kelvin(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, expected_result, "Error")

    def test_celsius_to_kelvin2(self):
        lat = 42.13
        long = 3
        ansi = '"2014-01":"2014-12"'
        expected_result = "283.976771736145,285.630315208435,293.0712589263916,295.0003932952881,298.3074802398681,303.5437015533447,302.1657489776611,302.1657489776611,301.8901580810547,296.6539367675781,288.9374011993408,284.80354347229"
        dbo.add_operation(cube.get_celsius_to_kelvin(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, expected_result, "Error")

    # The minimum value is returned
    def test_min1(self):
        lat = 53.08
        long = 8.80
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_min(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 2.2834647", "Error")

    def test_min2(self):
        lat = 42.13
        long = 3
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_min(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 10.826772'", "Error")

    # The maximum value is returned
    def test_max1(self):
        lat = 53.08
        long = 8.80
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_max(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 25.984251'", "Error")

    def test_max2(self):
        lat = 42.13
        long = 3
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_max(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 30.393702'", "Error")

    # The average value is returned
    def test_avg1(self):
        lat = 53.08
        long = 8.80
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_avg(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 15.052493472894033'", "Error")

    def test_avg2(self):
        lat = 42.13
        long = 3
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_avg(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 21.528871536254883'", "Error")

    # When the temperature is more than 15, it is returned to the user
    def test_temp_more_than_15_1(self):
        lat = 53.08
        long = 8.80
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_when_temp_more_than_15(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 7'", "Error")

    def test_temp_more_than_15_2(self):
        lat = 42.13
        long = 3
        ansi = '"2014-01":"2014-12"'
        dbo.add_operation(cube.get_when_temp_more_than_15(lat, long, ansi))
        result = dbo.execute_operation(1)
        dbo.pop_operation()
        self.assertIn(result, "Result: 9'", "Error")

if __name__ == "__main__": 
    unittest.main()