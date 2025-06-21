try:
    import pandas as pd
except ImportError as import_error:
    print(import_error)

# Set pandas options
pd.set_option("display.max_columns", None)
#pd.options.mode.copy_on_write = True


class ReplaceClass:
    def __init__(
        self,
        input_str: str,
        convert_to_elot: bool,
        convert_to_voice_eq: bool,
    ):
        self.input_str = input_str

        if not (convert_to_elot or convert_to_voice_eq):
            print(
                "Please set to True the keyword either for Converting to ELOT or for Voice Equivalen"
            )
        else:
            self.replacement_group, self.column_name = (
                ("replacements_normalize_string_EngELOT743", "ELOT")
                if convert_to_elot
                else ("replacements_normalize_string_Eng", "Voice_equivalent")
            )

        self.replacements_normalize_string = [
            ("ΟΥ", "U"),
            ("ΟΙ", "Ι"),
            ("ΥΙ", "Ι"),
            ("ΕΙ", "Ι"),
            ("ΑΙ", "Ε"),
            ("Η", "Ι"),
            ("Υ", "Ι"),
            ("Ω", "Ο"),
            ("Ά", "Α"),
            ("Έ", "Ε"),
            ("Ί", "Ι"),
            ("Ϊ", "Ι"),
        ]

        self.replacements_normalize_string_EngELOT743_lower = [
            ("άι", "α$$"),
            ("όι", "ο$$"),
            ("έι", "ε$$"),
            ("ά", "α"),
            ("έ", "ε"),
            ("ΐ", "ϊ"),
            ("αϊ", "ai"),
            ("αΐ", "ai"),
            ("εϊ", "ei"),
            ("εΐ", "ei"),
            ("οϊ", "oi"),
            ("οΐ", "oi"),
            ("οϋ", "oi"),
            ("οΰ", "oi"),
            ("ϊ", "υ"),
            ("ΰ", "υ"),
            ("ί", "ι"),
            ("ή", "η"),
            ("ό", "ο"),
            ("ώ", "ω"),
            ("ύ", "υ"),
            ("ϋ", "υ"),
            ("ΰ", "υ"),
            ("$$", "ι"),
        ]

        self.replacements_normalize_string_EngELOT743_upper = [
            ("ΑΥΑ", "AVΑ"),
            ("ΑΥΒ", "AV"),
            ("ΑΥΓ", "AVΓ"),
            ("ΑΥΔ", "AVΔ"),
            ("ΑΥΕ", "AVΕ"),
            ("ΑΥΖ", "AVΖ"),
            ("ΑΥΗ", "AVΗ"),
            ("ΑΥΙ", "AVΙ"),
            ("ΑΥΛ", "AVΛ"),
            ("ΑΥΜ", "AVΜ"),
            ("ΑΥΝ", "AVΝ"),
            ("ΑΥΡ", "AVΡ"),
            ("ΑΥΟ", "AVΟ"),
            ("ΑΥΥ", "AVΥ"),
            ("ΑΥΩ", "AVΩ"),
            ("ΑΥΘ", "AFΘ"),
            ("ΑΥΚ", "AFΚ"),
            ("ΑΥΞ", "AFΞ"),
            ("ΑΥΠ", "AFΠ"),
            ("ΑΥΣ", "AFΣ"),
            ("ΑΥΤ", "AFΤ"),
            ("ΑΥΦ", "AFΦ"),
            ("ΑΥΧ", "AFΧ"),
            ("ΑΥΨ", "AFΨ"),
            ("ΑΥ ", "AF "),
            ("ΕΥΑ", "EVΑ"),
            ("ΕΥΒ", "EV"),
            ("ΕΥΓ", "EVΓ"),
            ("ΕΥΔ", "EVΔ"),
            ("ΕΥΕ", "EVΕ"),
            ("ΕΥΖ", "EVΖ"),
            ("ΕΥΗ", "EVΗ"),
            ("ΕΥΙ", "EVΙ"),
            ("ΕΥΛ", "EVΛ"),
            ("ΕΥΜ", "EVΜ"),
            ("ΕΥΝ", "EVΝ"),
            ("ΕΥΡ", "EVΡ"),
            ("ΕΥΟ", "EVΟ"),
            ("ΕΥΥ", "EVΥ"),
            ("ΕΥΩ", "EVΩ"),
            ("ΕΥΘ", "EFΘ"),
            ("ΕΥΚ", "EFΚ"),
            ("ΕΥΞ", "EFΞ"),
            ("ΕΥΠ", "EFΠ"),
            ("ΕΥΣ", "EFΣ"),
            ("ΕΥΤ", "EFΤ"),
            ("ΕΥΦ", "EFΦ"),
            ("ΕΥΧ", "EFΧ"),
            ("ΕΥΨ", "EFΨ"),
            ("ΕΥ ", "EF "),
            ("ΗΥΑ", "IVΑ"),
            ("ΗΥΒ", "IV"),
            ("ΗΥΓ", "IVΓ"),
            ("ΗΥΔ", "IVΔ"),
            ("ΗΥΕ", "IVΕ"),
            ("ΗΥΖ", "IVΖ"),
            ("ΗΥΗ", "IVΗ"),
            ("ΗΥΙ", "IVΙ"),
            ("ΗΥΛ", "IVΛ"),
            ("ΗΥΜ", "IVΜ"),
            ("ΗΥΝ", "IVΝ"),
            ("ΗΥΡ", "IVΡ"),
            ("ΗΥΟ", "IVΟ"),
            ("ΗΥΥ", "IVΥ"),
            ("ΗΥΩ", "IVΩ"),
            ("ΗΥΘ", "IFΘ"),
            ("ΗΥΚ", "IFΚ"),
            ("ΗΥΞ", "IFΞ"),
            ("ΗΥΠ", "IFΠ"),
            ("ΗΥΣ", "IFΣ"),
            ("ΗΥΤ", "IFΤ"),
            ("ΗΥΦ", "IFΦ"),
            ("ΗΥΧ", "IFΧ"),
            ("ΗΥΨ", "IFΨ"),
            ("ΗΥ ", "IF "),
            (" ΜΠ", " B"),
            ("ΓΓ", "NG"),
            ("ΓΞ", "NX"),
            ("ΓΧ", "NCH"),
            ("ΟΥ", "OU"),
            ("Χ", "CH"),
            ("Ψ", "PS"),
            ("Θ", "TH"),
            ("Ά", "A"),
            ("Α", "A"),
            ("Β", "V"),
            ("Γ", "G"),
            ("Δ", "D"),
            ("Ε", "E"),
            ("Έ", "E"),
            ("Ζ", "Z"),
            ("Η", "I"),
            ("Ή", "I"),
            ("Ι", "I"),
            ("Ί", "I"),
            ("Κ", "K"),
            ("Λ", "L"),
            ("Μ", "M"),
            ("Ν", "N"),
            ("Ξ", "X"),
            ("Ο", "O"),
            ("Π", "P"),
            ("Ρ", "R"),
            ("Σ", "S"),
            ("Τ", "T"),
            ("Ύ", "Y"),
            ("Υ", "Y"),
            ("Φ", "F"),
            ("Ω", "O"),
            ("Ώ", "O"),
        ]

        self.replacements_normalize_string_Eng_lower = [
            ("άι", "α$$"),
            ("όι", "ο$$"),
            ("έι", "ε$$"),
            ("ά", "α"),
            ("έ", "ε"),
            ("ΐ", "ϊ"),
            ("αϊ", "ai"),
            ("αΐ", "ai"),
            ("εϊ", "ei"),
            ("εΐ", "ei"),
            ("οϊ", "oi"),
            ("οΐ", "oi"),
            ("οϋ", "oi"),
            ("οΰ", "oi"),
            ("ϊ", "υ"),
            ("ΰ", "υ"),
            ("ί", "ι"),
            ("ή", "η"),
            ("ό", "ο"),
            ("ώ", "ω"),
            ("ύ", "υ"),
            ("ϋ", "υ"),
            ("ΰ", "υ"),
            ("$$", "ι"),
        ]

        self.replacements_normalize_string_Eng_upper = [
            ("ΑΥΣΑ", "ΑΥSΑ"),
            ("ΑΥΣΕ", "ΑΥSΕ"),
            ("ΑΥΣΙ", "ΑΥSΙ"),
            ("ΑΥΣΗ", "ΑΥSΗ"),
            ("ΑΥΣΟ", "ΑΥSΟ"),
            ("ΑΥΣΥ", "ΑΥSΥ"),
            ("ΑΥΣΩ", "ΑΥSΩ"),
            ("ΕΥΣΑ", "ΕΥSΑ"),
            ("ΕΥΣΕ", "ΕΥSΕ"),
            ("ΕΥΣΙ", "ΕΥSΙ"),
            ("ΕΥΣΗ", "ΕΥSΗ"),
            ("ΕΥΣΟ", "ΕΥSΟ"),
            ("ΕΥΣΥ", "ΕΥSΥ"),
            ("ΕΥΣΩ", "ΕΥSΩ"),
            ("ΕΙΣΑ", "ΕΙΣΣΑ"),
            ("ΕΙΣΕ", "ΕΙΣΣΕ"),
            ("ΕΙΣΙ", "ΕΙΣΣΙ"),
            ("ΕΙΣΗ", "ΕΙΣΣΗ"),
            ("ΕΙΣΟ", "ΕΙΣΣΟ"),
            ("ΕΙΣΥ", "ΕΙΣΣΥ"),
            ("ΕΙΣΩ", "ΕΙΣΣΩ"),
            ("ΥΙΣΑ", "ΥΙΣΣΑ"),
            ("ΥΙΣΕ", "ΥΙΣΣΕ"),
            ("ΥΙΣΙ", "ΥΙΣΣΙ"),
            ("ΥΙΣΗ", "ΥΙΣΣΗ"),
            ("ΥΙΣΟ", "ΥΙΣΣΟ"),
            ("ΥΙΣΥ", "ΥΙΣΣΥ"),
            ("ΥΙΣΩ", "ΥΙΣΣΩ"),
            ("ΑΙΣΑ", "ΑΙΣΣΑ"),
            ("ΑΙΣΕ", "ΑΙΣΣΕ"),
            ("ΑΙΣΙ", "ΑΙΣΣΙ"),
            ("ΑΙΣΗ", "ΑΙΣΣΗ"),
            ("ΑΙΣΟ", "ΑΙΣΣΟ"),
            ("ΑΙΣΥ", "ΑΙΣΣΥ"),
            ("ΑΙΣΩ", "ΑΙΣΣΩ"),
            ("ΟΙΣΑ", "ΟΙΣΣΑ"),
            ("ΟΙΣΕ", "ΟΙΣΣΕ"),
            ("ΟΙΣΙ", "ΟΙΣΣΙ"),
            ("ΟΙΣΗ", "ΟΙΣΣΗ"),
            ("ΟΙΣΟ", "ΟΙΣΣΟ"),
            ("ΟΙΣΥ", "ΟΙΣΣΥ"),
            ("ΟΙΣΩ", "ΟΙΣΣΩ"),
            ("ΟΥΣΑ", "ΟΥΣΣΑ"),
            ("ΟΥΣΕ", "ΟΥΣΣΕ"),
            ("ΟΥΣΙ", "ΟΥΣΣΙ"),
            ("ΟΥΣΗ", "ΟΥΣΣΗ"),
            ("ΟΥΣΟ", "ΟΥΣΣΟ"),
            ("ΟΥΣΥ", "ΟΥΣΣΥ"),
            ("ΟΥΣΩ", "ΟΥΣΣΩ"),
            ("ΑΣΥΙ", "ΑΣΣΥΙ"),
            ("ΕΣΥΙ", "ΕΣΣΥΙ"),
            ("ΙΣΥΙ", "ΙΣΣΥΙ"),
            ("ΗΣΥΙ", "ΗΣΣΥΙ"),
            ("ΟΣΥΙ", "ΟΣΣΥΙ"),
            ("ΥΣΥΙ", "ΥΣΣΥΙ"),
            ("ΩΣΥΙ", "ΩΣΣΥΙ"),
            ("ΑΣΑΙ", "ΑΣΣΑΙ"),
            ("ΕΣΑΙ", "ΕΣΣΑΙ"),
            ("ΙΣΑΙ", "ΙΣΣΑΙ"),
            ("ΗΣΑΙ", "ΗΣΣΑΙ"),
            ("ΟΣΑΙ", "ΟΣΣΑΙ"),
            ("ΥΣΑΙ", "ΥΣΣΑΙ"),
            ("ΩΣΑΙ", "ΩΣΣΑΙ"),
            ("ΑΣΟΙ", "ΑΣΣΟΙ"),
            ("ΕΣΟΙ", "ΕΣΣΟΙ"),
            ("ΙΣΟΙ", "ΙΣΣΟΙ"),
            ("ΗΣΟΙ", "ΗΣΣΟΙ"),
            ("ΟΣΟΙ", "ΟΣΣΟΙ"),
            ("ΥΣΟΙ", "ΥΣΣΟΙ"),
            ("ΩΣΟΙ", "ΩΣΣΟΙ"),
            ("ΑΣΟΥ", "ΑΣΣΟΥ"),
            ("ΕΣΟΥ", "ΕΣΣΟΥ"),
            ("ΙΣΟΥ", "ΙΣΣΟΥ"),
            ("ΗΣΟΥ", "ΗΣΣΟΥ"),
            ("ΟΣΟΥ", "ΟΣΣΟΥ"),
            ("ΥΣΟΥ", "ΥΣΣΟΥ"),
            ("ΩΣΟΥ", "ΩΣΣΟΥ"),
            ("ΑΣΕΥ", "ΑΣΣΕΥ"),
            ("ΕΣΕΥ", "ΕΣΣΕΥ"),
            ("ΙΣΕΥ", "ΙΣΣΕΥ"),
            ("ΗΣΕΥ", "ΗΣΣΕΥ"),
            ("ΟΣΕΥ", "ΟΣΣΕΥ"),
            ("ΥΣΕΥ", "ΥΣΣΕΥ"),
            ("ΩΣΕΥ", "ΩΣΣΕΥ"),
            ("ΑΣΑΥ", "ΑΣΣΑΥ"),
            ("ΕΣΑΥ", "ΕΣΣΑΥ"),
            ("ΙΣΑΥ", "ΙΣΣΑΥ"),
            ("ΗΣΑΥ", "ΗΣΣΑΥ"),
            ("ΟΣΑΥ", "ΟΣΣΑΥ"),
            ("ΥΣΑΥ", "ΥΣΣΑΥ"),
            ("ΩΣΑΥ", "ΩΣΣΑΥ"),
            ("ΑΣΕΙ", "ΑΣΣΕΙ"),
            ("ΕΣΕΙ", "ΕΣΣΕΙ"),
            ("ΙΣΕΙ", "ΙΣΣΕΙ"),
            ("ΗΣΕΙ", "ΗΣΣΕΙ"),
            ("ΟΣΕΙ", "ΟΣΣΕΙ"),
            ("ΥΣΕΙ", "ΥΣΣΕΙ"),
            ("ΩΣΕΙ", "ΩΣΣΕΙ"),
            ("ΑΣΑ", "ΑΣΣΑ"),
            ("ΑΣΕ", "ΑΣΣΕ"),
            ("ΑΣΗ", "ΑΣΣΗ"),
            ("ΑΣΙ", "ΑΣΣΙ"),
            ("ΑΣΟ", "ΑΣΣΟ"),
            ("ΑΣΥ", "ΑΣΣΥ"),
            ("ΑΣΩ", "ΑΣΣΩ"),
            ("ΕΣΑ", "ΕΣΣΑ"),
            ("ΕΣΕ", "ΕΣΣΕ"),
            ("ΕΣΗ", "ΕΣΣΗ"),
            ("ΕΣΙ", "ΕΣΣΙ"),
            ("ΕΣΟ", "ΕΣΣΟ"),
            ("ΕΣΥ", "ΕΣΣΥ"),
            ("ΕΣΩ", "ΕΣΣΩ"),
            ("ΗΣΑ", "ΕΣΣΑ"),
            ("ΗΣΕ", "ΕΣΣΕ"),
            ("ΗΣΗ", "ΕΣΣΗ"),
            ("ΗΣΙ", "ΗΣΣΙ"),
            ("ΗΣΙ", "ΕΣΣΙ"),
            ("ΗΣΟ", "ΗΣΣΟ"),
            ("ΗΣΟ", "ΕΣΣΟ"),
            ("ΗΣΥ", "ΕΣΣΥ"),
            ("ΗΣΩ", "ΕΣΣΩ"),
            ("ΙΣΑ", "IΣΣΑ"),
            ("ΙΣΕ", "IΣΣΕ"),
            ("ΙΣΗ", "IΣΣΗ"),
            ("ΙΣΙ", "IΣΣΙ"),
            ("ΙΣΟ", "IΣΣΟ"),
            ("ΙΣΥ", "IΣΣΥ"),
            ("ΙΣΩ", "IΣΣΩ"),
            ("ΟΣΑ", "ΟΣΣΑ"),
            ("ΟΣΕ", "ΟΣΣΕ"),
            ("ΟΣΗ", "ΟΣΣΗ"),
            ("ΟΣΙ", "ΟΣΣΙ"),
            ("ΟΣΟ", "ΟΣΣΟ"),
            ("ΟΣΥ", "ΟΣΣΥ"),
            ("ΟΣΩ", "ΟΣΣΩ"),
            ("ΥΣΑ", "ΥΣΣΑ"),
            ("ΥΣΕ", "ΥΣΣΕ"),
            ("ΥΣΗ", "ΥΣΣΗ"),
            ("ΥΣΙ", "ΥΣΣΙ"),
            ("ΥΣΟ", "ΥΣΣΟ"),
            ("ΥΣΥ", "ΥΣΣΥ"),
            ("ΥΣΩ", "ΥΣΣΩ"),
            ("ΩΣΑ", "ΩΣΣΑ"),
            ("ΩΣΕ", "ΩΣΣΕ"),
            ("ΩΣΗ", "ΩΣΣΗ"),
            ("ΩΣΙ", "ΩΣΣΙ"),
            ("ΩΣΟ", "ΩΣΣΟ"),
            ("ΩΣΥ", "ΩΣΣΥ"),
            ("ΩΣΩ", "ΩΣΣΩ"),
            ("ΕΥΒ", "EV"),
            ("ΕΥΔ", "EVD"),
            ("ΕΥΜ", "EVM"),
            ("ΕΥΓ", "EVG"),
            ("ΕΥΗ", "EVI"),
            ("ΕΥΑ", "EVA"),
            ("ΕΥΜ", "EVM"),
            ("ΕΥΛ", "EVL"),
            ("ΕΥΝ", "EVN"),
            ("ΕΥΟ", "EVO"),
            ("ΕΥΡ", "EVR"),
            ("ΕΥΕ", "EVE"),
            ("ΑΥΔ", "AYD"),
            ("ΑΥΜ", "AVM"),
            ("ΑΥΓ", "AVG"),
            ("ΑΥΗ", "AVI"),
            ("ΑΥΑ", "AVA"),
            ("ΑΥΜ", "AVM"),
            ("ΑΥΛ", "AVL"),
            ("ΑΥΝ", "AVN"),
            ("ΑΥΟ", "AVO"),
            ("ΑΥΡ", "AVR"),
            ("ΑΥΕ", "AVE"),
            ("ΓΓ", "G"),
            ("ΓΚ", "G"),
            ("ΜΠ", "B"),
            ("ΝΤ", "D"),
            ("ΟΥ", "OU"),
            ("ΟΙ", "I"),
            ("ΥΙ", "I"),
            ("ΕΙ", "I"),
            ("ΑΙ", "E"),
            ("ΑΥ", "AF"),
            ("ΕΥΗ", "EVI"),
            ("ΕΥ", "EF"),
            ("Χ", "CH"),
            ("Ψ", "PS"),
            ("Θ", "TH"),
            ("Ά", "A"),
            ("Α", "A"),
            ("Β", "V"),
            ("Γ", "G"),
            ("Δ", "D"),
            ("Ε", "E"),
            ("Έ", "E"),
            ("Ζ", "Z"),
            ("Η", "I"),
            ("Ή", "I"),
            ("Ι", "I"),
            ("Ί", "I"),
            ("Κ", "K"),
            ("Λ", "L"),
            ("Μ", "M"),
            ("Ν", "N"),
            ("Ξ", "X"),
            ("Ο", "O"),
            ("Π", "P"),
            ("Ρ", "R"),
            ("Σ", "S"),
            ("Τ", "T"),
            ("Ύ", "I"),
            ("Υ", "I"),
            ("Φ", "F"),
            ("Ω", "O"),
            ("Ώ", "O"),
        ]

    def search_and_replace_normalize(self, input_str) -> str:
        """
        Normalize the input string by performing a series of search and replace operations
        using specified replacement groups for lowercase and uppercase transformations.

        The replacement rules are applied in the following sequence:
        1. Convert the input string to lowercase.
        2. Apply replacements using the '_lower' group.
        3. Convert the modified string to uppercase.
        4. Apply replacements using the '_upper' group.
        5. Convert the final string to title case.

        Parameters:
        - input_str (str): The string to be normalized.

        Returns:
        - str: The normalized string after applying the search and replace transformations.
        """
        try:
            # If the input string is empty, return an empty string
            if input_str == "":
                return ""

            # Convert the input string to lowercase for initial replacements
            input_str = input_str.lower()

            # Apply replacements based on the '_lower' replacement group
            # Example: self.replacements_normalize_string_Eng_lower
            for key, value in getattr(self, self.replacement_group + "_lower"):
                if key in input_str:
                    input_str = input_str.replace(key, value)

            # Convert the modified string to uppercase for the next set of replacements
            input_str = input_str.upper()

            # Apply replacements based on the '_upper' replacement group
            # Example: self.replacements_normalize_string_Eng_upper
            for key, value in getattr(self, self.replacement_group + "_upper"):
                if key in input_str:
                    input_str = input_str.replace(key, value)

            # Convert the final string to title case (first letter of each word capitalized)
            return input_str.lower().title()
        except Exception as error:
            # Print any error encountered during execution
            print(error)

    def replace_to_latin(self) -> None:
        """
        Replace the content of the input string with normalized text
        using the search and replace rules defined in the replacement groups.

        This method applies the normalization process to the input string
        and updates it with the transformed text.

        Modifies:
        - self.input_str: Updates the input string with normalized values.
        """
        try:
            # Apply the normalization function to the input string
            self.input_str = self.search_and_replace_normalize(self.input_str)
        except Exception as error:
            # Print any error encountered during execution
            print(error)


