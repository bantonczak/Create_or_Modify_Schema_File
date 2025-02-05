import os
import pandas as pd

def create_or_modify_schema_ini(csv_file, col_classes=None):
    """
    Function to create or modify a schema.ini file for a given CSV file.
    
    This function checks if a schema.ini file exists in the directory of the specified CSV file.
    If it exists, it updates the schema.ini file with the column definitions of the CSV file.
    If it does not exist, it creates a new schema.ini file with the column definitions.
    
    Parameters:
    csv_file (str): The path to the CSV file.
    col_classes (dict, optional): A dictionary specifying the data types of the columns. 
                                  The keys are column names and the values are data types.
    
    Raises:
    FileNotFoundError: If the specified CSV file does not exist.
    
    Example usage:
    create_or_modify_schema_ini("path/to/your_file.csv")

    Author:
    Brittany Antonczak
    britantonczak@gmail.com
    """
    
    # Check if the CSV file exists
    if not os.path.exists(csv_file):
        raise FileNotFoundError("The specified CSV file does not exist.")
    
    # Extract file directory and file name with extension
    csv_dir = os.path.dirname(csv_file)
    file_name = os.path.basename(csv_file)
    
    # Define the path to the schema.ini file
    schema_file = os.path.join(csv_dir, "schema.ini")
    
    # Check if schema.ini already exists
    if os.path.exists(schema_file):
        # Read existing schema.ini
        with open(schema_file, 'r') as f:
            schema_content = f.read()
        
        # Check if current CSV file is already detailed in schema.ini
        file_detailed = f"[{file_name}]" in schema_content
        
        # Update column definitions if CSV file is already detailed in schema.ini
        if file_detailed:
            # Find start index of current CSV file details in schema.ini
            file_index_start = schema_content.find(f"[{file_name}]")
            
            # Find end index of current CSV file details in schema.ini
            file_index_end = schema_content.find("[", file_index_start + 1)
            if file_index_end == -1:
                file_index_end = len(schema_content)
            
            # Remove existing details for the current CSV file
            schema_content = schema_content[:file_index_start] + schema_content[file_index_end:]
    else:
        schema_content = ""
    
    # Load the CSV file using pandas to get column names and data types
    data = pd.read_csv(csv_file, nrows=5)
    col_names = data.columns

    # Map pandas dtypes to ArcGIS field types
    def map_dtype(dtype):
        if pd.api.types.is_string_dtype(dtype):
            return "Text"
        elif pd.api.types.is_integer_dtype(dtype):
            return "Long"
        elif pd.api.types.is_float_dtype(dtype):
            return "Double"
        elif pd.api.types.is_bool_dtype(dtype):
            return "Short"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            return "Date"
        elif pd.api.types.is_categorical_dtype(dtype):
            return "Text"
        else:
            return "Unknown"

    # Create a dictionary to hold the final column types
    final_col_types = {}

    # Check provided col_classes against actual field types
    if col_classes is not None:
        for col in col_names:
            if col in col_classes:
                final_col_types[col] = map_dtype(col_classes[col])
            else:
                final_col_types[col] = map_dtype(data[col].dtype)
    else:
        final_col_types = {col: map_dtype(data[col].dtype) for col in col_names}

    # Create column definitions for the current CSV file
    file_definition = [
        f"[{file_name}]",
        "ColNameHeader=True",
        "Format=CSVDelimited"
    ]
    file_definition += [f"Col{i+1}={col} {final_col_types[col]}" for i, col in enumerate(col_names)]
    
    # Append column definitions for the current CSV file in schema_content
    schema_content = "\n".join(file_definition) + "\n" + schema_content
    
    # Write updated schema.ini file
    with open(schema_file, 'w') as f:
        f.write(schema_content)

# Example usage:
# Specify the path to the CSV file
# csv_file = "your_file.csv"

# Optionally, define column classes
# col_classes = {"column1": int, "column2": str, "column3": float}  

# Call the function to create or modify schema.ini
# create_or_modify_schema_ini(csv_file, col_classes)