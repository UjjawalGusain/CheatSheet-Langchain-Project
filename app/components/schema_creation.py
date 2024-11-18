import pandas as pd
def create_schema(df):
    # Create the schema description with column names and their data types
    schema = {col: str(df[col].dtype) for col in df.columns}
    
    # Get the size of the DataFrame (number of rows and columns)
    df_size = df.shape  # (rows, columns)
    
    # Format the schema into a readable string
    schema_description = f"DataFrame Size: {df_size[0]} rows, {df_size[1]} columns\n"
    schema_description += "Columns and Data Types:\n"
    schema_description += "\n".join([f"{col}: {dtype}" for col, dtype in schema.items()])
    
    return schema_description


