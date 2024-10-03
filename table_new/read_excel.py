import pandas as pd

# Define the file name globally in table.py
file_name = "table_coordinates.xlsx"

def excel_to_dataframe():
    # Load the Excel file to check for available sheets
    excel_file = pd.ExcelFile(file_name)
    
    # List available sheets and prompt the user to choose by number
    print("Available sheets:")
    for idx, sheet in enumerate(excel_file.sheet_names, 1):
        print(f"{idx}. {sheet}")
    
    # Prompt the user to select a sheet by entering the corresponding number
    while True:
        try:
            sheet_choice = int(input("Please enter the number of the sheet you want to load: "))
            if 1 <= sheet_choice <= len(excel_file.sheet_names):
                sheet_name = excel_file.sheet_names[sheet_choice - 1]
                break
            else:
                print("Invalid choice. Please enter a number between 1 and", len(excel_file.sheet_names))
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Read the specific sheet from the Excel file, skipping the first row (titles)
    df = pd.read_excel(file_name, sheet_name=sheet_name, skiprows=0)
    
    # Ensure the structure: x, y, symbol, and Include
    if df.shape[1] != 4:
        raise ValueError("The Excel sheet must contain exactly 4 columns: Symbol, x, y, and Include.")
    
    # Validate the column types
    if not pd.api.types.is_numeric_dtype(df.iloc[:, 1]) or not pd.api.types.is_numeric_dtype(df.iloc[:, 2]):
        raise ValueError("The second and third columns must be numeric (x and y coordinates).")
    if not pd.api.types.is_string_dtype(df.iloc[:, 0]):
        raise ValueError("The first column must be a string (element symbol).")
    if not pd.api.types.is_numeric_dtype(df.iloc[:, 3]):
        raise ValueError("The fourth column must be numeric (Include).")

    # Filter the DataFrame to include only rows where 'Include' column is 1
    if 'Include' not in df.columns:
        raise KeyError("'Include' column not found in the Excel file. Please check the column name.")
        
    df_filtered = df[df['Include'] == 1].copy()

    # Return the filtered dataframe and the sheet name
    return df_filtered, sheet_name