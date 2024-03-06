try:
    import os
    import pandas as pd
    import openpyxl as opyxl
    from openpyxl.utils.dataframe import dataframe_to_rows
    import re
except Exception as import_err:
    print(import_err)

# Set pandas options
pd.set_option("display.max_columns", None)
pd.options.mode.copy_on_write = True


def extract_base_name(x) -> str:
    try:
        # Match the first word
        match = re.match(r"(\w+)", x)
        if match:
            return match.group(1)
        else:
            return x
    except Exception as error:
        print(error)


def correct_target(filtered_df) -> any:
    """
    Corrects the values in the 'target' column of a DataFrame.

    Parameters:
        filtered_df (DataFrame): The DataFrame containing the 'target' column to be corrected.

    Returns:
        DataFrame: The DataFrame with corrected 'target' values.

    Note:
        This function replaces specific values in the 'target' column with standardized values.
        It checks for values containing keywords such as 'streetName', 'province', etc., and replaces them
        with corresponding standardized names. For example, 'streetName.1' will be replaced with 'streetName'.

    """
    try:
        # filtered_df["target"] = filtered_df["target"].apply(
        #     lambda x: "streetName" if "streetName" in x
        #     else ('province' if 'province' in x
        #           else ('punctuation_mark' if 'punctuation_mark' in x
        #                 else ('streetNumber' if 'streetNumber' in x
        #                       else ('unit' if 'unit' in x else x)))))

        # Find and replace wrong values in "target"
        replacements = {
            "streetName": "streetName",
            "province": "province",
            "punctuation_mark": "punctuation_mark",
            "streetNumber": "streetNumber",
            "unit": "unit"
        }

        filtered_df["target"] = filtered_df["target"].apply(lambda x: replacements.get(extract_base_name(x), x))
        return filtered_df
    except Exception as error:
        print(error)


def main(excel_file: str) -> None:
    """
    Main function to process Excel data, correct values in the "target" column,
    and output the updated data to a new tab in the same Excel file.

    Parameters:
    - excel_file (str): The path to the Excel file to process.

    Returns:
    - None
    """
    try:
        print(f"Processing for '{excel_file}'...")

        # Change directory to the raw data directory
        # os.chdir(r"../../data/raw")
        # excel_file = "input_output_template - Copy.xlsx"

        # Read data from the Excel file into a pandas DataFrame
        excel_df = pd.read_excel(excel_file, sheet_name='input', header=0)

        # Reorder DataFrame columns, moving "data_zip" and "data_city" to the end
        columns_to_reorder = ["data_zip", "data_city"]
        column_list = [column for column in excel_df.columns.to_list() if column not in columns_to_reorder]
        excel_df = excel_df.reindex(columns=column_list + columns_to_reorder)

        # Stack the DataFrame columns into indexes
        stacked_df = excel_df.stack()
        reset_stacked_df = stacked_df.reset_index()

        # Rename columns appropriately
        # TODO: check if the below is hard coded
        reset_stacked_df = reset_stacked_df.rename(columns={"level_0": "old_index", "level_1": "target", 0: "text"},
                                                   errors="raise")

        # Drop unwanted rows where "target" is 'aa', 'data_street', or 'data_number'
        column_to_filter = "target"
        values_to_filter = ["aa", "data_street", "data_number"]
        filtered_df = reset_stacked_df[~reset_stacked_df[column_to_filter].isin(values_to_filter)]

        # Merge with a new column that counts the total number of lines for each address
        count_df = filtered_df.groupby(["old_index"]).count().iloc[:, 1].rename("total_lines")
        filtered_df = filtered_df.merge(count_df, how="left", left_on="old_index", right_index=True)

        # Add a new column that counts from zero to total lines for each address
        filtered_df["line_number"] = filtered_df.groupby(["old_index", "total_lines"]).cumcount()

        # Call function to correct wrong values in "target"
        correct_target(filtered_df)

        # Reorder DataFrame columns, moving "total_lines" to the end
        columns_to_reorder = ["total_lines"]
        column_list = [column for column in filtered_df.columns.to_list() if column not in columns_to_reorder]
        filtered_df = filtered_df.reindex(columns=column_list + columns_to_reorder)

        # Create a new tab in 'excel_file'
        workbook = opyxl.load_workbook(filename=excel_file)
        sheet_name = "output"
        # Check and delete the sheet if it already exists
        if sheet_name in workbook.sheetnames:
            del workbook[sheet_name]
        ws = workbook.create_sheet(sheet_name)

        # Print DataFrame into Excel file
        for row in dataframe_to_rows(filtered_df.loc[:, filtered_df.columns != "old_index"],
                                     index=False, header=True):
            ws.append(row)

        # Save the .xlsx file
        workbook.save(excel_file)

        print(f"Saved in new tab 'output' within '{excel_file}'.")
    except Exception as main_error:
        print(main_error)


if __name__ == '__main__':
    try:
        args = {
            "input_output_template.xlsx"
        }
        main(*args)
    except Exception as error:
        print(error)
