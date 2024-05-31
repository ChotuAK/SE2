import requests
from requests.exceptions import HTTPError

# Example Coverages list (some Coverages that a user could implement in their program)
# 1) RadianceColorScaled
# 2) AvgLandTemp
# 3) AvgTemperatureColor
# 4) AverageChloroColor
# 5) AverageChloroColorScaled
# 6) C3S_satellite_soil_moisture_active_daily_t0
# 7) C3S_satellite_soil_moisture_combined_daily_flag
# 8) C3S_satellite_soil_moisture_combined_daily_mode
# 9) C3S_satellite_soil_moisture_passive_daily_dnflag
# 10) C3S_satellite_soil_moisture_combined_daily_sm_uncertainty

class dbc:
    # inside of __init__ we initialize the connection to the WCPS server
    def __init__(self):
        self.server_url = 'https://ows.rasdaman.org/rasdaman/ows?REQUEST=GetCoverage' # Link used for connection to WCPS server - Gets Coverages for the user
    
    # Send the query to WCPS server - result is either the response or just an error
    def query_run(self, query):
        try:
            response = requests.post(self.server_url, {'query':query})
            response.raise_for_status()
        except HTTPError as e:
            # Checks for server side errors
            if response.status_code == 500:
                return f"An Error occured on the Server's side - {e}. Try your query again."
            # Checks for general, HTTP related errors
            else:
                return f"An HTTP related error took place - {e}"
        # Checks for general errors
        except Exception as e:
            return f"Unexpected error - {e}"
        else:
            return response.content

# Queries sourced from https://standards.rasdaman.com/demo_wcps.html
# Most methods for updating the query include the 3 same parameters - latitude, longitude & time period / ansi
# ansi[:7] represents a singular date instead of a date range, as "self.ansi" would
class dbo:
    # Inside of __init__ we initialize the DataCube Object by establishing a connection and choosing a coverage
    def __init__(self, conn: dbc, coverage):
        self.conn = conn
        self.coverage = coverage

    # The most basic query - simply returns 1 for each pixel in coverage
    def most_basic_query(self):
        return f"""
        for $c in ({self.coverage}) return 1
        """
    
    # Returns a single value at specific point
    def get_single_value(self, lat, long, ansi):
        return f"""
        for $c in ({self.coverage}) 
        return $c[Lat({lat}), Long({long}), ansi({ansi[:7]})]
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
                    $c[ansi({ansi[:7]})]
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
                    case $c[ansi({ansi[:7]}), Lat({lat}), Long({long})] = 99999 
                        return {{red: 255; green: 255; blue: 255}} 
                    case 18 > $c[ansi("2014-07"), Lat(35:75), Long(-20:40)] 
                        return {{red: 0; green: 0; blue: 255}} 
                    case 23 > $c[ansi("2014-07"), Lat(35:75), Long(-20:40)] 
                        return {{red: 255; green: 255; blue: 0}} 
                    case 30 > $c[ansi("2014-07"), Lat(35:75), Long(-20:40)]  
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