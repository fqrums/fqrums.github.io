def remove_duplicates_from_file(input_file, output_file):
    """
    Remove duplicate numbers from a file, keeping only the first occurrence,
    add '@' prefix to each unique number, and save the result to another file.
    :param input_file: Path to the input file containing numbers
    :param output_file: Path to the output file to save unique numbers
    """
    try:
        # Read numbers from the input file
        with open(input_file, 'r') as file:
            content = file.read()

        # Split numbers, remove whitespace, and convert to integers
        numbers = [int(num.strip()) for num in content.split(",") if num.strip().isdigit()]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_numbers = []
        for num in numbers:
            if num not in seen:
                seen.add(num)
                unique_numbers.append(num)

        # Add '@' prefix and save to the output file
        prefixed_numbers = [f"@{num}" for num in unique_numbers]
        with open(output_file, 'w') as file:
            file.write(",".join(prefixed_numbers))

        print(f"Duplicates removed. Unique numbers with '@' prefix saved to {output_file}.")

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except ValueError:
        print("Error: Input file contains invalid numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    # Input and output file paths
    input_file = "numbers.txt"  # Replace with your input file
    output_file = "unique_numbers.txt"  # Replace with your desired output file

    # Process the file to remove duplicates and add '@' prefix
    remove_duplicates_from_file(input_file, output_file)
