import re


def reorder_and_join(listA: list, listB: list, address_text: str) -> str:
    """
    Reorders and joins elements from two lists (listA and listB) to match their sequence in a given address text.

    Args:
        listA (list): A list of strings, typically containing street names.
        listB (list): A list of strings, typically containing other address components like numbers or symbols.
        address_text (str): The full address text to use for determining the correct order of elements.

    Returns:
        str: A string containing the reordered and joined elements from listA and listB in the sequence they appear in address_text.

    Raises:
        Exception: Prints the error if an unexpected issue occurs during processing.
    """
    try:
        # Combine both lists into one for comparison with the address text
        combined_list = listA + listB

        # Initialize an empty list to hold sorted elements
        sorted_elements = []

        # Split the address_text into words while preserving spaces using regex
        for word in re.split(r"(\s+)", address_text):
            # Remove leading/trailing spaces from the word
            word = word.strip()

            # Check if the word exists in the combined list
            if word in combined_list:
                # Add the word to the sorted elements list
                sorted_elements.append(word)
                # Remove the word from the combined list to avoid duplicates
                combined_list.remove(word)

        # Join the sorted elements into a single string with spaces
        return " ".join(sorted_elements)
    except Exception as error:
        # Print any errors encountered during execution
        print(error)


if __name__ == "__main__":
    # Default values for standalone testing
    listA = ["Μουργκάνας", "Μαρούσι"]  # Example street names
    listB = ["&", "18", "1"]  # Example numbers and symbols
    address_text = "Μελισίων 18 & Μουργκάνας 1 Μαρούσι 15126"  # Full address text for comparison

    # Call the function with default values and print the result
    result = reorder_and_join(listA, listB, address_text)
    print(f"Result -> {result}")  # Expected output: 18 & Μουργκάνας 1 Μαρούσι
