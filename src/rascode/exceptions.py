class ServerError(Exception):
    """Exception raised for errors in the interaction with the WCPS server."""
    pass

class QueryError(Exception):
    """Exception raised for errors in the WCPS query formation."""
    pass