def main(
    input_str: str,
    convert_to_elot: bool,
    convert_to_voice_eq: bool,
) -> str:
    """
    Main function to normalize an input string and return the result.

    The process includes:
    1. Initializing the ReplaceClass with the provided parameters.
    2. Replacing text in the input string using the search and replace rules.
    3. Returning the updated string.

    Parameters:
    - input_str (str): Input string to be processed.
    - convert_to_elot (bool): Flag to indicate conversion to ELOT format.
    - convert_to_voice_eq (bool): Flag to indicate conversion to Voice Equivalent format.

    Returns:
    - str: The normalized and updated input string.
    """
    try:
        # Initialize the ReplaceClass with the provided inputs
        replace_class = ReplaceClass(
            input_str,
            convert_to_elot,
            convert_to_voice_eq,
        )

        # Perform the text replacement and normalization
        replace_class.replace_to_latin()

        return replace_class.input_str
    except Exception as main_error:
        # Print any error encountered during execution
        print(main_error)


if __name__ == "__main__":
    try:
        kwargs = {
            "input_str": ...,  # Input string that will be processed
            "convert_to_elot": ...,  # Flag indicating whether to convert text to ELOT format
            "convert_to_voice_eq": ...,  # Flag indicating whether to convert text to Voice Equivalent format
        }
        main(**kwargs)
    except Exception as error:
        print(error)
