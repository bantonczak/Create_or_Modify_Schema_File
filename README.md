### README.md
#### Author: Brittany Antonczak<br/>Last Updated: 2024-08-16

<br/> 

---

## **create_or_modify_schema_ini**
#### *Function to generate or modify a schema.ini file for ArcGIS*

---

<br/> 

This function generates or modifies a schema.ini file for a specified CSV file without hardcoding column names or data types. The resulting schema.ini file will be formatted to ensure compatibility with ArcGIS Pro, facilitating accurate data import.

Schema.ini files are crucial for ensuring that ArcGIS correctly interprets the data in a delimited text file, including proper handling of field types and values. This is particularly important for fields with leading zeros (e.g., GEOIDs), which require precise formatting to maintain data integrity.

<br/> 

### **Usage**

```{}
create_or_modify_schema_ini(csv_file, col_classes = NULL)
```
  
<br/> 

### **Arguments**

**csv_file** - (character) File name with file extension (e.g., .csv) of text data source.<br/> 
**col_classes** - an unnamed vector of types corresponding to the columns in the file, or a named vector specifying types for a subset of the columns by name. The default, NULL means types are inferred from the data in the file.<br/> 

<br/> 

### **Example**

# Example usage:

# Specify the path to the CSV file
csv_file <- "your_file.csv"

# Optionally, define column classes
col_classes <- col_classes = c("GEOID20"="character",
                               "STATEFP"="character",
                               "COUNTYFP"="character")

# Call the function to create or modify schema.ini
create_or_modify_schema_ini(csv_file, col_classes)

<br/> 

