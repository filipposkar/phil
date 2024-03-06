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


def extract_base_name(basename: str) -> str:
    """
    Uses regular expression in order to extract the base name of a column.

    Parameters:
        basename (str): The DataFrame column to be corrected.

    Returns:
        (str): The extracted basename without the index.
    """
    try:
        # Match the first word
        match = re.match(r"(\w+)", basename)
        if match:
            return match.group(1)
        else:
            return basename
    except Exception as error:
        # Print and handle any error that occurs
        print(error)


def generate_replacement_map(df: pd.DataFrame) -> dict:
    """
    Generate a replacement map for correcting values in the 'target' column of a DataFrame.
    The replacement map is created based on the substring before the dot in each 'target' value.

    Parameters:
        df (pd.DataFrame): The DataFrame containing the 'target' column to be corrected.

    Returns:
        dict: A dictionary where keys are the substrings before the dot and values are sets of corresponding 'target' values.

    Raises:
        Exception: If an error occurs during the generation of the replacement map.
    """
    try:
        # Initialize an empty dictionary to store the replacement map
        replacement_map = {}

        # Get distinct values of the 'target' column
        df_target_distinct_list = df['target'].unique()

        # Loop through all distinct values
        for value in df_target_distinct_list:
            # Extract the substring before the dot
            prefix = value.split('.')[0]
            # Check if the prefix is already in the replacement map
            if prefix not in replacement_map:
                # If not, initialize a set with the current 'target' value
                replacement_map[prefix] = {value}
            else:
                # If yes, add the current 'target' value to the existing set
                replacement_map[prefix].add(value)
        return replacement_map
    except Exception as error:
        # Print and handle any error that occurs
        print(error)


def correct_target(df: pd.DataFrame) -> pd.DataFrame:
    """
    Corrects the values in the 'target' column of a DataFrame.

    Parameters:
        df (DataFrame): The DataFrame containing the 'target' column to be corrected.

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

        # replacements = {
        #     "streetName": "streetName",
        #     "province": "province",
        #     "punctuation_mark": "punctuation_mark",
        #     "streetNumber": "streetNumber",
        #     "unit": "unit"
        # }
        # df["target"] = df["target"].apply(lambda target_value: replacements.get(extract_base_name(target_value), target_value))

        # Call function to gather all values
        replacements = generate_replacement_map(df)

        # Find and replace wrong values in "target"
        df["target"] = df["target"].apply(
            lambda target_value: target_value.split('.')[0] if target_value not in replacements else target_value)
        return df
    except Exception as error:
        # Print and handle any error that occurs
        print(error)


def main(excel_file: str, columns_to_drop: list) -> None:
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

        # Check if column list is empty
        if columns_to_drop:
            # Check if there is any input column that does not match with excel
            if set(columns_to_drop) <= set(excel_df.columns.to_list()):
                print(f"Deleting columns -> {sorted(columns_to_drop)}")
                excel_df = excel_df.drop(
                    columns=excel_df.columns[excel_df.columns.map(lambda x: x.split('.')[0] in columns_to_drop)])
            else:
                print(f"Input columns to drop: {set(columns_to_drop) - set(excel_df.columns.to_list())} are not valid.")

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
        # Print and handle any error that occurs
        print(main_error)


if __name__ == '__main__':
    try:
        kwargs = {
            "excel_file": "input_output_template.xlsx",  # Set the Excel file with the input data
            "columns_to_drop": [...],  # Set the columns to be dropped
        }
        main(**kwargs)
    except Exception as error:
        print(error)
