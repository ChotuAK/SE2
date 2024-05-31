# Main method file to test library

from wdc import WebDataConnector

class DataCube:
    """
    Provides an interface for constructing and executing dynamic WCPS queries tailored to specific data coverage.
    """
    def __init__(self, coverage):
        self.coverage = coverage

    def most_basic_query(self):
        return f"""
        for $c in ({self.coverage}) return 1
        """
    
    # Returns a single value at specific point
    def get_single_value(self, lat, long, ansi):
        return f"""
        for $c in ({self.coverage}) 
        return $c[Lat({lat}), Long({long}), ansi({ansi})]
        """

    # Transforms the 3d data into 1 dimensional data
    def get_3d_to_1d_subset(self, lat, long, ansi):
        return f"""
        diagram>>for $c in ({self.coverage})
        return encode(
                    $c[Lat({lat}), Long({long}), ansi({ansi})]
                , "text/csv")
        """

    # Transforms the 3d data into 2 dimensional data
    def get_3d_to_2d_subset(self, ansi):
        return f"""
        image>>for $c in ({self.coverage})
        return encode(
                    $c[ansi({ansi})]
                , "image/png")
        """

    # Converts celsius data to kelvin
    def get_celsius_to_kelvin(self, lat, long, ansi):
        return f"""
        diagram>>for $c in ({self.coverage}) 
        return encode(
                        $c[Lat({lat}), Long({long}), ansi({ansi})] 
                        + 273.15
                , "text/csv")
        """

    # Gets the minimum out of the data
    def get_min(self, lat, long, ansi):
        return f"""
        for $c in ({self.coverage}) 
        return 
            min($c[Lat({lat}), Long({long}), ansi({ansi})])
        """

    # Gets the maximum out of the data
    def get_max(self, lat, long, ansi):
        return f"""
        for $c in ({self.coverage}) 
        return 
            max($c[Lat({lat}), Long({long}), ansi({ansi})])
        """

    # Gets the average of the data
    def get_avg(self, lat, long, ansi):
        return f"""
        for $c in ({self.coverage}) 
        return 
            avg($c[Lat({lat}), Long({long}), ansi({ansi})])
        """

    # Finds out when the temperature is more than 15 
    def get_when_temp_more_than_15(self, lat, long, ansi):
        return f"""
        for $c in ({self.coverage})
        return count(
                $c[Lat({lat}), Long({long}), ansi({ansi})]
            > 15)
        """

    # Change the colors of an image, essentially creating a heat map out of an image
    def get_on_the_fly_coloring(self, lat, long, ansi):
        return f"""
        image>>for $c in ({self.coverage}) 
        return encode(
            switch 
                    case $c[ansi("{ansi}"), Lat({lat}), Long({long})] = 99999 
                        return {{red: 255; green: 255; blue: 255}} 
                    case 18 > $c[ansi("{ansi}"), Lat({lat}), Long({long})] 
                        return {{red: 0; green: 0; blue: 255}} 
                    case 23 > $c[ansi("{ansi}"), Lat({lat}), Long({long})] 
                        return {{red: 255; green: 255; blue: 0}} 
                    case 30 > $c[ansi("{ansi}"), Lat({lat}), Long({long})]  
                        return {{red: 255; green: 140; blue: 0}} 
                    default return {{red: 255; green: 0; blue: 0}}
                , "image/png")
        """

    # Constructs a gradient-looking image, to represent the coverage
    def get_coverage_consturctor(self):
        return f"""
        image>>for $c in ({self.coverage}) 
        return encode(
                        coverage myCoverage
                        over $p x(0:200),
                            $q y(0:200)
                        values $p + $q
            , "image/png")
        """
    

    def generate_query(self, select, conditions=None, return_format=None):
        """
        Dynamically constructs a WCPS query from specified parameters.
        - 'select' defines what to select in the query.
        - 'conditions' adds conditions to the query.
        - 'return_format' specifies the output format of the result.
        """
        query = f"for $c in ({self.coverage})"
        if conditions:
            query += f" where {conditions}"
        if return_format:
            select = f"encode({select}, '{return_format}')"
        query += f" return {select}"

        match return_format:
            case "image/png":
                query = f"image>>" + query
            case "text/csv":
                query =f"diagram>>" + query
        return query

    def retrieve_temperature_data(self, lat, long, date_range, output_format="text/csv"):
        """
        Retrieves temperature data over a specified date range at given coordinates.
        """
        select = f"$c[Lat({lat}), Long({long}), ansi('{date_range}')]"
        return self.generate_query(select, return_format=output_format)

    def calculate_aggregate_temperature(self, lat, long, date_range ):
        """
        Calculates aggregate values such as min, max, or avg temperature over a specified date range at given coordinates.
        """
        select = f"avg($c[Lat({lat}), Long({long}), ansi('{date_range}')])"
        return self.generate_query(select, return_format=None)

    def visualize_temperature(self, lat_range, long_range, date, color_scale):
        """
        Visualizes temperature data across a latitude and longitude range using a color scale.
        """
        conditions = f"Lat({lat_range}), Long({long_range}), ansi('{date}')"
        select = f"switch case $c > {color_scale['high']} then {{red: 255; green: 0; blue: 0}} case $c < {color_scale['low']} then {{red: 0; green: 0; blue: 255}} default {{red: 255; green: 255; blue: 0}}"
        return self.generate_query(select, conditions = date , return_format="image/png")

    def advanced_query_capabilities(self, lat, long, criteria, processing_steps):
        """
        Performs complex queries with multiple processing steps such as filtering, aggregation, and transformation.
        """
        query_parts = [f"$c[Lat({lat}), Long({long})]" + step for step in processing_steps]
        full_query = " and ".join(query_parts)
        return self.generate_query(full_query, conditions=criteria)
    
    def get_data_series(self, lat, long, start_date, end_date, freq):
        """
        Retrieves a series of data based on frequency over a given date range at specific coordinates.
        """
        select = f"$c[Lat({lat}), Long({long}), ansi('{start_date}:{end_date}:{freq}')]"
        return self.generate_query(select, return_format="text/csv")

    def apply_threshold_filter(self, threshold, above=True):
        """
        Filters data based on a temperature threshold, optionally specifying whether to filter above or below the threshold.
        """
        condition = f"$c > {threshold}" if above else f"$c < {threshold}"
        select = "$c"
        return self.generate_query(select, conditions=condition, return_format="text/csv")

    def extract_seasonal_data(self, lat, long, season, year, output_format="text/csv"):
        """
        Extracts data for a specific season and year at given coordinates.
        Seasons are defined as 'spring', 'summer', 'autumn', 'winter'.
        """
        season_months = {
            'spring': '03:05',
            'summer': '06:08',
            'autumn': '09:11',
            'winter': f'12:{year}-02:{int(year)+1}'
        }
        date_range = season_months.get(season, '01:12')
        select = f"$c[Lat({lat}), Long({long}), ansi('{year}-{date_range}')]"
        return self.generate_query(select, return_format=output_format)

    def spatial_aggregation(self, lat_range, long_range, date, aggregate_func="avg"):
        """
        Performs spatial aggregation over a specified area and date.
        """
        select = f"{aggregate_func}($c[Lat({lat_range}), Long({long_range}), ansi('{date}')])"
        return self.generate_query(select, return_format="text/plain")

    def difference_between_dates(self, lat, long, date1, date2):
        """
        Calculates the difference in data values between two dates at a specific location.
        """
        select = f"$c[Lat({lat}), Long({long}), ansi('{date1}')]" + " - " + f"$c[Lat({lat}), Long({long}), ansi('{date2}')]"
        return self.generate_query(select, return_format="text/plain")

    def classify_data(self, thresholds):
        """
        Classifies data into categories based on provided thresholds and returns the class labels.
        """
        cases = " ".join([f"case $c < {th} then '{idx+1}'" for idx, th in enumerate(thresholds)])
        select = f"switch {cases} default '0'"
        return self.generate_query(select, return_format="text/plain")

    def correlation_between_variables(self, variable1, variable2, lat_range, long_range, date_range):
        """
        Computes correlation between two variables over a specified range and time.
        """
        select = f"corr($c1[Lat({lat_range}), Long({long_range}), ansi('{date_range}')], $c2[Lat({lat_range}), Long({long_range}), ansi('{date_range}')])"
        conditions = f"$c1 in ({variable1}), $c2 in ({variable2})"
        return self.generate_query(select, conditions, "text/plain")

