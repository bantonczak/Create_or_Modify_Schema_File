
#----------------------------------------------------------------~    

# Function to generate a schema.ini file.

# Created by Brittany Antonczak

#----------------------------------------------------------------~ 


# Description: 

# Function to create or modify a schema.ini file for a given CSV file. 
# The schema.ini file generated will be compatible with reading data into ArcGIS.

create_or_modify_schema_ini <- function(csv_file, col_classes = NULL) {
  
  # install/load required packages 
  if(!require("data.table")) install.packages("data.table")
  
  # Check if the CSV file exists
  if (!file.exists(csv_file)) {
    stop("The specified CSV file does not exist.")
  }
  
  # extract file directory and file name with extension
  csv_dir <- dirname(csv_file)
  file_name <- basename(csv_file)
  
  # Define the path to the schema.ini file
  schema_file <- file.path(csv_dir, "schema.ini")
  
  # Check if schema.ini already exists
  if (file.exists(schema_file)) {
    
    # Read existing schema.ini
    schema_content <- readLines(schema_file)
    
    # Check if current CSV file is already detailed in schema.ini
    file_detailed <- any(grepl(paste0("^\\[", file_name, "\\]"), schema_content))
    
    # Update column definitions if CSV file is already detailed in schema.ini
    if (file_detailed) {
      
      # Find start index of current CSV file details in schema.ini
      file_index_start <- grep(paste0("^\\[", file_name, "\\]"), schema_content)
      
      # Find end index of current CSV file details in schema.ini
      if (any(grep("^\\[", schema_content[(file_index_start + 1):length(schema_content)]))) {
        file_index_end <- grep("^\\[", schema_content[(file_index_start + 1):length(schema_content)]) - 1
        file_index_end <- file_index_end[1]
      } else {
        file_index_end <- length(schema_content)
      }
      schema_content <- schema_content[-c((file_index_start):file_index_end)]
    }
  } else {
    schema_content <- character(0)
  }
  
  # Load the CSV file using data.table::fread to get column names and data types
  if (is.null(col_classes)) {
    data <- data.table::fread(csv_file, header = TRUE, nrows = 5)
  } else {
    data <- data.table::fread(csv_file, header = TRUE, nrows = 5, 
                              colClasses = col_classes)
  }
  
  # Extract column names and data types
  col_names <- names(data)
  col_types <- sapply(data, function(x) {
    if (is.character(x)) {
      "Text"
    } else if (is.integer(x)) {
      "Long"
    } else if (is.numeric(x)) {
      "Double"
    } else {
      "Unknown"  
    }
  })

  # Create column definitions for the current CSV file
  file_definition <- paste(c(
    paste("[", file_name, "]", sep = ""),
    "ColNameHeader=True",
    "Format=CSVDelimited",
    paste(paste0("Col",1:length(col_names),"=",col_names," ",col_types))
  ))
  
  # Append column definitions for the current CSV file in schema_content
  schema_content <- c(file_definition, "", schema_content)
  
  # Write updated schema.ini file
  writeLines(schema_content, schema_file)
}





# Example usage:

# Specify the path to the CSV file
csv_file = "your_file.csv"

# Optionally, define column classes:
# Create a named vector where each name corresponds to a column in your CSV, and each value specifies the data type 
# (e.g., "character", "numeric", "integer"):
col_classes = c("GEOID20"="character",
                "STATEFP"="character",
                "COUNTYFP"="character")

# Call the function to create or modify schema.ini
create_or_modify_schema_ini(csv_file, col_classes)

