### WCPS PYTHON Library
## Anshu Kushwaha, Elias Ouali, Stefan Dusnoki & Blaise Mbogho


## Description
This project showcases the functionality of interacting with a DataCube server by using the Python programming language. Some functionalities such as the ability to return the average out of a set, returning statistical data from a 3d set in thee form of a one dimensional subset.
## Example Usage
## Getting Started with DataCubeWCPS

To use the `DataCubeWCPS` library effectively, follow these steps to set up and execute WCPS queries for geospatial data analysis:


First, establish a connection to the WCPS server using the `WebDataConnector` class. After making the connection, execute the queries which are dynamically generated using the `DatabaseOperation` class.

```python

# 1.Initialize the connection
connection = WebDataConnector(url)

# 2. Initialize the DataCube with a coverage
cube = DataCube("AvgLandTemp")

# 3. Define parameters for the query
lat = 53.08
long = 8.80
ansi = '"2014-01":"2014-12"'  # Date range for the query

# 4. Construct the query
query = cube.get_single_value(lat, long, ansi)

# 5. Add the query for operation
dbo.add_operation(query)

# 6. Execute the operation on Datacube
dbo.execute_operation(index)
or
dbo.execute_all_operations()

# 7. Remove the operations after executions
dbo.pop()
or
dbo.clear()

```

## Features

- DataCube connection management: The ability to connect to the datacube server.
- Data Retrieval: Different functions that allow a user to retrieve certain values such as the minimum, maximum, average, etc. 
- Temperature Conversion: Allows a user to convert temperature from Celsius to Kelvin, the values then being returned.
- Subset Extraction: Fetching a 1 dimensional subset out of a 3d data set.
- Images: Downloads the images of different weather conditions based on the query.
- Dynamic queries generation: Queries are generated dynamically taking values for Lat, Lon, Ansi, etc for desired function.
- Advanced Statistical Analysis: Extended the library to include functions for calculating more complex statistical data directly from the DataCube server, such as variance and standard deviation.
- Improved Temperature Conversion: Enhanced the conversion functions to support more precise conversions between temperature scales, including new utility functions for real-time data transformation.

## To test all the features

All the features can be accessed and used performing this command:

```python
python  src/rascode/main.py
```

## Testing

The project includes a suite of tests under the `tests` directory to validate various functionalities:

- Single Value Retrieval Tests: Checks if the correct temperature value is returned for a given latitude, longitude, and time.
- 3D to 1D Subset Extraction Tests: Validates that a 1D temperature subset can be retrieved from a 3D dataset for a whole year.
- Temperature Scale Conversion Tests: Confirms that the conversion from Celsius to Kelvin is accurate.
- Statistical Data Retrieval Tests: Ensures that minimum, maximum, and average calculations are correct.
- Conditional Extraction Test: Tests if the system correctly counts the number of data points above 15 degrees Celsius.

To run the tests, a user simply has to be in the root directory of the package and run the following command
```python
python src/rascode/test.py
```




### New Functionalities

- **Subset Extraction**: Added functionality to extract one-dimensional subsets from three-dimensional datasets, enabling detailed analysis on specific data slices.
- **Conditional Data Retrieval**: Implemented advanced filtering capabilities to retrieve data based on custom-defined conditions, such as temperature thresholds.
- **Spatial Aggregation**: Introduced methods to perform spatial data aggregation, providing users with the tools to summarize data over specified geographic areas.
- **Correlation Analysis**: Developed features to calculate the correlation between different datasets, facilitating complex environmental and spatial analyses.
- **Threshold Filtering**: New functions to apply temperature thresholds that filter data dynamically, allowing for specialized data views based on user-defined criteria.

## UML
The design for the UML (Unified Modeling Language) diagram has been added in order for the user to better understand how the different parts of the code interact with each other. It can be found in the root directory of the package.
