# Note: Portions of this code may have been generated with AI assistance.
#
# Adds quotes around CSV data that may have problematic spacing or special
# characters to avoid conflicts with any scripts or systems that don't have
# adequate protections, like SQL imports.

import csv

def add_quotes_to_csv(input_file, output_file):
    """
    Read a CSV file, wrap all field values in double quotes, and write to a new file.
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile, quoting=csv.QUOTE_ALL)

            for row in reader:
                writer.writerow(row)

        print(f"Processed file saved to: {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Prompt user for input and output file paths
    input_file = input("Enter the path to the input CSV file: ").strip()
    output_file = input("Enter the path for the output CSV file: ").strip()

    add_quotes_to_csv(input_file, output_file)
