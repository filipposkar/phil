try:
    import os
    import pandas as pd
    from typing import Tuple, Any
except ImportError as import_err:
    print(import_err)

# Set pandas options
pd.set_option("display.max_columns", None)
pd.options.mode.copy_on_write = True


def split_train_test_val_sets(df: pd.DataFrame, splits_dict: dict) -> list:
    """
    Split the DataFrame into train, test, and validation sets based on the provided splits.

    Parameters:
        df (pandas.DataFrame): The DataFrame to be split.
        splits_dict (dict): A dictionary containing the desired splits for train, test, and validation sets.

    Returns:
        list: A list containing tuples representing the start and end indices for each subset.
    """
    # Filter the DataFrame to include only rows with line_number == 0
    df_zero = df[df["line_number"] == 0]
    # Get the indices of these rows
    df_zero_indices = df_zero.index.to_numpy()
    # Calculate the total number of addresses
    number_of_addresses = len(df_zero_indices)

    # Initialize a dictionary to store the split indices
    split_data_dict = {}
    sum_rows = 0
    # Calculate the index at which each split should occur
    for key, value in splits_dict.items():
        sum_rows += int(value * number_of_addresses)
        split_data_dict[key] = df_zero_indices[sum_rows]

    # Convert the split data dictionary to a list of tuples
    subset_list = [(key, value) for key, value in split_data_dict.items()]

    return subset_list


def check_subset_fractions(frac_tuple: tuple) -> bool:
    """
    Check if the fractions specified for splitting sum up to 1.

    Parameters:
        frac_tuple (tuple): A tuple containing the fractions for splitting.

    Returns:
        bool: True if the fractions sum up to 1, False otherwise.
    """
    try:
        # Calculate the sum of fractions in the tuple
        total_frac = sum(frac_tuple)

        # Check if the sum is equal to 1
        if total_frac == 1:
            return True
        else:
            # Print a message if the sum is not 1
            print("Splitting fractions sum must be 1.")
            return False  # Return False to indicate failure
    except Exception as error:
        # Print and handle any error that occurs
        print(error)
        return False  # Return False to indicate failure


def main(input_file: str, sets_fract_dict: dict) -> any:
    """
    Main function to split the input DataFrame into sub DataFrames based on the provided fractions.

    Parameters:
        input_file (str): The path to the input CSV file.
        sets_fract_dict (dict): A dictionary containing fractions for train, test, and validation subsets.

    Returns:
        any: A list containing three sub DataFrames.
    """
    try:
        # Print information about the splitting fractions
        print(f"Splitting into sub DataFrames for"
              f"\n\ttrain: {sets_fract_dict['train_subset']},"
              f"\n\ttest: {sets_fract_dict['test_subset']},"
              f"\n\tvalidation: {sets_fract_dict['val_subset']},", end="\n\n"
              )

        # Navigate to the processed data directory
        # os.chdir("../../data/processed")

        # Read the input CSV file into a DataFrame
        input_df = pd.read_csv(input_file, header=0)

        # Convert the fractions dictionary into a tuple
        sets_fract_tuple = tuple(sets_fract_dict[key] for key in sets_fract_dict)

        # Check if the fractions sum up to 1
        check_fract = check_subset_fractions(sets_fract_tuple)
        if check_fract:
            dataframes = []
            subset_indexes_list = split_train_test_val_sets(input_df, sets_fract_dict)

            last_index = 0
            for subset in subset_indexes_list:
                df_name = str(subset[0]) + "_df"
                df_name = input_df[(input_df.index > last_index) & (input_df.index < subset[1])]
                dataframes.append(df_name)
                last_index = df_name.index[-1]

            # Print and return the list of sub DataFrames
            print("Returning 3 sub DataFrames (train, test, validate).")
            return dataframes

        # Print a message if the fractions are invalid
        print("Splitting into subsets process ended.")
    except Exception as main_error:
        # Print and handle any error that occurs
        print(main_error)


if __name__ == "__main__":
    try:
        kwargs = {
            "input_file": "output.csv",  # Set the Excel file with the input data
            "sets_fract_dict": {"train_subset": 0.8,
                                "test_subset": 0.1,  # Set fractions in order to split dataset
                                "val_subset": 0.1}
        }
        main(**kwargs)
    except Exception as error:
        print(error)
