# Datacube Object
# Stores operations (queries) in the operations array

import logging
from PIL import Image
import io

class DatabaseOperation:
    def __init__(self, dbc):
        self.dbc = dbc
        self.operations = []
        logging.basicConfig(level=logging.DEBUG)

    def add_operation(self, operation):
        self.operations.append(operation)
        print("Operation added...")

    def pop_operation(self):
        self.operations.pop()
        print("Operation popped...")

    def clear_operation(self):
        self.operations.clear()
        print("Operations cleared...")

    def execute_operation(self, index):
        logging.debug(f"Executing query {index}")
        logging.debug(f"Query: {self.operations[index-1]}")

    # Perform the query
        result = self.dbc.query(self.operations[index-1])

    # Assuming result is a bytes object that might represent an image or text
        try:
            # Try to decode as text
            text_output = result.decode('utf-8')
            logging.debug(f"Result: {text_output}")
            print(f"Text Result: {text_output}")
            return text_output
        except UnicodeDecodeError:
            # If decode fails, assume it's an image
            try:
                # Load the image from bytes
                image = Image.open(io.BytesIO(result))
                image.show()  # This will display the image if possible (works in GUI environments)

                # Optionally, save the image to disk
                image_path = f"output_image_{index}.png"
                image.save(image_path)
                logging.debug(f"Image saved to {image_path}")
                print(f"Image Result: Saved to {image_path}")
            except IOError:
                logging.error("Failed to process image data")

    def execute_all_operations(self):
        for i in range(len(self.operations)):
            self.execute_operation(i+1)