serverUrl = "https://ows.rasdaman.org/rasdaman/ows"
    
# Initialize library object and one DataCube
wdc_instance = WebDataConnector(serverUrl)
dbo = wdc_instance.createDBO()
cube = DataCube("AvgLandTemp")



# Example of using the DataCube class
if __name__ == "__main__":
    
    dbo.add_operation(cube.get_max(53.08, 8.80, '"2014-01":"2014-12"'))
    dbo.add_operation(cube.calculate_aggregate_temperature(53.08, 8.80, '"2014-01":"2014-12"'))
    dbo.add_operation(cube.get_when_temp_more_than_15(53.08, 8.80, '"2014-01":"2014-12"'))
    dbo.add_operation(cube.get_3d_to_1d_subset(53.08, 8.80, '"2014-01":"2014-12"'))
    dbo.add_operation(cube.get_celsius_to_kelvin(53.08, 8.80, '"2014-01":"2014-12"'))
    dbo.add_operation(cube.get_avg(53.08, 8.80, '"2014-01":"2014-12"'))
    dbo.add_operation(cube.get_single_value(53.08, 8.80, "2014-07"))
    dbo.add_operation(cube.get_3d_to_2d_subset("2014-07"))
    dbo.add_operation(cube.get_on_the_fly_coloring('35:75', '-20:40', "2014-07"))
    dbo.add_operation(cube.get_coverage_consturctor())
    dbo.execute_all_operations()

    dbo.clear_operation()

    print("Success.")

