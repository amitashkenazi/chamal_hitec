import pandas as pd
from pathlib import Path

def save_sheets_as_csv(file_path):
    # Load the Excel workbook
    xls = pd.ExcelFile(file_path)

    # Iterate through each sheet in the workbook
    for sheet_name in xls.sheet_names:
        # Load the sheet into a DataFrame
        df = xls.parse(sheet_name)

        # Create a CSV filename based on the Excel filename and sheet name
        csv_filename = f"data/{file_path.stem}_{sheet_name}.csv"

        # Save the DataFrame to a CSV file
        df.to_csv(csv_filename, index=False)

    # Close the Excel workbook
    xls.close()

# Usage:
file_path = Path("data/_1698142363.xlsx")
save_sheets_as_csv(file_path)
