import csv
import json
import sys
import argparse

def convert_csv_to_json(csv_path, json_path, root_key="standards"):
    """
    Reads a CSV file and converts it into a JSON file.
    Each row is converted to a JSON object, and the collection is stored
    under a specified root key in the final JSON object.

    Args:
        csv_path (str): The path to the input CSV file.
        json_path (str): The path for the output JSON file.
        root_key (str): The top-level key in the output JSON file that will
                        contain the list of objects.
    """
    print(f"Reading data from '{csv_path}'...")
    
    records = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as csv_file:
            # DictReader uses the first row as headers for the keys
            csv_reader = csv.DictReader(csv_file)
            
            for row in csv_reader:
                processed_row = {key: (None if value == '' else value) for key, value in row.items()}
                records.append(processed_row)

    except FileNotFoundError:
        print(f"Error: The file was not found at '{csv_path}'", file=sys.stderr)
        return False
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}", file=sys.stderr)
        return False

    if not records:
        print("Warning: The CSV file is empty or contains only a header row.", file=sys.stderr)
        return False

    print(f"Successfully loaded {len(records)} records. Now writing to '{json_path}'...")

    final_json_structure = {root_key: records}

    try:
        with open(json_path, 'w', encoding='utf-8') as json_file:
            # Use indent=2 for pretty-printing the JSON
            json.dump(final_json_structure, json_file, indent=2)
        
        print(f"Successfully created JSON file at: {json_path}")
        return True
    except Exception as e:
        print(f"An error occurred while writing the JSON file: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Convert a CSV file to a structured JSON file."
    )
    parser.add_argument(
        "csv_input", 
        help="The path to the input CSV file."
    )
    parser.add_argument(
        "json_output", 
        help="The path for the output JSON file."
    )
    parser.add_argument(
        "--key", 
        default="standards", 
        help="The root key to use in the JSON output (default: 'standards')."
    )

    args = parser.parse_args()

    convert_csv_to_json(args.csv_input, args.json_output, args.key)
