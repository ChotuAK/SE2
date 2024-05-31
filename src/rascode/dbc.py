# DataBase Connection object
# Several datacubes can use a single DBC object
# One DBC instance is created when a WDC is created

import requests

class DataBlockConnector:
    # Set URL to that specified by user
    def __init__(self, url):
        self.url = url
    
    def query(self, query):
        # Send query to the server
        response = requests.post(self.url, params={'query': query})
        
        # Print HTTP request for debugging purposes
        print("HTTP Request:", response.request.url)
        
        # If  successful, return response; if unsuccessful, display error message
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error: {response.status_code}, {response.text}")